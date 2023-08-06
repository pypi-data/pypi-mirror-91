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

from tempest import config
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
import testtools
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests import share_exceptions
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF
_MIN_SUPPORTED_MICROVERSION = '2.11'


class ReplicationActionsAdminTest(base.BaseSharesMixedTest):

    @classmethod
    def skip_checks(cls):
        super(ReplicationActionsAdminTest, cls).skip_checks()
        if not CONF.share.run_replication_tests:
            raise cls.skipException('Replication tests are disabled.')
        if CONF.share.multitenancy_enabled:
            raise cls.skipException(
                'Only for driver_handles_share_servers = False driver mode.')

        utils.check_skip_if_microversion_lt(_MIN_SUPPORTED_MICROVERSION)

    @classmethod
    def resource_setup(cls):
        super(ReplicationActionsAdminTest, cls).resource_setup()
        cls.admin_client = cls.admin_shares_v2_client
        cls.member_client = cls.shares_v2_client
        cls.replication_type = CONF.share.backend_replication_type
        cls.multitenancy_enabled = (
            utils.replication_with_multitenancy_support())

        if cls.replication_type not in constants.REPLICATION_TYPE_CHOICES:
            raise share_exceptions.ShareReplicationTypeException(
                replication_type=cls.replication_type
            )

        # create share type
        extra_specs = {"replication_type": cls.replication_type}
        cls.share_type = cls._create_share_type(specs=extra_specs)
        cls.share_type_id = cls.share_type['id']

        cls.sn_id = None
        if cls.multitenancy_enabled:
            cls.share_network = cls.shares_v2_client.get_share_network(
                cls.shares_v2_client.share_network_id)
            cls.sn_id = cls.share_network['id']

        cls.zones = cls.get_availability_zones_matching_share_type(
            cls.share_type, client=cls.admin_client)
        cls.share_zone = cls.zones[0]
        cls.replica_zone = cls.zones[-1]

        # create share
        cls.share = cls.create_share(size=CONF.share.share_size + 1,
                                     share_type_id=cls.share_type_id,
                                     availability_zone=cls.share_zone,
                                     share_network_id=cls.sn_id,
                                     client=cls.admin_client)
        cls.replica = cls.admin_client.list_share_replicas(
            share_id=cls.share['id'])[0]

    @decorators.idempotent_id('b39f319e-2515-42c0-85c4-21c2fb2123bf')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_extend_tests,
                          'Extend share tests are disabled.')
    def test_extend_replicated_share(self):
        # Test extend share
        new_size = self.share["size"] + 1
        self.admin_client.extend_share(self.share["id"], new_size)
        self.admin_client.wait_for_share_status(self.share["id"],
                                                "available")
        share = self.admin_client.get_share(self.share["id"])
        self.assertEqual(new_size, int(share["size"]))

    @decorators.idempotent_id('743bfb8e-a314-4e8e-92b5-079bd3eae72d')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_shrink_tests,
                          'Shrink share tests are disabled.')
    def test_shrink_replicated_share(self):
        share = self.admin_client.get_share(self.share["id"])
        new_size = self.share["size"] - 1
        self.admin_client.shrink_share(self.share["id"], new_size)
        self.admin_client.wait_for_share_status(share["id"], "available")
        shrink_share = self.admin_client.get_share(self.share["id"])
        self.assertEqual(new_size, int(shrink_share["size"]))

    @decorators.idempotent_id('84150cd6-2777-4806-8aa3-51359f16816e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_BACKEND)
    @testtools.skipUnless(CONF.share.run_manage_unmanage_tests,
                          'Manage/Unmanage Tests are disabled.')
    def test_manage_share_for_replication_type(self):
        """Manage a share with replication share type."""
        # Create a share and unmanage it
        share = self.create_share(size=2,
                                  share_type_id=self.share_type_id,
                                  availability_zone=self.share_zone,
                                  share_network_id=self.sn_id,
                                  cleanup_in_class=True,
                                  client=self.admin_client)
        share = self.admin_client.get_share(share["id"])
        export_locations = self.admin_client.list_share_export_locations(
            share["id"])
        export_path = export_locations[0]['path']

        self.admin_client.unmanage_share(share['id'])
        self.admin_client.wait_for_resource_deletion(share_id=share['id'])

        # Manage the previously unmanaged share
        managed_share = self.admin_client.manage_share(
            share['host'], share['share_proto'],
            export_path, self.share_type_id)
        self.admin_client.wait_for_share_status(
            managed_share['id'], 'available')

        # Add managed share to cleanup queue
        self.method_resources.insert(
            0, {'type': 'share', 'id': managed_share['id'],
                'client': self.admin_client})

        # Make sure a replica can be added to newly managed share
        self.create_share_replica(managed_share['id'], self.replica_zone,
                                  cleanup=True, client=self.admin_client)

    @decorators.idempotent_id('cbbe2650-47bb-456b-8b41-74c66270ea97')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_manage_unmanage_tests,
                          'Manage/Unmanage Tests are disabled.')
    def test_unmanage_replicated_share_with_replica(self):
        """Try to unmanage a share having replica."""
        # Create a share replica before unmanaging the share
        self.create_share_replica(self.share["id"], self.replica_zone,
                                  cleanup=True, client=self.admin_client)
        self.assertRaises(
            lib_exc.Conflict,
            self.admin_client.unmanage_share,
            share_id=self.share['id'])

    @decorators.idempotent_id('796fb2a8-1ac3-4eee-b12e-da511eb52e87')
    @tc.attr(base.TAG_POSITIVE, base.TAG_BACKEND)
    @testtools.skipUnless(CONF.share.run_manage_unmanage_tests,
                          'Manage/Unmanage Tests are disabled.')
    def test_unmanage_replicated_share_with_no_replica(self):
        """Unmanage a replication type share that does not have replica."""
        share = self.create_share(size=2,
                                  share_type_id=self.share_type_id,
                                  share_network_id=self.sn_id,
                                  availability_zone=self.share_zone,
                                  client=self.admin_client)
        self.admin_client.unmanage_share(share['id'])
        self.admin_client.wait_for_resource_deletion(share_id=share['id'])

    @decorators.idempotent_id('93220873-c6c4-40f7-840d-d0ff02e7cd7e')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_manage_unmanage_snapshot_tests,
                          'Manage/Unmanage Snapshot Tests are disabled.')
    def test_manage_replicated_share_snapshot(self):
        """Try to manage a snapshot of the replicated."""
        # Create a share replica before managing the snapshot
        self.create_share_replica(self.share["id"], self.replica_zone,
                                  cleanup=True, client=self.admin_client)
        self.assertRaises(
            lib_exc.Conflict,
            self.admin_client.manage_snapshot,
            share_id=self.share['id'],
            provider_location="127.0.0.1:/fake_provider_location/"
                              "manila_share_9dc61f49_fbc8_48d7_9337_2f9593d9")

    @decorators.idempotent_id('0b0cd350-8691-477b-adb1-5e79b92e3759')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_manage_unmanage_snapshot_tests,
                          'Manage/Unmanage Snapshot Tests are disabled.')
    def test_unmanage_replicated_share_snapshot(self):
        """Try to unmanage a snapshot of the replicated share with replica."""
        # Create a share replica before unmanaging the snapshot
        self.create_share_replica(self.share["id"], self.replica_zone,
                                  cleanup=True, client=self.admin_client)
        snapshot = self.create_snapshot_wait_for_active(
            self.share["id"], client=self.admin_client)
        self.assertRaises(
            lib_exc.Conflict,
            self.admin_client.unmanage_snapshot,
            snapshot_id=snapshot['id'])
