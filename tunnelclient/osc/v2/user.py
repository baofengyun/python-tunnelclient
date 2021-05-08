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

"""User action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from tunnelclient.osc.v2 import constants as const
from tunnelclient.osc.v2 import utils as v2_utils
from tunnelclient.osc.v2 import validate


class CreateUser(command.ShowOne):
    """Create a user"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpnserver>',
            help="Vpn server for the user (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help="Set the user name."
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            required=True,
            help="Password of the user name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this user."
        )
        return parser

    def take_action(self, parsed_args):
        rows = const.USER_ROWS
        attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                            parsed_args)

        validate.check_user_attrs(attrs)

        body = {"user": attrs}
        data = self.app.client_manager.vpn_server.user_create(
            json=body)

        formatters = {'vpnservers': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(data['user'],
                                           rows,
                                           formatters=formatters)))


class DeleteUser(command.Command):
    """Delete a user"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'user',
            metavar="<user>",
            help="User to delete (name or ID)"
        )
        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                            parsed_args)

        user_id = attrs.pop('user_id')

        self.app.client_manager.vpn_server.user_delete(
            user_id=user_id)


class ListUser(lister.Lister):
    """List users"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List users by user name."
        )
        parser.add_argument(
            '--vpnserver',
            metavar='<vpnserver>',
            help="Filter by vpn server (name or ID).",
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="List users by project ID."
        )
        return parser

    def take_action(self, parsed_args):
        columns = const.USER_COLUMNS
        attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.vpn_server.user_list(**attrs)
        formatters = {'vpnservers': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['users']))


class ShowUser(command.ShowOne):
    """Show the details of a single user"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'user',
            metavar='<user>',
            help='Name or UUID of the user'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.USER_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.user):
            try:
                data = self.app.client_manager.vpn_server.user_show(
                    user_id=parsed_args.user)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                                parsed_args)

            user_id = attrs.pop('user_id')

            data = self.app.client_manager.vpn_server.user_show(
                user_id=user_id,
            )
        formatters = {'vpnservers': v2_utils.format_list}

        return rows, utils.get_dict_properties(data, rows,
                                               formatters=formatters)


class SetUser(command.Command):
    """Update a user"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'user',
            metavar="<user>",
            help="User to modify (name or ID)."
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            required=True,
            help="Password of the user name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this user."
        )
        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                            parsed_args)

        user_id = attrs.pop('user_id')

        body = {'user': attrs}

        self.app.client_manager.vpn_server.user_set(
            user_id, json=body)


class UnsetUser(command.Command):
    """Clear user settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'user',
            metavar="<user>",
            help="User to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the user name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the description of this user."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        user_id = v2_utils.get_resource_id(
            self.app.client_manager.vpn_server.user_list,
            'users', parsed_args.user)

        body = {'user': unset_args}

        self.app.client_manager.vpn_server.user_set(
            user_id, json=body)


class ShowUserStats(command.ShowOne):
    """Shows the current statistics for a user."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'user',
            metavar='<user>',
            help='Name or UUID of the user'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.VPN_SERVER_STATS_ROWS
        attrs = v2_utils.get_user_attrs(self.app.client_manager,
                                            parsed_args)

        user_id = attrs.pop('user_id')

        data = self.app.client_manager.vpn_server.user_stats_show(
            user_id=user_id,
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))
