# Copyright (c) 2015 Telefonica I+D.
# Copyright (c) 2016 Mirantis, Inc.
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

from tempest.lib import decorators

from murano_tempest_tests.tests.api.application_catalog import base
from murano_tempest_tests import utils


class TestEnvironmentTemplatesSanity(base.BaseApplicationCatalogTest):

    @decorators.idempotent_id('c13f9799-ed80-463f-8275-6bba62933226')
    def test_list_empty_env_templates(self):
        templates_list = self.application_catalog_client.\
            get_env_templates_list()
        self.assertIsInstance(templates_list, list)

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('15363b15-c350-40b9-a96b-de8d7a56a185')
    def test_create_and_delete_env_template(self):
        name = utils.generate_name('create_and_delete_env_template')
        env_template = self.application_catalog_client.\
            create_env_template(name)
        self.assertFalse(env_template['is_public'])
        self.assertEqual(name, env_template['name'])
        self.assertEqual("description", env_template['description_text'])
        env_templates_list = self.application_catalog_client.\
            get_env_templates_list()
        # Deleting dates from dictionaries to skip it in assert
        env_template.pop('updated', None)
        env_template.pop('created', None)
        list(map(lambda x: x.pop('updated', None), env_templates_list))
        list(map(lambda x: x.pop('created', None), env_templates_list))
        self.assertIn(env_template, env_templates_list)
        self.application_catalog_client.\
            delete_env_template(env_template['id'])
        env_templates_list = self.application_catalog_client.\
            get_env_templates_list()
        self.assertNotIn(env_template, env_templates_list)


class TestEnvironmentTemplates(base.BaseApplicationCatalogTest):

    @classmethod
    def resource_setup(cls):
        super(TestEnvironmentTemplates, cls).resource_setup()
        name = utils.generate_name(cls.__name__)
        cls.env_template = cls.application_catalog_client.\
            create_public_env_template(name)
        cls.alt_client = cls.get_client_with_isolated_creds('alt')

    @classmethod
    def resource_cleanup(cls):
        cls.application_catalog_client.\
            delete_env_template(cls.env_template['id'])
        super(TestEnvironmentTemplates, cls).resource_cleanup()

    @decorators.idempotent_id('3821a826-2d14-4287-b56b-4a022bca9044')
    def test_get_env_template(self):
        env_template = self.application_catalog_client.\
            get_env_template(self.env_template['id'])
        self.assertEqual(self.env_template['name'], env_template['name'])

    @decorators.idempotent_id('c7f77fa4-cdc3-45b7-a013-668668da0c8e')
    def test_create_env_template_with_a_service(self):
        name = utils.generate_name('create_env_template_with_service')
        post_body = self._get_demo_app()
        env_template = self.application_catalog_client.\
            create_env_template_with_services(name, post_body)
        self.addCleanup(self.application_catalog_client.delete_env_template,
                        env_template['id'])
        list_services = self.application_catalog_client.\
            get_services_list_in_env_template(env_template['id'])
        self.assertIsInstance(list_services, list)
        self.assertIn(post_body, list_services)

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('be1be6c8-b882-4b17-9221-4b88c71d8d31')
    def test_add_and_remove_service_in_env_templates(self):
        env_template_services = self.application_catalog_client.\
            get_services_list_in_env_template(self.env_template['id'])
        self.assertIsInstance(env_template_services, list)
        post_body = self._get_demo_app()
        service = self.application_catalog_client.\
            create_service_in_env_template(self.env_template['id'], post_body)
        self.assertEqual(post_body['name'], service['name'])
        services = self.application_catalog_client.\
            get_services_list_in_env_template(self.env_template['id'])
        self.assertIn(service, services)
        self.application_catalog_client.\
            delete_service_from_env_template(self.env_template['id'],
                                             service['?']['id'])
        services = self.application_catalog_client.\
            get_services_list_in_env_template(self.env_template['id'])
        self.assertNotIn(service, services)

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('4c409154-f848-42b5-99e4-3d1352d0cf3f')
    def test_update_service_in_env_templates(self):
        env_template_services = self.application_catalog_client.\
            get_services_list_in_env_template(self.env_template['id'])
        self.assertIsInstance(env_template_services, list)
        post_body = self._get_demo_app()
        service = self.application_catalog_client.\
            create_service_in_env_template(self.env_template['id'], post_body)
        self.assertEqual(post_body['name'], service['name'])
        post_body["name"] = "updated_name"
        service = self.application_catalog_client.\
            update_service_from_env_template(self.env_template['id'],
                                             service["?"]["id"],
                                             post_body)
        self.assertEqual("updated_name", service['name'])

    @decorators.idempotent_id('1fe4b071-8c1f-434a-bb37-0712879df931')
    def test_create_public_env_template(self):
        name = utils.generate_name('create_public_env_template')
        env_template = self.application_catalog_client.\
            create_public_env_template(name)
        self.addCleanup(self.application_catalog_client.delete_env_template,
                        env_template['id'])
        self.assertEqual(name, env_template['name'])
        env_temp = self.application_catalog_client.\
            get_env_template(env_template['id'])
        self.assertTrue(env_temp['is_public'])

    @decorators.idempotent_id('1c79c1dc-c4ff-42d7-9382-6d523f2d9f5b')
    def test_clone_env_template(self):
        name = utils.generate_name('clone_env_template')
        cloned_template = self.alt_client.\
            clone_env_template(self.env_template['id'], name)
        self.addCleanup(self.alt_client.delete_env_template,
                        cloned_template['id'])
        self.assertEqual(name, cloned_template['name'])
        template = self.alt_client.get_env_template(cloned_template['id'])
        self.assertEqual(name, template['name'])

    @decorators.idempotent_id('98f889cf-de5e-4cda-a97e-f2eff3b471ce')
    def test_get_public_private_both_env_templates(self):
        name = utils.generate_name('get_public_private_both')
        public_env_template = self.application_catalog_client.\
            create_public_env_template(name)
        self.addCleanup(self.application_catalog_client.delete_env_template,
                        public_env_template['id'])
        self.assertTrue(public_env_template['is_public'])
        private_name = utils.generate_name('get_public_private_both')
        private_env_template = self.application_catalog_client.\
            create_env_template(private_name)
        self.addCleanup(self.application_catalog_client.delete_env_template,
                        private_env_template['id'])
        self.assertFalse(private_env_template['is_public'])
        private_name_alt = utils.generate_name('get_public_private_both')
        private_alt_env_template = self.alt_client.\
            create_env_template(private_name_alt)
        self.addCleanup(self.alt_client.delete_env_template,
                        private_alt_env_template['id'])

        public_env_templates = self.application_catalog_client.\
            get_public_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None),
             public_env_templates + [public_env_template] +
             [private_env_template] + [private_alt_env_template]))
        list(map(lambda x: x.pop('created', None),
             public_env_templates + [public_env_template] +
             [private_env_template] + [private_alt_env_template]))

        self.assertIn(public_env_template, public_env_templates)
        self.assertNotIn(private_env_template, public_env_templates)
        self.assertNotIn(private_alt_env_template, public_env_templates)

        private_env_templates = self.application_catalog_client.\
            get_private_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None), private_env_templates))
        list(map(lambda x: x.pop('created', None), private_env_templates))

        self.assertNotIn(public_env_template, private_env_templates)
        self.assertIn(private_env_template, private_env_templates)
        self.assertNotIn(private_alt_env_template, private_env_templates)

        env_templates = self.application_catalog_client.\
            get_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None), env_templates))
        list(map(lambda x: x.pop('created', None), env_templates))

        self.assertIn(public_env_template, env_templates)
        self.assertIn(private_env_template, env_templates)
        self.assertNotIn(private_alt_env_template, env_templates)

        alt_pub_templates = self.alt_client.get_public_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None), alt_pub_templates))
        list(map(lambda x: x.pop('created', None), alt_pub_templates))

        self.assertIn(public_env_template, alt_pub_templates)
        self.assertNotIn(private_env_template, alt_pub_templates)
        self.assertNotIn(private_alt_env_template, alt_pub_templates)

        alt_priv_templates = self.alt_client.get_private_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None), alt_priv_templates))
        list(map(lambda x: x.pop('created', None), alt_priv_templates))

        self.assertNotIn(public_env_template, alt_priv_templates)
        self.assertNotIn(private_env_template, alt_priv_templates)
        self.assertIn(private_alt_env_template, alt_priv_templates)

        alt_env_templates = self.alt_client.get_env_templates_list()

        # Deleting dates from dictionaries to skip it in assert
        list(map(lambda x: x.pop('updated', None), alt_env_templates))
        list(map(lambda x: x.pop('created', None), alt_env_templates))

        self.assertIn(public_env_template, alt_env_templates)
        self.assertNotIn(private_env_template, alt_env_templates)
        self.assertIn(private_alt_env_template, alt_env_templates)

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('f7524a15-a4ad-43a5-bcb2-784fd515eb59')
    def test_create_env_from_template(self):
        name = utils.generate_name('create_env_from_template')
        env_template = self.application_catalog_client.\
            create_public_env_template(name)
        self.addCleanup(self.application_catalog_client.delete_env_template,
                        env_template['id'])
        post_body = self._get_demo_app()
        service = self.application_catalog_client.\
            create_service_in_env_template(env_template['id'], post_body)
        self.assertEqual(post_body['name'], service['name'])
        env_name = utils.generate_name('create_env_from_template')
        environment = self.application_catalog_client.\
            create_env_from_template(env_template['id'], env_name)
        self.addCleanup(self.application_catalog_client.delete_environment,
                        environment['environment_id'])
        self.assertIsNotNone(environment)
        service_from_env = self.application_catalog_client.\
            get_service(environment['environment_id'],
                        service['?']['id'],
                        environment['session_id'])
        self.assertEqual(service, service_from_env)
