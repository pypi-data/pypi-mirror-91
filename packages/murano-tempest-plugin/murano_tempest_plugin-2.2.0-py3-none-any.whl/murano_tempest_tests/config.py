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

from oslo_config import cfg

service_option = [
    cfg.BoolOpt("murano",
                default=True,
                help="Whether or not murano is expected to be available"),
    cfg.BoolOpt("murano_cfapi",
                default=False,
                help="Whether or not murano-cfapi is expected to be "
                     "unavailable by default"),
    cfg.BoolOpt("glare",
                default=False,
                help="Whether or not glare is expected to be unavailable")
]

application_catalog_group = cfg.OptGroup(name="application_catalog",
                                         title="Application Catalog Options")

service_broker_group = cfg.OptGroup(name="service_broker",
                                    title="Service Broker Options")

artifacts_group = cfg.OptGroup(name="artifacts",
                               title="Glance Artifacts Options")

orchestration_group = cfg.OptGroup(name='orchestration',
                                   title='Orchestration Service Options')

ApplicationCatalogGroup = [
    # Application catalog tempest configuration
    cfg.StrOpt("region",
               default="",
               help="The application_catalog region name to use. If empty, "
                    "the value of identity.region is used instead. "
                    "If no such region is found in the service catalog, "
                    "the first found one is used."),

    cfg.StrOpt("linux_image",
               default="debian-8-m-agent.qcow2",
               help="Image for linux services"),

    cfg.StrOpt("catalog_type",
               default="application-catalog",
               help="Catalog type of Application Catalog."),

    cfg.StrOpt("endpoint_type",
               default="publicURL",
               choices=["publicURL", "adminURL", "internalURL"],
               help="The endpoint type for application catalog service."),

    cfg.IntOpt("build_interval",
               default=3,
               help="Time in seconds between application catalog"
                    " availability checks."),

    cfg.IntOpt("build_timeout",
               default=500,
               help="Timeout in seconds to wait for a application catalog"
                    " to become available."),
    cfg.BoolOpt("glare_backend",
                default=False,
                help="Tells tempest about murano glare backend "
                     "configuration."),
    cfg.BoolOpt("cinder_volume_tests",
                default=False,
                help="Whether or not cinder volumes attachment tests "
                     "are expected to run"),
    cfg.BoolOpt("deployment_tests",
                default=False,
                help="Whether or not deployment tests are expected to run")
]

ServiceBrokerGroup = [
    # Test runs control
    cfg.BoolOpt("run_service_broker_tests",
                default=False,
                help="Defines whether run service broker api tests or not"),

    cfg.StrOpt("catalog_type",
               default="service-broker",
               help="Catalog type of Service Broker API"),

    cfg.StrOpt("endpoint_type",
               default="publicURL",
               choices=["publicURL", "adminURL", "internalURL"],
               help="The endpoint type for service broker service"),

    cfg.IntOpt("build_interval",
               default=3,
               help="Time in seconds between service broker"
                    " availability checks."),

    cfg.IntOpt("build_timeout",
               default=500,
               help="Timeout in seconds to wait for a service broker"
                    " to become available.")


]

ArtifactsGroup = [
    # Glance artifacts options
    cfg.StrOpt("catalog_type",
               default="artifact",
               help="Catalog type of Artifacts API"),

    cfg.StrOpt("endpoint_type",
               default="publicURL",
               choices=["publicURL", "adminURL", "internalURL"],
               help="The endpoint type for artifacts service"),

    cfg.IntOpt("build_interval",
               default=3,
               help="Time in seconds between artifacts"
                    " availability checks."),

    cfg.IntOpt("build_timeout",
               default=500,
               help="Timeout in seconds to wait for a artifacts"
                    " to become available.")
]

OrchestrationGroup = [
    cfg.StrOpt('catalog_type',
               default='orchestration',
               help="Catalog type of the Orchestration service."),
    cfg.StrOpt('region',
               default='',
               help="The orchestration region name to use. If empty, the "
                    "value of identity.region is used instead. If no such "
                    "region is found in the service catalog, the first found "
                    "one is used."),
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               choices=['public', 'admin', 'internal',
                        'publicURL', 'adminURL', 'internalURL'],
               help="The endpoint type to use for the orchestration service."),
    cfg.StrOpt('stack_owner_role', default='heat_stack_owner',
               help='Role required for users to be able to manage stacks'),
    cfg.IntOpt('build_interval',
               default=1,
               help="Time in seconds between build status checks."),
    cfg.IntOpt('build_timeout',
               default=1200,
               help="Timeout in seconds to wait for a stack to build.")
]
