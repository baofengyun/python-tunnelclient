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

"""Vpn Server v2 API Library Tests"""

from keystoneauth1 import session
from oslo_utils import uuidutils
from requests_mock.contrib import fixture

from osc_lib.tests import utils

from tunnelclient.api import exceptions
from tunnelclient.api.v2 import tunnel

FAKE_ACCOUNT = 'q12we34r'
FAKE_AUTH = '11223344556677889900'
FAKE_URL = 'http://example.com/v2.0/'
FAKE_VPNAAS_URL = FAKE_URL + 'vpnaas/'
FAKE_TUNNEL_URL = FAKE_URL + 'tunnel/'

FAKE_LB = uuidutils.generate_uuid()
FAKE_LI = uuidutils.generate_uuid()
FAKE_PO = uuidutils.generate_uuid()
FAKE_ME = uuidutils.generate_uuid()
FAKE_L7PO = uuidutils.generate_uuid()
FAKE_L7RU = uuidutils.generate_uuid()
FAKE_HM = uuidutils.generate_uuid()
FAKE_PRJ = uuidutils.generate_uuid()
FAKE_AMP = uuidutils.generate_uuid()
FAKE_PROVIDER = 'fake_provider'
FAKE_FV = uuidutils.generate_uuid()
FAKE_FVPF = uuidutils.generate_uuid()
FAKE_AZ = 'fake_az'
FAKE_AZPF = uuidutils.generate_uuid()


LIST_LB_RESP = {
    'vpnservers':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_LI_RESP = {
    'listeners':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_PO_RESP = {
    'pools':
        [{'name': 'po1'},
         {'name': 'po2'}]
}

LIST_ME_RESP = {
    'members':
        [{'name': 'mem1'},
         {'name': 'mem2'}]
}

LIST_L7PO_RESP = [
    {'name': 'l71'},
    {'name': 'l72'},
]

LIST_L7RU_RESP = {
    'rules':
        [{'id': uuidutils.generate_uuid()},
         {'id': uuidutils.generate_uuid()}]
}

LIST_HM_RESP = {
    'healthmonitors':
        [{'id': uuidutils.generate_uuid()},
         {'id': uuidutils.generate_uuid()}]
}

LIST_QT_RESP = {
    'quotas':
        [{'health_monitor': -1},
         {'listener': -1},
         {'vpn_server': 5},
         {'member': 10},
         {'pool': 20},
         {'project': uuidutils.generate_uuid()}]
}

LIST_AMP_RESP = {
    'amphorae':
        [{'id': uuidutils.generate_uuid()},
         {'id': uuidutils.generate_uuid()}]
}

LIST_PROVIDER_RESP = {
    'providers':
        [{'name': 'provider1', 'description': 'description of provider1'},
         {'name': 'provider2', 'description': 'description of provider2'}]
}

LIST_FV_RESP = {
    'flavors': [{'name': 'fv1'},
                {'name': 'fv2'}]
}

LIST_FVPF_RESP = {
    'flavorprofiles': [{'name': 'fvpf1'},
                       {'name': 'fvpf2'}]
}

LIST_AZ_RESP = {
    'availability_zones': [{'name': 'az1'},
                           {'name': 'az2'}]
}

LIST_AZPF_RESP = {
    'availability_zone_profiles': [{'name': 'azpf1'},
                                   {'name': 'azpf2'}]
}

SINGLE_LB_RESP = {'vpnserver': {'id': FAKE_LB, 'name': 'lb1'}}
SINGLE_LB_UPDATE = {"vpnserver": {"admin_state_up": False}}
SINGLE_LB_STATS_RESP = {'bytes_in': '0'}
SINGLE_LB_STATUS_RESP = {'statuses': {'operating_status': 'ONLINE',
                                      'provisioning_status': 'ACTIVE'}}

SINGLE_LI_RESP = {'listener': {'id': FAKE_LI, 'name': 'li1'}}
SINGLE_LI_UPDATE = {"listener": {"admin_state_up": False}}

SINGLE_PO_RESP = {'pool': {'id': FAKE_PO, 'name': 'li1'}}
SINGLE_PO_UPDATE = {'pool': {'admin_state_up': False}}

SINGLE_L7PO_RESP = {'l7policy': {'id': FAKE_L7PO, 'name': 'l71'}}
SINGLE_L7PO_UPDATE = {'l7policy': {'admin_state_up': False}}

SINGLE_ME_RESP = {'member': {'id': FAKE_ME, 'name': 'mem1'}}
SINGLE_ME_UPDATE = {"member": {"admin_state_up": False}}

SINGLE_L7RU_RESP = {'rule': {'id': FAKE_L7RU}}
SINGLE_L7RU_UPDATE = {'rule': {'admin_state_up': False}}

SINGLE_HM_RESP = {'healthmonitor': {'id': FAKE_ME}}
SINGLE_HM_UPDATE = {'healthmonitor': {'admin_state_up': False}}

SINGLE_QT_RESP = {'quota': {'pool': -1}}
SINGLE_QT_UPDATE = {'quota': {'pool': -1}}
SINGLB_AMP_RESP = {'amphora': {'id': FAKE_AMP}}
SINGLE_AMP_STATS_RESP = {'bytes_in': '0'}

SINGLE_PROVIDER_CAPABILITY_RESP = {
    'flavor_capabilities':
    [{'some_capability': 'Capabilicy description'}]
}

SINGLE_FV_RESP = {'flavor': {'id': FAKE_FV, 'name': 'fv1'}}
SINGLE_FV_UPDATE = {'flavor': {'enabled': False}}

SINGLE_FVPF_RESP = {'flavorprofile': {'id': FAKE_FVPF, 'name': 'fvpf1'}}
SINGLE_FVPF_UPDATE = {'flavorprofile': {'provider_name': 'fake_provider'}}

SINGLE_AZ_RESP = {'availability_zone': {'name': FAKE_AZ}}
SINGLE_AZ_UPDATE = {'availability_zone': {'enabled': False}}

SINGLE_AZPF_RESP = {'availability_zone_profile': {'id': FAKE_AZPF,
                                                  'name': 'azpf1'}}
SINGLE_AZPF_UPDATE = {'availability_zone_profile': {
    'provider_name': 'fake_provider'}}


class TestAPI(utils.TestCase):
    def test_client_exception(self):
        self.assertIs(tunnel.TunnelClientException,
                      exceptions.TunnelClientException)


class TestTunnelClient(utils.TestCase):

    def setUp(self):
        super().setUp()
        sess = session.Session()
        self.api = tunnel.TunnelAPI(session=sess, endpoint=FAKE_URL)
        self.requests_mock = self.useFixture(fixture.Fixture())


class TestVpnServer(TestTunnelClient):

    _error_message = ("Validation failure: Test message.")

    def test_list_vpn_server_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'vpnservers',
            json=LIST_LB_RESP,
            status_code=200,
        )
        ret = self.api.vpn_server_list()
        self.assertEqual(LIST_LB_RESP, ret)

    def test_show_vpn_server(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB,
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.vpn_server_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_RESP['vpnserver'], ret)

    def test_create_vpn_server(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'vpnservers',
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.vpn_server_create(json=SINGLE_LB_RESP)
        self.assertEqual(SINGLE_LB_RESP, ret)

    def test_create_vpn_server_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'vpnservers',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.vpn_server_create,
                               json=SINGLE_LB_RESP)

    def test_create_vpn_server_503_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'vpnservers',
            status_code=503
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               'Service Unavailable',
                               self.api.vpn_server_create,
                               json=SINGLE_LB_RESP)

    def test_set_vpn_server(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB,
            json=SINGLE_LB_UPDATE,
            status_code=200
        )
        ret = self.api.vpn_server_set(FAKE_LB, json=SINGLE_LB_UPDATE)
        self.assertEqual(SINGLE_LB_UPDATE, ret)

    def test_set_vpn_server_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.vpn_server_set,
                               FAKE_LB,
                               json=SINGLE_LB_UPDATE)

    def test_failover_vpn_server(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB + '/failover',
            status_code=202,
        )
        ret = self.api.vpn_server_failover(FAKE_LB)
        self.assertEqual(202, ret.status_code)

    def test_failover_vpn_server_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB + '/failover',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=409,
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.vpn_server_failover,
                               FAKE_LB)

    def test_delete_vpn_server(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB,
            status_code=200
        )
        ret = self.api.vpn_server_delete(FAKE_LB)
        self.assertEqual(200, ret.status_code)

    def test_delete_vpn_server_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.vpn_server_delete,
                               FAKE_LB)

    def test_stats_show_vpn_server(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB + '/stats',
            json=SINGLE_LB_STATS_RESP,
            status_code=200,
        )
        ret = self.api.vpn_server_stats_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_STATS_RESP, ret)

    def test_status_show_vpn_server(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'vpnservers/' + FAKE_LB + '/status',
            json=SINGLE_LB_STATUS_RESP,
            status_code=200,
        )
        ret = self.api.vpn_server_status_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_STATUS_RESP, ret)

    def test_list_listeners_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'listeners',
            json=LIST_LI_RESP,
            status_code=200,
        )
        ret = self.api.listener_list()
        self.assertEqual(LIST_LI_RESP, ret)

    def test_show_listener(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_show(FAKE_LI)
        self.assertEqual(SINGLE_LI_RESP['listener'], ret)

    def test_create_listener(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'listeners',
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_create(json=SINGLE_LI_RESP)
        self.assertEqual(SINGLE_LI_RESP, ret)

    def test_create_listener_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'listeners',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.listener_create,
                               json=SINGLE_LI_RESP)

    def test_set_listeners(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_UPDATE,
            status_code=200
        )
        ret = self.api.listener_set(FAKE_LI, json=SINGLE_LI_UPDATE)
        self.assertEqual(SINGLE_LI_UPDATE, ret)

    def test_set_listeners_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.listener_set,
                               FAKE_LI, json=SINGLE_LI_UPDATE)

    def test_delete_listener(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI,
            status_code=200
        )
        ret = self.api.listener_delete(FAKE_LI)
        self.assertEqual(200, ret.status_code)

    def test_delete_listener_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.listener_delete,
                               FAKE_LI)

    def test_stats_show_listener(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'listeners/' + FAKE_LI + '/stats',
            json=SINGLE_LB_STATS_RESP,
            status_code=200,
        )
        ret = self.api.listener_stats_show(FAKE_LI)
        self.assertEqual(SINGLE_LB_STATS_RESP, ret)

    def test_list_pool_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'pools',
            json=LIST_PO_RESP,
            status_code=200,
        )
        ret = self.api.pool_list()
        self.assertEqual(LIST_PO_RESP, ret)

    def test_show_pool(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_show(FAKE_PO)
        self.assertEqual(SINGLE_PO_RESP['pool'], ret)

    def test_create_pool(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'pools',
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_create(json=SINGLE_PO_RESP)
        self.assertEqual(SINGLE_PO_RESP, ret)

    def test_create_pool_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'pools',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.pool_create,
                               json=SINGLE_PO_RESP)

    def test_set_pool(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_UPDATE,
            status_code=200
        )
        ret = self.api.pool_set(FAKE_PO, json=SINGLE_PO_UPDATE)
        self.assertEqual(SINGLE_PO_UPDATE, ret)

    def test_set_pool_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.pool_set,
                               FAKE_PO, json=SINGLE_PO_UPDATE)

    def test_delete_pool(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO,
            status_code=200
        )
        ret = self.api.pool_delete(FAKE_PO)
        self.assertEqual(200, ret.status_code)

    def test_delete_pool_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.pool_delete,
                               FAKE_PO)

    def test_list_member_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members',
            json=LIST_ME_RESP,
            status_code=200,
        )
        ret = self.api.member_list(FAKE_PO)
        self.assertEqual(LIST_ME_RESP, ret)

    def test_show_member(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            json=SINGLE_ME_RESP,
            status_code=200
        )
        ret = self.api.member_show(pool_id=FAKE_PO, member_id=FAKE_ME)
        self.assertEqual(SINGLE_ME_RESP['member'], ret)

    def test_create_member(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members',
            json=SINGLE_ME_RESP,
            status_code=200
        )
        ret = self.api.member_create(json=SINGLE_ME_RESP, pool_id=FAKE_PO)
        self.assertEqual(SINGLE_ME_RESP, ret)

    def test_create_member_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.member_create,
                               json=SINGLE_ME_RESP, pool_id=FAKE_PO)

    def test_set_member(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            json=SINGLE_ME_UPDATE,
            status_code=200
        )
        ret = self.api.member_set(pool_id=FAKE_PO, member_id=FAKE_ME,
                                  json=SINGLE_ME_UPDATE)
        self.assertEqual(SINGLE_ME_UPDATE, ret)

    def test_set_member_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.member_set,
                               pool_id=FAKE_PO, member_id=FAKE_ME,
                               json=SINGLE_ME_UPDATE)

    def test_delete_member(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            status_code=200
        )
        ret = self.api.member_delete(pool_id=FAKE_PO, member_id=FAKE_ME)
        self.assertEqual(200, ret.status_code)

    def test_delete_member_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.member_delete,
                               pool_id=FAKE_PO, member_id=FAKE_ME)

    def test_list_l7policy_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'l7policies',
            json=LIST_L7PO_RESP,
            status_code=200,
        )
        ret = self.api.l7policy_list()
        self.assertEqual(LIST_L7PO_RESP, ret)

    def test_show_l7policy(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO,
            json=SINGLE_L7PO_RESP,
            status_code=200
        )
        ret = self.api.l7policy_show(FAKE_L7PO)
        self.assertEqual(SINGLE_L7PO_RESP['l7policy'], ret)

    def test_create_l7policy(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'l7policies',
            json=SINGLE_L7PO_RESP,
            status_code=200
        )
        ret = self.api.l7policy_create(json=SINGLE_L7PO_RESP)
        self.assertEqual(SINGLE_L7PO_RESP, ret)

    def test_create_l7policy_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'l7policies',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7policy_create,
                               json=SINGLE_L7PO_RESP)

    def test_set_l7policy(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO,
            json=SINGLE_L7PO_UPDATE,
            status_code=200
        )
        ret = self.api.l7policy_set(FAKE_L7PO, json=SINGLE_L7PO_UPDATE)
        self.assertEqual(SINGLE_L7PO_UPDATE, ret)

    def test_set_l7policy_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7policy_set,
                               FAKE_L7PO, json=SINGLE_L7PO_UPDATE)

    def test_delete_l7policy(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO,
            status_code=200
        )
        ret = self.api.l7policy_delete(FAKE_L7PO)
        self.assertEqual(200, ret.status_code)

    def test_delete_l7policy_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7policy_delete,
                               FAKE_L7PO)

    def test_list_l7rule_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            json=LIST_L7RU_RESP,
            status_code=200,
        )
        ret = self.api.l7rule_list(FAKE_L7PO)
        self.assertEqual(LIST_L7RU_RESP, ret)

    def test_show_l7rule(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            json=SINGLE_L7RU_RESP,
            status_code=200
        )
        ret = self.api.l7rule_show(FAKE_L7RU, FAKE_L7PO)
        self.assertEqual(SINGLE_L7RU_RESP['rule'], ret)

    def test_create_l7rule(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            json=SINGLE_L7RU_RESP,
            status_code=200
        )
        ret = self.api.l7rule_create(FAKE_L7PO, json=SINGLE_L7RU_RESP)
        self.assertEqual(SINGLE_L7RU_RESP, ret)

    def test_create_l7rule_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7rule_create,
                               FAKE_L7PO, json=SINGLE_L7RU_RESP)

    def test_set_l7rule(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            json=SINGLE_L7RU_UPDATE,
            status_code=200
        )
        ret = self.api.l7rule_set(
            l7rule_id=FAKE_L7RU,
            l7policy_id=FAKE_L7PO,
            json=SINGLE_L7RU_UPDATE
        )
        self.assertEqual(SINGLE_L7RU_UPDATE, ret)

    def test_set_l7rule_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7rule_set,
                               l7rule_id=FAKE_L7RU,
                               l7policy_id=FAKE_L7PO,
                               json=SINGLE_L7RU_UPDATE)

    def test_delete_l7rule(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            status_code=200
        )
        ret = self.api.l7rule_delete(
            l7rule_id=FAKE_L7RU,
            l7policy_id=FAKE_L7PO
        )
        self.assertEqual(200, ret.status_code)

    def test_delete_l7rule_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.l7rule_delete,
                               l7rule_id=FAKE_L7RU,
                               l7policy_id=FAKE_L7PO)

    def test_list_health_monitor_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'healthmonitors',
            json=LIST_HM_RESP,
            status_code=200,
        )
        ret = self.api.health_monitor_list()
        self.assertEqual(LIST_HM_RESP, ret)

    def test_show_health_monitor(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'healthmonitors/' + FAKE_HM,
            json=SINGLE_HM_RESP,
            status_code=200
        )
        ret = self.api.health_monitor_show(FAKE_HM)
        self.assertEqual(SINGLE_HM_RESP['healthmonitor'], ret)

    def test_create_health_monitor(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'healthmonitors',
            json=SINGLE_HM_RESP,
            status_code=200
        )
        ret = self.api.health_monitor_create(json=SINGLE_HM_RESP)
        self.assertEqual(SINGLE_HM_RESP, ret)

    def test_create_health_monitor_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'healthmonitors',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.health_monitor_create,
                               json=SINGLE_HM_RESP)

    def test_set_health_monitor(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'healthmonitors/' + FAKE_HM,
            json=SINGLE_HM_UPDATE,
            status_code=200
        )
        ret = self.api.health_monitor_set(FAKE_HM, json=SINGLE_HM_UPDATE)
        self.assertEqual(SINGLE_HM_UPDATE, ret)

    def test_set_health_monitor_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'healthmonitors/' + FAKE_HM,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.health_monitor_set,
                               FAKE_HM, json=SINGLE_HM_UPDATE)

    def test_delete_health_monitor(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'healthmonitors/' + FAKE_HM,
            status_code=200
        )
        ret = self.api.health_monitor_delete(FAKE_HM)
        self.assertEqual(200, ret.status_code)

    def test_delete_health_monitor_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'healthmonitors/' + FAKE_HM,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.health_monitor_delete,
                               FAKE_HM)

    def test_list_quota_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'quotas',
            json=LIST_QT_RESP,
            status_code=200,
        )
        ret = self.api.quota_list()
        self.assertEqual(LIST_QT_RESP, ret)

    def test_show_quota(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'quotas/' + FAKE_PRJ,
            json=SINGLE_QT_RESP,
            status_code=200
        )
        ret = self.api.quota_show(FAKE_PRJ)
        self.assertEqual(SINGLE_QT_RESP['quota'], ret)

    def test_set_quota(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'quotas/' + FAKE_PRJ,
            json=SINGLE_QT_UPDATE,
            status_code=200
        )
        ret = self.api.quota_set(FAKE_PRJ, json=SINGLE_QT_UPDATE)
        self.assertEqual(SINGLE_QT_UPDATE, ret)

    def test_set_quota_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'quotas/' + FAKE_PRJ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.quota_set,
                               FAKE_PRJ, json=SINGLE_QT_UPDATE)

    def test_reset_quota(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'quotas/' + FAKE_PRJ,
            status_code=200
        )
        ret = self.api.quota_reset(FAKE_PRJ)
        self.assertEqual(200, ret.status_code)

    def test_reset_quota_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'quotas/' + FAKE_PRJ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.quota_reset,
                               FAKE_PRJ)

    def test_list_amphora_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_TUNNEL_URL + 'amphorae?',
            json=LIST_AMP_RESP,
            status_code=200,
        )
        ret = self.api.amphora_list()
        self.assertEqual(LIST_AMP_RESP, ret)

    def test_show_amphora(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP,
            json=SINGLB_AMP_RESP,
            status_code=200
        )
        ret = self.api.amphora_show(FAKE_AMP)
        self.assertEqual(SINGLB_AMP_RESP['amphora'], ret)

    def test_configure_amphora(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP + '/config',
            status_code=202,
        )
        ret = self.api.amphora_configure(FAKE_AMP)
        self.assertEqual(202, ret.status_code)

    def test_configure_amphora_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP + '/config',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=409,
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.amphora_configure,
                               FAKE_AMP)

    def test_delete_amphora(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP,
            status_code=200
        )
        ret = self.api.amphora_delete(FAKE_AMP)
        self.assertEqual(200, ret.status_code)

    def test_stats_show_amphora(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP + '/stats',
            json=SINGLE_AMP_STATS_RESP,
            status_code=200
        )
        ret = self.api.amphora_stats_show(FAKE_AMP)
        self.assertEqual(SINGLE_AMP_STATS_RESP, ret)

    def test_failover_amphora(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP + '/failover',
            status_code=202,
        )
        ret = self.api.amphora_failover(FAKE_AMP)
        self.assertEqual(202, ret.status_code)

    def test_failover_amphora_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_TUNNEL_URL + 'amphorae/' + FAKE_AMP + '/failover',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=409,
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.amphora_failover,
                               FAKE_AMP)

    def test_list_provider(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'providers',
            json=LIST_PROVIDER_RESP,
            status_code=200,
        )
        ret = self.api.provider_list()
        self.assertEqual(LIST_PROVIDER_RESP, ret)

    def test_show_provider_capability(self):
        self.requests_mock.register_uri(
            'GET',
            (FAKE_VPNAAS_URL + 'providers/' +
             FAKE_PROVIDER + '/flavor_capabilities'),
            json=SINGLE_PROVIDER_CAPABILITY_RESP,
            status_code=200
        )
        ret = self.api.provider_flavor_capability_list(FAKE_PROVIDER)
        self.assertEqual(
            SINGLE_PROVIDER_CAPABILITY_RESP, ret)

    def test_list_flavor_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'flavors',
            json=LIST_FV_RESP,
            status_code=200,
        )
        ret = self.api.flavor_list()
        self.assertEqual(LIST_FV_RESP, ret)

    def test_show_flavor(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'flavors/' + FAKE_FV,
            json=SINGLE_FV_RESP,
            status_code=200
        )
        ret = self.api.flavor_show(FAKE_FV)
        self.assertEqual(SINGLE_FV_RESP['flavor'], ret)

    def test_create_flavor(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'flavors',
            json=SINGLE_FV_RESP,
            status_code=200
        )
        ret = self.api.flavor_create(json=SINGLE_FV_RESP)
        self.assertEqual(SINGLE_FV_RESP, ret)

    def test_create_flavor_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'flavors',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavor_create,
                               json=SINGLE_FV_RESP)

    def test_set_flavor(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'flavors/' + FAKE_FV,
            json=SINGLE_FV_UPDATE,
            status_code=200
        )
        ret = self.api.flavor_set(FAKE_FV, json=SINGLE_FV_UPDATE)
        self.assertEqual(SINGLE_FV_UPDATE, ret)

    def test_set_flavor_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'flavors/' + FAKE_FV,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavor_set,
                               FAKE_FV,
                               json=SINGLE_FV_UPDATE)

    def test_delete_flavor(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'flavors/' + FAKE_FV,
            status_code=200
        )
        ret = self.api.flavor_delete(FAKE_FV)
        self.assertEqual(200, ret.status_code)

    def test_delete_flavor_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'flavors/' + FAKE_FV,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavor_delete,
                               FAKE_FV)

    def test_list_flavorprofiles_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'flavorprofiles',
            json=LIST_FVPF_RESP,
            status_code=200,
        )
        ret = self.api.flavorprofile_list()
        self.assertEqual(LIST_FVPF_RESP, ret)

    def test_show_flavorprofile(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'flavorprofiles/' + FAKE_FVPF,
            json=SINGLE_FVPF_RESP,
            status_code=200
        )
        ret = self.api.flavorprofile_show(FAKE_FVPF)
        self.assertEqual(SINGLE_FVPF_RESP['flavorprofile'], ret)

    def test_create_flavorprofile(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'flavorprofiles',
            json=SINGLE_FVPF_RESP,
            status_code=200
        )
        ret = self.api.flavorprofile_create(json=SINGLE_FVPF_RESP)
        self.assertEqual(SINGLE_FVPF_RESP, ret)

    def test_create_flavorprofile_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'flavorprofiles',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavorprofile_create,
                               json=SINGLE_FVPF_RESP)

    def test_set_flavorprofiles(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'flavorprofiles/' + FAKE_FVPF,
            json=SINGLE_FVPF_UPDATE,
            status_code=200
        )
        ret = self.api.flavorprofile_set(FAKE_FVPF, json=SINGLE_FVPF_UPDATE)
        self.assertEqual(SINGLE_FVPF_UPDATE, ret)

    def test_set_flavorprofiles_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'flavorprofiles/' + FAKE_FVPF,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavorprofile_set,
                               FAKE_FVPF, json=SINGLE_FVPF_UPDATE)

    def test_delete_flavorprofile(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'flavorprofiles/' + FAKE_FVPF,
            status_code=200
        )
        ret = self.api.flavorprofile_delete(FAKE_FVPF)
        self.assertEqual(200, ret.status_code)

    def test_delete_flavorprofile_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'flavorprofiles/' + FAKE_FVPF,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.flavorprofile_delete,
                               FAKE_FVPF)

    def test_list_availabilityzone_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'availabilityzones',
            json=LIST_AZ_RESP,
            status_code=200,
        )
        ret = self.api.availabilityzone_list()
        self.assertEqual(LIST_AZ_RESP, ret)

    def test_show_availabilityzone(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'availabilityzones/' + FAKE_AZ,
            json=SINGLE_AZ_RESP,
            status_code=200
        )
        ret = self.api.availabilityzone_show(FAKE_AZ)
        self.assertEqual(SINGLE_AZ_RESP['availability_zone'], ret)

    def test_create_availabilityzone(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'availabilityzones',
            json=SINGLE_AZ_RESP,
            status_code=200
        )
        ret = self.api.availabilityzone_create(json=SINGLE_AZ_RESP)
        self.assertEqual(SINGLE_AZ_RESP, ret)

    def test_create_availabilityzone_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'availabilityzones',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzone_create,
                               json=SINGLE_AZ_RESP)

    def test_set_availabilityzone(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'availabilityzones/' + FAKE_AZ,
            json=SINGLE_AZ_UPDATE,
            status_code=200
        )
        ret = self.api.availabilityzone_set(FAKE_AZ, json=SINGLE_AZ_UPDATE)
        self.assertEqual(SINGLE_AZ_UPDATE, ret)

    def test_set_availabilityzone_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'availabilityzones/' + FAKE_AZ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzone_set,
                               FAKE_AZ,
                               json=SINGLE_AZ_UPDATE)

    def test_delete_availabilityzone(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'availabilityzones/' + FAKE_AZ,
            status_code=200
        )
        ret = self.api.availabilityzone_delete(FAKE_AZ)
        self.assertEqual(200, ret.status_code)

    def test_delete_availabilityzone_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'availabilityzones/' + FAKE_AZ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzone_delete,
                               FAKE_AZ)

    def test_list_availabilityzoneprofiles_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles',
            json=LIST_AZPF_RESP,
            status_code=200,
        )
        ret = self.api.availabilityzoneprofile_list()
        self.assertEqual(LIST_AZPF_RESP, ret)

    def test_show_availabilityzoneprofile(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles/' + FAKE_AZPF,
            json=SINGLE_AZPF_RESP,
            status_code=200
        )
        ret = self.api.availabilityzoneprofile_show(FAKE_AZPF)
        self.assertEqual(SINGLE_AZPF_RESP['availability_zone_profile'], ret)

    def test_create_availabilityzoneprofile(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles',
            json=SINGLE_AZPF_RESP,
            status_code=200
        )
        ret = self.api.availabilityzoneprofile_create(json=SINGLE_AZPF_RESP)
        self.assertEqual(SINGLE_AZPF_RESP, ret)

    def test_create_availabilityzoneprofile_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzoneprofile_create,
                               json=SINGLE_AZPF_RESP)

    def test_set_availabilityzoneprofiles(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles/' + FAKE_AZPF,
            json=SINGLE_AZPF_UPDATE,
            status_code=200
        )
        ret = self.api.availabilityzoneprofile_set(FAKE_AZPF,
                                                   json=SINGLE_AZPF_UPDATE)
        self.assertEqual(SINGLE_AZPF_UPDATE, ret)

    def test_set_availabilityzoneprofiles_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles/' + FAKE_AZPF,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzoneprofile_set,
                               FAKE_AZPF, json=SINGLE_AZPF_UPDATE)

    def test_delete_availabilityzoneprofile(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles/' + FAKE_AZPF,
            status_code=200
        )
        ret = self.api.availabilityzoneprofile_delete(FAKE_AZPF)
        self.assertEqual(200, ret.status_code)

    def test_delete_availabilityzoneprofile_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_VPNAAS_URL + 'availabilityzoneprofiles/' + FAKE_AZPF,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(exceptions.TunnelClientException,
                               self._error_message,
                               self.api.availabilityzoneprofile_delete,
                               FAKE_AZPF)
