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

"""Secgroup action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from tunnelclient.osc.v2 import constants as const
from tunnelclient.osc.v2 import utils as v2_utils
from tunnelclient.osc.v2 import validate


class CreateSecgroup(command.ShowOne):
    """Create a secgroup"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpnserver>',
            help="Vpn server for the secgroup (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the secgroup name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this secgroup."
        )
        parser.add_argument(
            '--remote-ip',
            metavar='<ip-address>',
            help="The IP address to allow access.",
            required=True
        )
        return parser

    def take_action(self, parsed_args):
        rows = const.SECGROUP_ROWS
        attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                            parsed_args)

        validate.check_secgroup_attrs(attrs)

        body = {"secgroup": attrs}
        data = self.app.client_manager.vpn_server.secgroup_create(
            json=body)

        formatters = {'vpnservers': v2_utils.format_list,
                      'allowed_cidrs': v2_utils.format_list_flat}

        return (rows,
                (utils.get_dict_properties(data['secgroup'],
                                           rows,
                                           formatters=formatters)))


class DeleteSecgroup(command.Command):
    """Delete a secgroup"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'secgroup',
            metavar="<secgroup>",
            help="Secgroup to delete (name or ID)"
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                            parsed_args)

        secgroup_id = attrs.pop('secgroup_id')

        self.app.client_manager.vpn_server.secgroup_delete(
            secgroup_id=secgroup_id)


class ListSecgroup(lister.Lister):
    """List secgroups"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List secgroups by secgroup name."
        )
        parser.add_argument(
            '--vpnserver',
            metavar='<vpnserver>',
            help="Filter by vpn server (name or ID).",
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="List secgroups by project ID."
        )
        return parser

    def take_action(self, parsed_args):
        columns = const.SECGROUP_COLUMNS
        attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.vpn_server.secgroup_list(**attrs)
        formatters = {'vpnservers': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['secgroups']))


class ShowSecgroup(command.ShowOne):
    """Show the details of a single secgroup"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'secgroup',
            metavar='<secgroup>',
            help='Name or UUID of the secgroup'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.SECGROUP_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.secgroup):
            try:
                data = self.app.client_manager.vpn_server.secgroup_show(
                    secgroup_id=parsed_args.secgroup)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                                parsed_args)

            secgroup_id = attrs.pop('secgroup_id')

            data = self.app.client_manager.vpn_server.secgroup_show(
                secgroup_id=secgroup_id,
            )
        formatters = {'vpnservers': v2_utils.format_list,
                      'allowed_cidrs': v2_utils.format_list_flat}

        return rows, utils.get_dict_properties(data, rows,
                                               formatters=formatters)


class SetSecgroup(command.Command):
    """Update a secgroup"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'secgroup',
            metavar="<secgroup>",
            help="Secgroup to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the secgroup name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this secgroup."
        )
        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                            parsed_args)

        secgroup_id = attrs.pop('secgroup_id')

        body = {'secgroup': attrs}

        self.app.client_manager.vpn_server.secgroup_set(
            secgroup_id, json=body)


class UnsetSecgroup(command.Command):
    """Clear secgroup settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'secgroup',
            metavar="<secgroup>",
            help="Secgroup to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the secgroup name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the description of this secgroup."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        secgroup_id = v2_utils.get_resource_id(
            self.app.client_manager.vpn_server.secgroup_list,
            'secgroups', parsed_args.secgroup)

        body = {'secgroup': unset_args}

        self.app.client_manager.vpn_server.secgroup_set(
            secgroup_id, json=body)


class ShowSecgroupStats(command.ShowOne):
    """Shows the current statistics for a secgroup."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'secgroup',
            metavar='<secgroup>',
            help='Name or UUID of the secgroup'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_STATS_ROWS
        attrs = v2_utils.get_secgroup_attrs(self.app.client_manager,
                                            parsed_args)

        secgroup_id = attrs.pop('secgroup_id')

        data = self.app.client_manager.vpn_server.secgroup_stats_show(
            secgroup_id=secgroup_id,
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))
