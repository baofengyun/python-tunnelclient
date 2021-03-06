#   Copyright 2019 Red Hat, Inc. All rights reserved.
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
import copy
from unittest import mock

from osc_lib import exceptions

from tunnelclient.osc.v2 import constants
from tunnelclient.osc.v2 import pool as pool
from tunnelclient.tests.unit.osc.v2 import constants as attr_consts
from tunnelclient.tests.unit.osc.v2 import fakes


class TestPool(fakes.TestTunnelClient):

    def setUp(self):
        super().setUp()

        self._po = fakes.createFakeResource('pool')
        self.pool_info = copy.deepcopy(attr_consts.POOL_ATTRS)
        self.columns = copy.deepcopy(constants.POOL_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.pool_list.return_value = copy.deepcopy(
            {'pools': [attr_consts.POOL_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.vpn_server = self.api_mock


class TestPoolList(TestPool):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.POOL_ATTRS[k] for k in self.columns
        ),)
        self.cmd = pool.ListPool(self.app, None)

    def test_pool_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestPoolDelete(TestPool):

    def setUp(self):
        super().setUp()
        self.cmd = pool.DeletePool(self.app, None)

    def test_pool_delete(self):
        arglist = [self._po.id]
        verifylist = [
            ('pool', self._po.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_delete.assert_called_with(
            pool_id=self._po.id)

    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_pool_delete_wait(self, mock_wait):
        arglist = [self._po.id, '--wait']
        verifylist = [
            ('pool', self._po.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_delete.assert_called_with(
            pool_id=self._po.id)
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_listener_delete_failure(self):
        arglist = ['unknown_pool']
        verifylist = [
            ('pool', 'unknown_pool')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.pool_delete)


class TestPoolCreate(TestPool):

    def setUp(self):
        super().setUp()
        self.api_mock.pool_create.return_value = {
            'pool': self.pool_info}
        lb_client = self.app.client_manager
        lb_client.vpn_server = self.api_mock

        self.cmd = pool.CreatePool(self.app, None)

    @mock.patch('tunnelclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create(self, mock_attrs):
        mock_attrs.return_value = self.pool_info
        arglist = ['--vpnserver', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN',
                   '--enable-tls',
                   '--tls-container-ref', self._po.tls_container_ref,
                   '--ca-tls-container-ref', self._po.ca_tls_container_ref,
                   '--crl-container-ref', self._po.crl_container_ref,
                   '--tls-ciphers', self._po.tls_ciphers,
                   '--tls-version', self._po.tls_versions[0],
                   '--tls-version', self._po.tls_versions[1]]

        verifylist = [
            ('vpnserver', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('enable_tls', self._po.tls_enabled),
            ('tls_container_ref', self._po.tls_container_ref),
            ('ca_tls_container_ref', self._po.ca_tls_container_ref),
            ('crl_container_ref', self._po.crl_container_ref),
            ('tls_ciphers', self._po.tls_ciphers),
            ('tls_versions', self._po.tls_versions)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.pool_info})

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('tunnelclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create_wait(self, mock_attrs, mock_wait):
        self.pool_info['vpnservers'] = [{'id': 'mock_lb_id'}]
        mock_attrs.return_value = self.pool_info
        self.api_mock.pool_show.return_value = self.pool_info
        arglist = ['--vpnserver', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN',
                   '--wait']

        verifylist = [
            ('vpnserver', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.pool_info})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id='mock_lb_id',
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestPoolShow(TestPool):

    def setUp(self):
        super().setUp()
        self.api_mock.pool_show.return_value = self.pool_info
        lb_client = self.app.client_manager
        lb_client.vpn_server = self.api_mock

        self.cmd = pool.ShowPool(self.app, None)

    def test_pool_show(self,):
        arglist = [self._po.id]
        verifylist = [
            ('pool', self._po.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_show.assert_called_with(pool_id=self._po.id)


class TestPoolSet(TestPool):

    def setUp(self):
        super().setUp()
        self.cmd = pool.SetPool(self.app, None)

    def test_pool_set(self):
        new_tls_id, new_ca_id, new_crl_id = (
            'test-tls-container-id', 'test-ca-tls-container-id',
            'test-crl-container-id')
        arglist = [self._po.id, '--name', 'new_name', '--tls-container-ref',
                   new_tls_id, '--ca-tls-container-ref', new_ca_id,
                   '--crl-container-ref', new_crl_id, '--enable-tls',
                   '--tls-ciphers', self._po.tls_ciphers,
                   '--tls-version', self._po.tls_versions[0],
                   '--tls-version', self._po.tls_versions[1]]
        verifylist = [
            ('pool', self._po.id),
            ('name', 'new_name'),
            ('tls_ciphers', self._po.tls_ciphers),
            ('tls_versions', self._po.tls_versions)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_with(
            self._po.id, json={'pool': {'name': 'new_name',
                                        'tls_container_ref': new_tls_id,
                                        'ca_tls_container_ref': new_ca_id,
                                        'crl_container_ref': new_crl_id,
                                        'tls_enabled': True,
                                        'tls_ciphers': self._po.tls_ciphers,
                                        'tls_versions': self._po.tls_versions
                                        }})

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_pool_set_wait(self, mock_wait):
        arglist = [self._po.id, '--name', 'new_name', '--wait']
        verifylist = [
            ('pool', self._po.id),
            ('name', 'new_name'),
            ('wait', True),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_with(
            self._po.id, json={'pool': {'name': 'new_name'}})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestPoolUnset(TestPool):
    PARAMETERS = ('name', 'description', 'ca_tls_container_ref',
                  'crl_container_ref', 'session_persistence',
                  'tls_container_ref', 'tls_versions', 'tls_ciphers')

    def setUp(self):
        super().setUp()
        self.cmd = pool.UnsetPool(self.app, None)

    def test_pool_unset_name(self):
        self._test_pool_unset_param('name')

    def test_pool_unset_name_wait(self):
        self._test_pool_unset_param_wait('name')

    def test_pool_unset_description(self):
        self._test_pool_unset_param('description')

    def test_pool_unset_ca_tls_container_ref(self):
        self._test_pool_unset_param('ca_tls_container_ref')

    def test_pool_unset_crl_container_ref(self):
        self._test_pool_unset_param('crl_container_ref')

    def test_pool_unset_session_persistence(self):
        self._test_pool_unset_param('session_persistence')

    def test_pool_unset_tls_container_ref(self):
        self._test_pool_unset_param('tls_container_ref')

    def test_pool_unset_tls_versions(self):
        self._test_pool_unset_param('tls_versions')

    def test_pool_unset_tls_ciphers(self):
        self._test_pool_unset_param('tls_ciphers')

    def _test_pool_unset_param(self, param):
        self.api_mock.pool_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._po.id, '--%s' % arg_param]
        ref_body = {'pool': {param: None}}
        verifylist = [
            ('pool', self._po.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)

    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_pool_unset_param_wait(self, param, mock_wait):
        self.api_mock.pool_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._po.id, '--%s' % arg_param, '--wait']
        ref_body = {'pool': {param: None}}
        verifylist = [
            ('pool', self._po.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_pool_unset_all(self):
        self.api_mock.pool_set.reset_mock()
        ref_body = {'pool': {x: None for x in self.PARAMETERS}}
        arglist = [self._po.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('pool', self._po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)

    def test_pool_unset_none(self):
        self.api_mock.pool_set.reset_mock()
        arglist = [self._po.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('pool', self._po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_not_called()
