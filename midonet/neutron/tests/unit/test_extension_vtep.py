# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import mock
from webob import exc

from neutron.openstack.common import uuidutils
from neutron.tests.unit import test_api_v2
from neutron.tests.unit import test_api_v2_extension

from midonet.neutron.extensions import vtep

_uuid = uuidutils.generate_uuid
_get_path = test_api_v2._get_path


class VtepExtensionTestCase(test_api_v2_extension.ExtensionTestCase):
    """Test the endpoints for the vtep extension."""

    fmt = 'json'

    def setUp(self):
        super(VtepExtensionTestCase, self).setUp()
        plural_mappings = {'vtep': 'vteps'}
        self._setUpExtension(
            'midonet.neutron.extensions.vtep.VtepPluginBase',
            None, vtep.RESOURCE_ATTRIBUTE_MAP,
            vtep.Vtep, '', plural_mappings=plural_mappings)

    def test_vtep_list(self):
        return_value = [{'mgmt_ip': "1.1.1.1",
                         'name': 'dummy_vtep',
                         'tunnel_zone_id': _uuid()}]
        instance = self.plugin.return_value
        instance.get_vteps.return_value = return_value

        res = self.api.get(_get_path('vteps', fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        instance.get_vteps.assert_called_once_with(
            mock.ANY, fields=mock.ANY, filters=mock.ANY)
        res = self.deserialize(res)
        self.assertIn('vteps', res)
        self.assertEqual(1, len(res['vteps']))

    def test_vtep_show(self):
        vtep_ip = '1.1.1.1'
        return_value = {'mgmt_ip': vtep_ip,
                        'name': 'dummy_vtep',
                        'tunnel_zone_id': _uuid()}

        instance = self.plugin.return_value
        instance.get_vtep.return_value = return_value
        res = self.api.get(_get_path('vteps/%s' % vtep_ip, fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        instance.get_vtep.assert_called_once_with(
            mock.ANY, vtep_ip, fields=mock.ANY)
        res = self.deserialize(res)
        self.assertIn('vtep', res)

    def test_vtep_create(self):
        vtep_ip = '1.1.1.1'
        data = {'vtep': {'mgmt_ip': vtep_ip,
                         'mgmt_port': 4,
                         'description': "bank holiday",
                         'tenant_id': _uuid(),
                         'name': 'dummy_vtep',
                         'connection_state': "DISCONNECTED",
                         'tunnel_ip_addrs': None,
                         'tunnel_zone_id': _uuid()}}
        return_value = copy.deepcopy(data['vtep'])
        instance = self.plugin.return_value
        instance.create_vtep.return_value = return_value
        res = self.api.post(_get_path('vteps', fmt=self.fmt),
                            self.serialize(data),
                            content_type='application/%s' % self.fmt)
        instance.create_vtep.assert_called_once_with(mock.ANY, vtep=mock.ANY)
        self.assertEqual(exc.HTTPCreated.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('vtep', res)
        self.assertIn(vtep_ip, res['vtep']['mgmt_ip'])


class VtepExtensionTestCaseXml(VtepExtensionTestCase):
    fmt = 'xml'


class VtepBindingExtensionTestCase(test_api_v2_extension.ExtensionTestCase):
    """Test the endpoints for the vtep binding extension."""

    fmt = 'json'

    def setUp(self):
        super(VtepExtensionTestCase, self).setUp()
        plural_mappings = {'binding': 'bindings'}
        self._setUpExtension(
            'midonet.neutron.extensions.vtep.VtepBindingPluginBase',
            None, vtep.RESOURCE_ATTRIBUTE_MAP,
            vtep.Vtep, '', plural_mappings=plural_mappings)

    def test_vtep_binding_show(self):
        mgmt_ip = '1.1.1.1'
        vlan_id = 5
        port_name = 'steve'
        reqstr = "%s_%s" % (port_name, vlan_id)
        return_value = {'mgmt_ip': mgmt_ip,
                        'port_name': port_name,
                        'vlan_id': vlan_id,
                        'network_id': _uuid()}

        instance = self.plugin.return_value
        instance.get_vtep_binding.return_value = return_value

        res = self.api.get(_get_path(
            'vteps/%s/bindings/%s' % (mgmt_ip, reqstr),
            fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('binding', res)

    def test_vtep_binding_list(self):
        mgmt_ip = '1.1.1.1'
        vlan_id = 5
        port_name = 'steve'
        return_value = [{'mgmt_ip': mgmt_ip,
                         'port_name': port_name,
                         'vlan_id': vlan_id,
                         'network_id': _uuid()}]

        instance = self.plugin.return_value
        instance.get_vtep_bindings.return_value = return_value

        res = self.api.get(
            _get_path('vteps/%s/bindings' % mgmt_ip, fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('bindings', res)
        self.assertEqual(1, len(res['bindings']))

    def test_vtep_create(self):
        vtep_ip = '1.1.1.1'
        data = {'vtep': {'mgmt_ip': vtep_ip,
                         'mgmt_port': 4,
                         'description': "bank holiday",
                         'tenant_id': _uuid(),
                         'name': 'dummy_vtep',
                         'connection_state': "DISCONNECTED",
                         'tunnel_ip_addrs': None,
                         'tunnel_zone_id': _uuid()}}
        return_value = copy.deepcopy(data['vtep'])
        instance = self.plugin.return_value
        instance.create_vtep.return_value = return_value
        res = self.api.post(_get_path('vteps', fmt=self.fmt),
                            self.serialize(data),
                            content_type='application/%s' % self.fmt)
        instance.create_vtep.assert_called_once_with(mock.ANY, vtep=mock.ANY)
        self.assertEqual(exc.HTTPCreated.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('vtep', res)
        self.assertIn(vtep_ip, res['vtep']['mgmt_ip'])


class VtepBindingExtensionTestCaseXml(VtepBindingExtensionTestCase):
    fmt = 'xml'


class VtepVxlanBindingExtensionTestCase(
        test_api_v2_extension.ExtensionTestCase):

    def setUp(self):
        super(VtepExtensionTestCase, self).setUp()
        plural_mappings = {'binding': 'bindings'}
        self._setUpExtension(
            'midonet.neutron.extensions.vtep.VtepVxlanBindingPluginBase',
            None, vtep.RESOURCE_ATTRIBUTE_MAP,
            vtep.Vtep, '', plural_mappings=plural_mappings)

    def test_vtep_binding_show(self):
        port_id = _uuid()
        mgmt_ip = "1.1.1.1"
        vlan_id = 5
        port_name = 'steve'
        reqstr = "%s_%s" % (port_name, vlan_id)
        return_value = {'mgmt_ip': mgmt_ip,
                        'port_name': port_name,
                        'vlan_id': vlan_id,
                        'network_id': _uuid()}
        instance = self.plugin.return_value
        instance.get_vtep_vxlan.return_value = return_value

        res = self.api.get(_get_path(
            'vteps/%s/bindings/%s' % (port_id, reqstr),
            fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)

        res = self.deserialize(res)
        self.assertIn('binding', res)

    def test_vtep_binding_list(self):
        mgmt_ip = '1.1.1.1'
        vlan_id = 5
        port_name = 'steve'
        return_value = [{'mgmt_ip': mgmt_ip,
                         'port_name': port_name,
                         'vlan_id': vlan_id,
                         'network_id': _uuid()}]
        instance = self.plugin.return_value
        instance.get_vtep_vxlans.return_value = return_value

        res = self.api.get(
            _get_path('vteps/%s/bindings' % mgmt_ip, fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('bindings', res)
        self.assertEqual(1, len(res['bindings']))

    def test_vtep_binding_create(self):
        mgmt_ip = '1.1.1.1'
        vlan_id = 5
        port_name = 'steve'
        data = {'binding': {'mgmt_ip': mgmt_ip,
                            'port_name': port_name,
                            'vlan_id': vlan_id,
                            'network_id': _uuid()}}
        return_value = data['binding']
        instance = self.plugin.return_value
        instance.create_vtep_port_binding.return_value = return_value

        res = self.api.post(
            _get_path('vteps/%s/bindings' % mgmt_ip, fmt=self.fmt),
            self.serialize(data),
            content_type='application/%s' % self.fmt)
        self.assertEqual(exc.HTTPCreated.code, res.status_int)
        res = self.deserialize(res)
        self.assertIn('binding', res)
        self.assertEqual(res['binding'], return_value)

    def test_vtep_binding_delete(self):
        mgmt_ip = '1.1.1.1'
        vlan_id = 5
        port_name = 'steve'
        reqstr = "%s_%s" % (port_name, vlan_id)
        instance = self.plugin.return_value

        res = self.api.delete(_get_path(
            'vteps/%s/bindings/%s' % (vlan_id, reqstr), fmt=self.fmt))
        self.assertEqual(exc.HTTPNocontent.code, res.status_int)
        instance.delete_vtep_port_binding.assert_called_once_with(
            mock.ANY, reqstr, vtep_id=mgmt_ip)


class VtepVxlanBindingExtensionTestCaseXml(VtepVxlanBindingExtensionTestCase):
    fmt = 'xml'


class VtepPortExtensionTestCase(test_api_v2_extension.ExtensionTestCase):
    """Test the endpoints for the vtep port extension."""

    fmt = 'json'

    def setUp(self):
        super(VtepExtensionTestCase, self).setUp()
        plural_mappings = {'port': 'ports'}
        self._setUpExtension(
            'midonet.neutron.extensions.vtep.VtepPortPluginBase',
            None, vtep.RESOURCE_ATTRIBUTE_MAP,
            vtep.Vtep, '', plural_mappings=plural_mappings)

    def test_vtep_port_list(self):
        mgmt_ip = '10.0.0.1'
        return_value = [{'name': 'dummy_vtep',
                         'description': 'This is a dummy description.'}]
        instance = self.plugin.return_value
        instance.get_vteps.return_value = return_value

        res = self.api.get(
            _get_path('vteps/%s/ports' % mgmt_ip, fmt=self.fmt))
        self.assertEqual(exc.HTTPOk.code, res.status_int)
        instance.get_vtep_portss.assert_called_once_with(
            mock.ANY, vtep_id=mgmt_ip, fields=mock.ANY, filters=mock.ANY)
        res = self.deserialize(res)
        self.assertIn('ports', res)
        self.assertEqual(1, len(res['ports']))


class VtepPortBindingExtensionTestCaseXml(VtepPortExtensionTestCase):
    fmt = 'xml'
