# Copyright 2014 Mirantis Inc.
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

import ddt
from tempest import config
from tempest.lib import decorators
import testtools
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base

CONF = config.CONF


@ddt.ddt
class AdminActionsTest(base.BaseSharesAdminTest):

    @classmethod
    def resource_setup(cls):
        super(AdminActionsTest, cls).resource_setup()
        cls.task_states = ["migration_starting", "data_copying_in_progress",
                           "migration_success", None]
        cls.bad_status = "error_deleting"
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']
        # create share
        cls.sh = cls.create_share(share_type_id=cls.share_type_id)

    def _wait_for_resource_status(self, resource_id, resource_type):
        wait_for_resource_status = getattr(
            self.shares_v2_client, "wait_for_{}_status".format(resource_type))
        wait_for_resource_status(resource_id, "available")

    def _reset_resource_available(self, resource_id, resource_type="shares"):
        self.shares_v2_client.reset_state(
            resource_id, s_type=resource_type, status="available")
        self._wait_for_resource_status(resource_id, resource_type[:-1])

    @decorators.idempotent_id('4f8c6ae9-0656-445f-a911-fbf98fe761d0')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data("error", "available", "error_deleting", "deleting", "creating")
    def test_reset_share_state(self, status):
        self.shares_v2_client.reset_state(self.sh["id"], status=status)
        self.shares_v2_client.wait_for_share_status(self.sh["id"], status)
        self.addCleanup(self._reset_resource_available, self.sh["id"])

    @decorators.idempotent_id('13075b2d-fe83-41bf-b6ef-99cfcc00257d')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data("error", "available", "error_deleting", "deleting", "creating")
    def test_reset_share_instance_state(self, status):
        sh_instance = self.shares_v2_client.get_instances_of_share(
            self.sh["id"])[0]
        share_instance_id = sh_instance["id"]
        self.shares_v2_client.reset_state(
            share_instance_id, s_type="share_instances", status=status)
        self.shares_v2_client.wait_for_share_instance_status(
            share_instance_id, status)
        self.addCleanup(self._reset_resource_available,
                        share_instance_id, "share_instances")

    @decorators.idempotent_id('3e16d990-fa19-45e9-893f-e0b7a90127bd')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_snapshot_tests,
                          "Snapshot tests are disabled.")
    @ddt.data("error", "available", "error_deleting", "deleting", "creating")
    def test_reset_snapshot_state(self, status):
        snapshot = self.create_snapshot_wait_for_active(self.sh["id"])
        self.shares_v2_client.reset_state(
            snapshot["id"], s_type="snapshots", status=status)
        self.shares_v2_client.wait_for_snapshot_status(
            snapshot["id"], status)
        self.addCleanup(self._reset_resource_available,
                        snapshot["id"], "snapshots")

    @decorators.idempotent_id('2e8fee75-6b7f-4b69-8f68-0646ce6a96e9')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_force_delete_share(self):
        share = self.create_share(share_type_id=self.share_type_id)

        # Change status from 'available' to 'error_deleting'
        self.shares_v2_client.reset_state(share["id"], status=self.bad_status)

        # Check that status was changed
        check_status = self.shares_v2_client.get_share(share["id"])
        self.assertEqual(self.bad_status, check_status["status"])

        # Share with status 'error_deleting' should be deleted
        self.shares_v2_client.force_delete(share["id"])
        self.shares_v2_client.wait_for_resource_deletion(share_id=share["id"])

    @decorators.idempotent_id('382fca90-746e-4ad1-a509-b82a643d4a03')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_force_delete_share_instance(self):
        share = self.create_share(share_type_id=self.share_type_id,
                                  cleanup_in_class=False)
        instances = self.shares_v2_client.get_instances_of_share(share["id"])
        # Check that instance was created
        self.assertEqual(1, len(instances))

        instance = instances[0]

        # Change status from 'available' to 'error_deleting'
        self.shares_v2_client.reset_state(
            instance["id"], s_type="share_instances", status=self.bad_status)

        # Check that status was changed
        check_status = self.shares_v2_client.get_share_instance(instance["id"])
        self.assertEqual(self.bad_status, check_status["status"])

        # Share with status 'error_deleting' should be deleted
        self.shares_v2_client.force_delete(
            instance["id"], s_type="share_instances")
        self.shares_v2_client.wait_for_resource_deletion(
            share_instance_id=instance["id"])

    @decorators.idempotent_id('d5a48182-ecd7-463e-a31a-148c81d3c5ed')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(CONF.share.run_snapshot_tests,
                          "Snapshot tests are disabled.")
    def test_force_delete_snapshot(self):
        sn = self.create_snapshot_wait_for_active(self.sh["id"])

        # Change status from 'available' to 'error_deleting'
        self.shares_v2_client.reset_state(
            sn["id"], s_type="snapshots", status=self.bad_status)

        # Check that status was changed
        check_status = self.shares_v2_client.get_snapshot(sn["id"])
        self.assertEqual(self.bad_status, check_status["status"])

        # Snapshot with status 'error_deleting' should be deleted
        self.shares_v2_client.force_delete(sn["id"], s_type="snapshots")
        self.shares_v2_client.wait_for_resource_deletion(snapshot_id=sn["id"])

    @decorators.idempotent_id('49a576eb-733a-4299-aa6f-918fe7c67a6a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @base.skip_if_microversion_lt("2.22")
    def test_reset_share_task_state(self):
        for task_state in self.task_states:
            self.shares_v2_client.reset_task_state(self.sh["id"], task_state)
            self.shares_v2_client.wait_for_share_status(
                self.sh["id"], task_state, 'task_state')
