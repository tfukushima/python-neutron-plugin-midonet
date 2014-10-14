# Copyright (C) 2014 Midokura SARL
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import six

from neutron.api import extensions
from neutron.api.v2 import attributes as attr
from neutron.api.v2 import base
from neutron import manager

PORT = 'port'
PORTS = '%%s'

VTEP = 'vtep'
VTEPS = '%ss' % VTEP

VTEP_BINDING = 'binding'
VTEP_BINDINGS = '%ss' % VTEP_BINDING

VTEP_PORT = 'vtep_port'
VTEP_PORTS = '%ss' % VTEP_PORT

RESOURCE_ATTRIBUTE_MAP = {
    VTEPS: {
        'mgmt_ip': {'allow_post': True, 'allow_put': False,
                    'validate': {'type:ip_address': None},
                    'is_visible': True},
        'mgmt_port': {'allow_post': True, 'allow_put': True,
                      'validate': {'type:port_range': None},
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': None},
                 'is_visible': True},
        'description': {'allow_post': True, 'allow_put': False,
                        'validate': {'type:string': None},
                        'is_visible': True},
        'connection_state': {'allow_post': True, 'allow_put': False,
                             'validate': {
                                 'type:values': [
                                     'CONNECTED',
                                     'DISCONNECTED',
                                     'ERROR'
                                 ]
                             },
                             'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'is_visible': True, 'required_by_policy': True},
        'tunnel_zone_id': {'allow_post': True, 'allow_put': False,
                           'validate': {'type:uuid': None},
                           'is_visible': True, 'required_by_policy': True},
        'tunnel_ip_addrs': {'allow_post': True, 'allow_put': False,
                            'validate': {
                                'type:list_of_ip_address_or_none': None
                            },
                            'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'is_visible': True}
    },
    VTEP_BINDINGS: {
        'port_name': {'allow_post': True, 'allow_put': True,
                      'validate': {'type:string': None},
                      'is_visible': True},
        'vlan_id': {'allow_post': True, 'allow_put': True,
                    'validate': {'type:range': [0, 4095]},
                    'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
    },
    VTEP_PORTS: {
        'name': {'allow_post': False, 'allow_put': False,
                 'validate': {'type:string': None},
                 'is_visible': True},
        'description': {'allow_post': False, 'allow_put': False,
                        'validate': {'type:string': None},
                        'is_visible': True}
    }
}


def _validate_list_of_ip_address_or_none(data, key_spec=None):
    if data:
        if not isinstance(data, list):
            msg = _("must be a list of strings %s") % data
            return msg

        for item in data:
            if not attr.validators['type:ip_address'](item):
                msg = _("must be a list of strings %s") % data
                return msg

attr.validators['type:list_of_ip_address_or_none'] = \
    _validate_list_of_ip_address_or_none


class Vtep(object):
    """Vtep extension."""

    @classmethod
    def get_name(cls):
        return "Midonet Vtep Extension"

    @classmethod
    def get_alias(cls):
        return "vtep"

    @classmethod
    def get_description(cls):
        return "vtep abstraction for basic vtep-related features"

    @classmethod
    def get_namespace(cls):
        return "http://docs.openstack.org/ext/vtep/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2014-07-20T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        exts = []
        plugin = manager.NeutronManager.get_plugin()

        # VTEP
        collection_name = VTEPS
        params = RESOURCE_ATTRIBUTE_MAP.get(collection_name, dict())
        vtep_controller = base.create_resource(
            collection_name, VTEP, plugin, params)
        ex = extensions.ResourceExtension(collection_name, vtep_controller)
        exts.append(ex)

        # VTEP Binding
        parent = dict(member_name=VTEP, collection_name=VTEPS)
        collection_name = VTEP_BINDINGS
        params = RESOURCE_ATTRIBUTE_MAP.get(collection_name, dict())
        binding_controller = base.create_resource(
            collection_name, VTEP_BINDING, plugin, params, parent=parent)
        ex = extensions.ResourceExtension(
            collection_name, binding_controller, parent)
        exts.append(ex)

        parent = dict(member_name=PORT, collection_name=PORTS)
        collection_name = VTEP_BINDINGS
        params = RESOURCE_ATTRIBUTE_MAP.get(collection_name, dict())
        binding_controller = base.create_resource(
            collection_name, VTEP_BINDING, plugin, params, parent=parent)

        # VTEP Port
        parent = dict(member_name=VTEP, collection_name=VTEPS)
        collection_name = PORTS
        resource_name = PORT
        params = RESOURCE_ATTRIBUTE_MAP.get(collection_name, dict())
        vtep_port_controller = base.create_resource(
            collection_name, resource_name, plugin, params, parent=parent)
        ex = extensions.ResourceExtension(
            collection_name, vtep_port_controller, parent)
        exts.append(ex)

        return exts

    def update_attributes_map(self, attributes):
        for resource_map, attrs in RESOURCE_ATTRIBUTE_MAP.iteritems():
            extended_attrs = attributes.get(resource_map)
            if extended_attrs:
                attrs.update(extended_attrs)

    def get_extended_resources(self, version):
        if version == "2.0":
            return RESOURCE_ATTRIBUTE_MAP
        else:
            return {}


@six.add_metaclass(abc.ABCMeta)
class VtepPluginBase(object):

    @abc.abstractmethod
    def create_vtep(self, context, vtep):
        pass

    @abc.abstractmethod
    def get_vtep(self, context, ip_addr, fields=None):
        pass

    @abc.abstractmethod
    def get_vteps(self, context, filters=None, fields=None):
        pass

    @abc.abstractmethod
    def delete_vtep(self, context, ip_addr):
        pass


@six.add_metaclass(abc.ABCMeta)
class VtepBindingPluginBase(object):

    @abc.abstractmethod
    def create_vtep_binding(self, context, vtep_binding):
        pass

    @abc.abstractmethod
    def get_vtep_binding(self, context, binding, vtep_id, fields=None):
        pass

    @abc.abstractmethod
    def get_vtep_bindings(self, context, vtep_id, filters=None, fields=None):
        pass

    @abc.abstractmethod
    def delete_vtep_binding(self, context, binding, vtep_id, filters=None,
                            fields=None):
        pass


@six.add_metaclass(abc.ABCMeta)
class VtepVxlanBindingPluginBase(object):

    @abc.abstractmethod
    def get_port_binding(self, context, binding, vxlan_port_id, fields=None):
        pass

    @abc.abstractmethod
    def get_port_bindings(self, context, vxlan_port_id,
                          filters=None, fields=None):
        pass


@six.add_metaclass(abc.ABCMeta)
class VtepPortPluginBase(object):

    @abc.abstractmethod
    def get_vtep_ports(self, context, vtep_id, filters=None, fields=None):
        pass
