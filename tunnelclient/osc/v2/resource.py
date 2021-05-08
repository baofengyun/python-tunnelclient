#   Copyright 2017 GoDaddy
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

"""Resource action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from tunnelclient.osc.v2 import constants as const
from tunnelclient.osc.v2 import utils as v2_utils
from tunnelclient.osc.v2 import validate

PROTOCOL_CHOICES = ['TCP', 'UDP']

class CreateResource(command.ShowOne):
    """Create a resource"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpnserver>',
            help="Vpn server for the resource (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the resource name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this resource."
        )
        parser.add_argument(
            '--subnet-id',
            metavar='<subnet_id>',
            required=True,
            help="The subnet ID the member service is accessible from."
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip_address>',
            help="The IP address of the resource to add",
            #required=True
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_CHOICES) + '}',
            choices=PROTOCOL_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            #required=True,
            help="The protocol for the listener."
        )
        parser.add_argument(
            '--protocol-port',
            metavar='<port>',
            #required=True,
            type=int,
            help="Set the protocol port number for the listener."
        )
        return parser

    def take_action(self, parsed_args):
        rows = const.RESOURCE_ROWS
        attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                            parsed_args)

        validate.check_resource_attrs(attrs)

        if 'ip_address' not in attrs:
            subnet_id = attrs['subnet_id']
            subnet_info = self.app.client_manager.neutronclient.show_subnet(subnet_id)
            subnet_cidr = subnet_info['subnet']['cidr']
            attrs['ip_address'] = subnet_cidr

        body = {"resource": attrs}
        data = self.app.client_manager.vpn_server.resource_create(
            json=body)

        formatters = {'vpnservers': v2_utils.format_list,
                      'pools': v2_utils.format_list,
                      'allowed_cidrs': v2_utils.format_list_flat}

        return (rows,
                (utils.get_dict_properties(data['resource'],
                                           rows,
                                           formatters=formatters)))


class DeleteResource(command.Command):
    """Delete a resource"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'resource',
            metavar="<resource>",
            help="Resource to delete (name or ID)"
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                            parsed_args)

        resource_id = attrs.pop('resource_id')

        self.app.client_manager.vpn_server.resource_delete(
            resource_id=resource_id)


class ListResource(lister.Lister):
    """List resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List resources by resource name."
        )
        parser.add_argument(
            '--vpnserver',
            metavar='<vpnserver>',
            help="Filter by vpn server (name or ID).",
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="List resources by project ID."
        )
        return parser

    def take_action(self, parsed_args):
        columns = const.RESOURCE_COLUMNS
        attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.vpn_server.resource_list(**attrs)
        formatters = {'vpnservers': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['resources']))


class ShowResource(command.ShowOne):
    """Show the details of a single resource"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'resource',
            metavar='<resource>',
            help='Name or UUID of the resource'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.RESOURCE_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.resource):
            try:
                data = self.app.client_manager.vpn_server.resource_show(
                    resource_id=parsed_args.resource)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                                parsed_args)

            resource_id = attrs.pop('resource_id')

            data = self.app.client_manager.vpn_server.resource_show(
                resource_id=resource_id,
            )
        formatters = {'vpnservers': v2_utils.format_list,
                      'allowed_cidrs': v2_utils.format_list_flat}

        return rows, utils.get_dict_properties(data, rows,
                                               formatters=formatters)


class SetResource(command.Command):
    """Update a resource"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'resource',
            metavar="<resource>",
            help="Resource to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the resource name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this resource."
        )
        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                            parsed_args)

        resource_id = attrs.pop('resource_id')

        body = {'resource': attrs}

        self.app.client_manager.vpn_server.resource_set(
            resource_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.vpn_server.resource_show,
                res_id=resource_id
            )


class UnsetResource(command.Command):
    """Clear resource settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'resource',
            metavar="<resource>",
            help="Resource to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the resource name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the description of this resource."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        resource_id = v2_utils.get_resource_id(
            self.app.client_manager.vpn_server.resource_list,
            'resources', parsed_args.resource)

        body = {'resource': unset_args}

        self.app.client_manager.vpn_server.resource_set(
            resource_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.vpn_server.resource_show,
                res_id=resource_id
            )


class ShowResourceStats(command.ShowOne):
    """Shows the current statistics for a resource."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'resource',
            metavar='<resource>',
            help='Name or UUID of the resource'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_STATS_ROWS
        attrs = v2_utils.get_resource_attrs(self.app.client_manager,
                                            parsed_args)

        resource_id = attrs.pop('resource_id')

        data = self.app.client_manager.vpn_server.resource_stats_show(
            resource_id=resource_id,
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))
