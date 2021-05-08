# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""OpenStackClient plugin for Vpn Server service."""
import logging

from osc_lib import utils

from tunnelclient.api.v2 import tunnel

LOG = logging.getLogger(__name__)

DEFAULT_VPNSERVER_API_VERSION = '2.0'
API_VERSION_OPTION = 'os_vpnserver_api_version'
API_NAME = 'vpn_server'
VPN_SERVER_API_TYPE = 'vpnserver'
VPN_SERVER_API_VERSIONS = {
    '2.0': 'tunnelclient.api.v2.tunnel.TunnelAPI',
}


def make_client(instance):
    """Returns a vpn server service client"""
    endpoint = instance.get_endpoint_for_service_type(
        'vpn',
        region_name=instance.region_name,
        interface=instance.interface,
    )
    client = tunnel.TunnelAPI(
        session=instance.session,
        service_type='vpn',
        endpoint=endpoint,
    )
    return client


def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized. This is
    where a plugin can add global options such as an API version.

    :param argparse.ArgumentParser parser: The parser object that
        has been initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-vpnserver-api-version',
        metavar='<vpnserver-api-version>',
        default=utils.env(
            'OS_VPNSERVER_API_VERSION',
            default=DEFAULT_VPNSERVER_API_VERSION),
        help='OSC Plugin API version, default=' +
             DEFAULT_VPNSERVER_API_VERSION +
             ' (Env: OS_VPNSERVER_API_VERSION)')
    return parser
