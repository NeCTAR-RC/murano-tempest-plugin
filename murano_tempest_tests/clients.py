# Copyright (c) 2015 Mirantis, Inc.
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

from tempest.common import credentials_factory as common_creds
from tempest import config
from tempest.lib import auth

from murano_tempest_tests.services.application_catalog \
    import application_catalog_client
from murano_tempest_tests.services.artifacts import artifacts_client
from murano_tempest_tests.services.service_broker import service_broker_client

CONF = config.CONF


class Manager(object):
    def __init__(self,
                 credentials=None):
        if credentials is None:
            credentials = common_creds.\
                get_configured_admin_credentials('identity_admin')
        self.auth_provider = get_auth_provider(credentials)
        self.service_broker_client = service_broker_client.ServiceBrokerClient(
            self.auth_provider)
        if CONF.application_catalog.glare_backend:
            self.artifacts_client = artifacts_client.ArtifactsClient(
                self.auth_provider)
        else:
            self.artifacts_client = None
        self.application_catalog_client = \
            application_catalog_client.ApplicationCatalogClient(
                self.auth_provider)


class AltManager(Manager):
    def __init__(self, service=None):
        super(AltManager, self).__init__(
            common_creds.get_configured_admin_credentials('alt_user'), service)


def get_auth_provider(credentials, scope='project'):
    default_params = {
        'disable_ssl_certificate_validation':
            CONF.identity.disable_ssl_certificate_validation,
        'ca_certs': CONF.identity.ca_certificates_file,
        'trace_requests': CONF.debug.trace_requests
    }

    if isinstance(credentials, auth.KeystoneV3Credentials):
        auth_provider_class, auth_url = \
            auth.KeystoneV3AuthProvider, CONF.identity.uri_v3
    else:
        auth_provider_class, auth_url = \
            auth.KeystoneV2AuthProvider, CONF.identity.uri

    _auth_provider = auth_provider_class(credentials, auth_url,
                                         scope=scope,
                                         **default_params)
    _auth_provider.set_auth()
    return _auth_provider
