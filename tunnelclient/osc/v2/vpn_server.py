#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Vpn Server action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_serialization import jsonutils
from oslo_utils import uuidutils

from tunnelclient.osc.v2 import constants as const
from tunnelclient.osc.v2 import utils as v2_utils

PROVISIONING_STATUS = ['ACTIVE', 'DELETED', 'ERROR', 'PENDING_CREATE',
                       'PENDING_UPDATE', 'PENDING_DELETE']

OPERATING_STATUS = ['ONLINE', 'DRAINING', 'OFFLINE', 'DEGRADED', 'ERROR',
                    'NO_MONITOR']


class CreateVpnServer(command.ShowOne):
    """Create a vpn server"""

    @staticmethod
    def _check_attrs(attrs):
        verify_args = ['vip_subnet_id', 'vip_network_id', 'vip_port_id']
        if not any(i in attrs for i in verify_args):
            msg = ("Missing required argument: Requires one of "
                   "--vip-subnet-id, --vip-network-id or --vip-port-id")
            raise exceptions.CommandError(msg)
        if all(i in attrs for i in ('vip_network_id', 'vip_port_id')):
            msg = ("Argument error: --vip-port-id can not be used with "
                   "--vip-network-id")
            raise exceptions.CommandError(msg)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="New vpn server name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set vpn server description."
        )
        parser.add_argument(
            '--vip-address',
            metavar='<vip_address>',
            help="Set the VIP IP Address."
        )

        vip_group = parser.add_argument_group(
            "VIP Network",
            description="At least one of the following arguments is required."
        )
        vip_group.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help="Set Port for the vpn server (name or ID)."
        )
        vip_group.add_argument(
            '--vip-subnet-id',
            metavar='<vip_subnet_id>',
            help="Set subnet for the vpn server (name or ID)."
        )
        vip_group.add_argument(
            '--vip-network-id',
            metavar='<vip_network_id>',
            help="Set network for the vpn server (name or ID)."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="Set QoS policy ID for VIP port. Unset with 'None'.",
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="Project for the vpn server (name or ID)."
        )

        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help="Provider name for the vpn server."
        )

        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            default=None,
            help="Availability zone for the vpn server."
        )

        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable vpn server (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable vpn server."
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help="The name or ID of the flavor for the vpn server."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete',
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_ROWS
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        self._check_attrs(attrs)
        body = {'vpnserver': attrs}

        data = self.app.client_manager.vpn_server.vpn_server_create(
            json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.vpn_server.
                          vpn_server_show),
                res_id=data['vpnserver']['id']
            )
            data = {
                'vpnserver': (
                    self.app.client_manager.vpn_server.vpn_server_show(
                        data['vpnserver']['id']))
            }

        formatters = {
            'listeners': v2_utils.format_list,
            'resources': v2_utils.format_list,
            'users': v2_utils.format_list,
            'secgroups': v2_utils.format_list
        }

        return (rows,
                (utils.get_dict_properties(
                    data['vpnserver'], rows, formatters=formatters)))


class DeleteVpnServer(command.Command):
    """Delete a vpn server"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help="Vpn servers to delete (name or ID)"
        )
        parser.add_argument(
            '--cascade',
            action='store_true',
            default=None,
            help="Cascade the delete to all child elements of the vpn "
                 "server."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('vpnserver_id')

        self.app.client_manager.vpn_server.vpn_server_delete(
            lb_id=lb_id, **attrs)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=(self.app.client_manager.vpn_server.
                          vpn_server_show),
                res_id=lb_id
            )


class FailoverVpnServer(command.Command):
    """Trigger vpn server failover"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help="Name or UUID of the vpn server."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('vpnserver_id')
        self.app.client_manager.vpn_server.vpn_server_failover(
            lb_id=lb_id)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.vpn_server.
                          vpn_server_show),
                res_id=lb_id
            )


class ListVpnServer(lister.Lister):
    """List vpn servers"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List vpn servers according to their name."
        )
        admin_state_group = parser.add_mutually_exclusive_group()
        admin_state_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="List enabled vpn servers."
        )
        admin_state_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="List disabled vpn servers."
        )
        parser.add_argument(
            '--project',
            metavar='<project-id>',
            help="List vpn servers according to their project (name or ID)."
        )
        parser.add_argument(
            '--vip-network-id',
            metavar='<vip_network_id>',
            help="List vpn servers according to their VIP network "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-subnet-id',
            metavar='<vip_subnet_id>',
            help="List vpn servers according to their VIP subnet "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="List vpn servers according to their VIP Qos policy "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help="List vpn servers according to their VIP port "
                 "(name or ID)."
        )
        parser.add_argument(
            '--provisioning-status',
            metavar='{' + ','.join(PROVISIONING_STATUS) + '}',
            choices=PROVISIONING_STATUS,
            type=lambda s: s.upper(),
            help="List vpn servers according to their provisioning status."
        )
        parser.add_argument(
            '--operating-status',
            metavar='{' + ','.join(OPERATING_STATUS) + '}',
            choices=OPERATING_STATUS,
            type=lambda s: s.upper(),
            help="List vpn servers according to their operating status."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help="List vpn servers according to their provider."
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help="List vpn servers according to their flavor."
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            help="List vpn servers according to their availability zone."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.VPN_SERVER_COLUMNS
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)

        data = self.app.client_manager.vpn_server.vpn_server_list(
            **attrs)

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['vpnservers']))


class ShowVpnServer(command.ShowOne):
    """Show the details for a single vpn server"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help="Name or UUID of the vpn server."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_ROWS
        data = None

        if uuidutils.is_uuid_like(parsed_args.vpnserver):
            try:
                data = (
                    self.app.client_manager.vpn_server.vpn_server_show(
                        lb_id=parsed_args.vpnserver))
            except exceptions.NotFound:
                pass

        if data is None:
            attrs = v2_utils.get_vpnserver_attrs(
                self.app.client_manager, parsed_args)
            lb_id = attrs.pop('vpnserver_id')

            data = self.app.client_manager.vpn_server.vpn_server_show(
                lb_id=lb_id)

        formatters = {
            'listeners': v2_utils.format_list,
            'resources': v2_utils.format_list,
            'users': v2_utils.format_list,
            'secgroups': v2_utils.format_list
        }

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetVpnServer(command.Command):
    """Update a vpn server"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help='Name or UUID of the vpn server to update.'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set vpn server name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set vpn server description."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="Set QoS policy ID for VIP port. Unset with 'None'.",
        )

        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable vpn server."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable vpn server."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('vpnserver_id')
        body = {'vpnserver': attrs}

        self.app.client_manager.vpn_server.vpn_server_set(
            lb_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.vpn_server.
                          vpn_server_show),
                res_id=lb_id
            )


class UnsetVpnServer(command.Command):
    """Clear vpn server settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help='Name or UUID of the vpn server to update.'
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the vpn server name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the vpn server description."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            action='store_true',
            help="Clear the vpn server QoS policy.",
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete',
        )

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        lb_id = v2_utils.get_resource_id(
            self.app.client_manager.vpn_server.vpn_server_list,
            'vpnservers', parsed_args.vpnserver)

        body = {'vpnserver': unset_args}

        self.app.client_manager.vpn_server.vpn_server_set(
            lb_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.vpn_server.
                          vpn_server_show),
                res_id=lb_id
            )


class ShowVpnServerStats(command.ShowOne):
    """Shows the current statistics for a vpn server"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help="Name or UUID of the vpn server."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_STATS_ROWS
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('vpnserver_id')

        data = self.app.client_manager.vpn_server.vpn_server_stats_show(
            lb_id=lb_id
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))


class ShowVpnServerStatus(command.Command):
    """Display vpn server status tree in json format"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpn_server>',
            help="Name or UUID of the vpn server."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_vpnserver_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('vpnserver_id')

        data = self.app.client_manager.vpn_server.vpn_server_status_show(
            lb_id=lb_id
        )
        res = data.get('statuses', {})
        print(jsonutils.dumps(res, indent=4))
