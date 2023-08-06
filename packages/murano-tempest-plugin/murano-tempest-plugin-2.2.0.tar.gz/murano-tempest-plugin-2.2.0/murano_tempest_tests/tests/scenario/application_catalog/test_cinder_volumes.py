#    Copyright (c) 2016 Mirantis, Inc.
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

import os
import testtools

from tempest import config
from tempest.lib import decorators

from murano_tempest_tests.tests.scenario.application_catalog import base
from murano_tempest_tests import utils

CONF = config.CONF


class TestCinderVolumes(base.BaseApplicationCatalogScenarioTest):

    @classmethod
    def skip_checks(cls):
        super(TestCinderVolumes, cls).skip_checks()
        if not CONF.service_available.cinder:
            msg = "Cinder is not available. Skipping volumes tests"
            raise cls.skipException(msg)

    @classmethod
    def setup_clients(cls):
        super(TestCinderVolumes, cls).setup_clients()
        _volume = cls.services_manager.volume_v3
        cls.volumes_client = _volume.VolumesClient()
        cls.backups_client = _volume.BackupsClient()
        cls.snapshots_client = _volume.SnapshotsClient()

    @classmethod
    def resource_setup(cls):
        if not CONF.application_catalog.cinder_volume_tests:
            msg = "Cinder volumes tests will be skipped."
            raise cls.skipException(msg)
        super(TestCinderVolumes, cls).resource_setup()
        cls.linux = CONF.application_catalog.linux_image
        application_name = utils.generate_name('VM')
        cls.abs_archive_path, dir_with_archive, archive_name = \
            utils.prepare_package(
                application_name,
                app='io.murano.apps.test.VM',
                manifest_required=False)
        if CONF.application_catalog.glare_backend:
            cls.client = cls.artifacts_client
        else:
            cls.client = cls.application_catalog_client
        cls.package = cls.client.upload_package(
            application_name, archive_name, dir_with_archive,
            {"categories": ["Web"], "tags": ["test"]})
        cls.volume = cls.create_volume(size='1')

    @classmethod
    def resource_cleanup(cls):
        cls.delete_volume(cls.volume['id'])
        cls.client.delete_package(cls.package['id'])
        os.remove(cls.abs_archive_path)
        super(TestCinderVolumes, cls).resource_cleanup()

    @decorators.idempotent_id('241ace7d-3b6e-413e-8936-a851ff1163f8')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_boot_volume_as_image(self):
        """Test app deployment using boot volume as image

        Scenario:
            1. Create environment
            2. Add VM application with ability to boot instance
            from Cinder volume
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that instance is not booted from image, volume is attached
            to the instance, has size 4GiB and created from image
            7. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        post_body = {
            "instance": {
                "flavor": "m1.tiny",
                "blockDevices": {
                    "volume": {
                        "?": {
                            "type": "io.murano.resources.CinderVolume"
                        },
                        "size": 4,
                        "sourceImage": self.cirros_image
                    },
                    "bootIndex": 0,
                    "deviceName": "vda",
                    "deviceType": "disk"
                },
                "assignFloatingIp": True,
                "availabilityZone": "nova",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": utils.generate_uuid()
                },
                "name": utils.generate_name("testMurano")
            },
            "name": utils.generate_name("VM"),
            "?": {
                "_{id}".format(id=utils.generate_uuid()): {
                    "name": "VM"
                },
                "type": "io.murano.apps.test.VM",
                "id": utils.generate_uuid()
            }
        }
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 4)
        self.assertEqual(volume_data['volume_image_metadata']['image_name'],
                         self.cirros_image)
        server = self.get_instance_id('testMurano')
        self.assertFalse(
            self.servers_client.show_server(server)['server']['image'])

    @decorators.idempotent_id('e10d3bad-7145-46df-8118-4040842883f6')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_existing_volume(self):
        """Test app deployment with existing volume

        Scenario:
            1. Create environment
            2. Add VM application with ability to attach existing
            Cinder volume to the instance
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that volume is attached to the instance
            7. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.ExistingCinderVolume"
                },
                "openstackId": self.volume['id']
            }
        }
        post_body = self.vm_cinder(attributes=volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        self.check_volume_attached('testMurano', self.volume['id'])

    @decorators.idempotent_id('6338a496-7415-42a9-a514-61f6f5cb1e65')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation(self):
        """Test app deployment with volume creation

        Scenario:
            1. Create environment
            2. Add VM application with ability to create and
            attach Cinder volume with size 1 GiB to the instance
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that volume is attached to the instance and has size 1GiB
            7. Check that we can access some attachment info about the volume
            8. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 1
            }
        }
        post_body = self.vm_cinder(attributes=volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.check_volume_attachments(environment['id'])
        self.assertEqual(volume_data['size'], 1)

    @decorators.idempotent_id('1eb9bbe4-9810-408e-86a0-78ff114aadae')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation_from_image(self):
        """Test app deployment with volume creation from image

        Scenario:
            1. Create environment
            2. Add VM application with ability to create Cinder
            volume with size 2 GiB from image and attach it to the instance
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that volume is attached to the instance, has size 2GiB and
            created from image
            7. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 4,
                "sourceImage": self.cirros_image
            }
        }
        post_body = self.vm_cinder(volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 4)
        self.assertEqual(volume_data['volume_image_metadata']['image_name'],
                         self.cirros_image)

    @decorators.idempotent_id('bd624a9b-10ae-4079-b515-7b6031d9e725')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation_from_volume(self):
        """Test app deployment with volume creation from volume

        Scenario:
            1. Create environment
            2. Add VM application with ability to create Cinder
            volume with size 1 GiB from existing volume and attach it to the
            instance
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that volume is attached to the instance, has size 1GiB and
            created from existing volume
            7. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 1,
                "sourceVolume": {
                    "?": {
                        "type": "io.murano.resources.ExistingCinderVolume"
                    },
                    "openstackId": self.volume['id']
                }
            }
        }
        post_body = self.vm_cinder(volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 1)
        self.assertEqual(volume_data['source_volid'], self.volume['id'])

    @decorators.idempotent_id('7a671222-160d-4594-97bf-ea47f60ad965')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation_from_snapshot(self):
        """Test app deployment with volume creation from volume snapshot

        Scenario:
            1. Make snapshot from volume
            2. Create environment
            3. Add VM application with ability to create
            Cinder volume with size 1 GiB from existing volume snapshot and
            attach it to the instance
            4. Deploy environment
            5. Make sure that deployment finished successfully
            6. Check that application is accessible
            7. Check that volume is attached to the instance, has size 1GiB and
            created from existing volume snapshot
            8. Delete environment, snapshot
        """
        snapshot = self.create_snapshot(self.volume['id'])
        self.addCleanup(self.delete_snapshot, snapshot['id'])
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 1,
                "sourceSnapshot": {
                    "?": {
                        "type": "io.murano.resources.CinderVolumeSnapshot"
                    },
                    "openstackId": snapshot['id']
                }
            }
        }
        post_body = self.vm_cinder(volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 1)
        self.assertEqual(volume_data['snapshot_id'], snapshot['id'])


class TestCinderVolumeIsolatedAdmin(
        base.BaseApplicationCatalogScenarioIsolatedAdminTest):

    @classmethod
    def resource_setup(cls):
        if not CONF.application_catalog.cinder_volume_tests:
            msg = "Cinder volumes attachment tests will be skipped."
            raise cls.skipException(msg)
        super(TestCinderVolumeIsolatedAdmin, cls).resource_setup()
        application_name = utils.generate_name('VM')
        cls.abs_archive_path, dir_with_archive, archive_name = \
            utils.prepare_package(
                application_name,
                app='io.murano.apps.test.VM',
                manifest_required=False)
        if CONF.application_catalog.glare_backend:
            cls.client = cls.artifacts_client
        else:
            cls.client = cls.application_catalog_client
        cls.package = cls.client.upload_package(
            application_name, archive_name, dir_with_archive,
            {"categories": ["Web"], "tags": ["test"]})
        cls.volume = cls.create_volume(size='1')

    @classmethod
    def resource_cleanup(cls):
        cls.delete_volume(cls.volume['id'])
        cls.client.delete_package(cls.package['id'])
        os.remove(cls.abs_archive_path)
        super(TestCinderVolumeIsolatedAdmin, cls).resource_cleanup()

    @decorators.idempotent_id('4111eb94-2636-4d0b-af5c-776ed5a59b87')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation_readonly(self):
        """Test app deploy with volume creation with readonly

        Scenario:
            1. Create environment
            2. Add VM application with ability to create and
            attach Cinder volume with size 1 GiB and readonly
            properties to the instance
            3. Deploy environment
            4. Make sure that deployment finished successfully
            5. Check that application is accessible
            6. Check that volume is attached to the instance, has size 1GiB,
            and readonly attributes
            7. Delete environment
        """
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client.\
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client.\
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 1,
                "readOnly": True
            }
        }
        post_body = self.vm_cinder(attributes=volume_attributes)
        self.application_catalog_client.\
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 1)
        self.assertEqual(volume_data['metadata']['readonly'], 'True')

    @decorators.idempotent_id('5c134343-11bc-4329-ac30-9b43f32c15e2')
    @testtools.testcase.attr('smoke')
    @testtools.testcase.attr('scenario')
    def test_deploy_app_with_volume_creation_from_backup(self):
        """Test app deployment with volume creation from volume backup

        Scenario:
            1. Make backup from volume
            2. Create environment
            3. Add VM application with ability to create Cinder
            volume with size 1 GiB from existing volume backup and attach it to
            the instance
            4. Deploy environment
            5. Make sure that deployment finished successfully
            6. Check that application is accessible
            7. Check that volume is attached to the instance, has size 1GiB and
            restored from existing volume backup
            8. Delete environment, backup
        """
        if not (CONF.volume_feature_enabled.backup and
                CONF.service_available.swift):
            msg = ("Cinder backup driver and Swift are required. "
                   "Deploy app with volume restoring from backup test "
                   "will be skipped.")
            raise self.skipException(msg)

        backup = self.create_backup(self.volume['id'])
        self.addCleanup(self.delete_backup, backup['id'])
        name = utils.generate_name('testMurano')
        environment = self.application_catalog_client. \
            create_environment(name)
        self.addCleanup(self.environment_delete, environment['id'])
        session = self.application_catalog_client. \
            create_session(environment['id'])
        volume_attributes = {
            "/dev/vdb": {
                "?": {
                    "type": "io.murano.resources.CinderVolume"
                },
                "size": 1,
                "name": "restore_backup_" + backup['id'],
                "sourceVolumeBackup": {
                    "?": {
                        "type": "io.murano.resources.CinderVolumeBackup"
                    },
                    "openstackId": backup['id']
                }
            }
        }
        post_body = self.vm_cinder(volume_attributes)
        self.application_catalog_client. \
            create_service(environment['id'], session['id'],
                           post_body)
        self.deploy_environment(environment, session)

        volume_data = self.get_volume(environment['id'])
        self.check_volume_attached('testMurano', volume_data['id'])
        self.assertEqual(volume_data['size'], 1)
        self.assertIn(backup['id'], volume_data['name'])
