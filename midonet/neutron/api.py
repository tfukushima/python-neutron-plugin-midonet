# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright (C) 2014 Midokura SARL.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from midonet.neutron.common import util

from neutron.api.v2 import base

CREATE = base.Controller.CREATE
DELETE = base.Controller.DELETE
LIST = base.Controller.LIST
SHOW = base.Controller.SHOW
UPDATE = base.Controller.UPDATE


@util.generate_methods(LIST, SHOW, CREATE, DELETE)
class BgpHandlerMixin(object):
    """The mixin of the request handler for the BGP."""


@util.generate_methods(LIST, SHOW, CREATE, DELETE)
class AdRouteHandlerMixin(object):
    """The mixin of the request handler for the advertised routes."""
    ALIAS = 'ad_route'


@util.generate_methods(LIST, SHOW, CREATE, UPDATE, DELETE)
class ChainHandlerMixin(object):
    """The mixin of the request handler for the chains."""


@util.generate_methods(LIST, SHOW, CREATE, DELETE)
class RuleHandlerMixin(object):
    """The mixin of the request handler for the rules."""


@util.generate_methods(LIST, SHOW, CREATE, UPDATE, DELETE)
class TunnelzoneHandlerMixin(object):
    """The mixin of the request handler for the tunnel zones."""


@util.generate_methods(LIST, SHOW, CREATE, UPDATE, DELETE)
class TunnelzonehostHandlerMixin(object):
    """The mixin of the request handler for the tunnel zone hosts."""
    PARENT = TunnelzoneHandlerMixin.ALIAS


class MidoNetApiMixin(AdRouteHandlerMixin,
                      BgpHandlerMixin,
                      ChainHandlerMixin,
                      RuleHandlerMixin,
                      TunnelzoneHandlerMixin,
                      TunnelzonehostHandlerMixin):
    """MidoNet REST API plugin."""
