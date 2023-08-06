# -*- coding: utf-8 -*-
# Copyright 2016 Andrew Kerr
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
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF
LATEST_MICROVERSION = CONF.share.max_api_microversion


@ddt.ddt
class ShareGroupActionsTest(base.BaseSharesMixedTest):
    """Covers share group functionality."""

    @classmethod
    def skip_checks(cls):
        super(ShareGroupActionsTest, cls).skip_checks()
        if not CONF.share.run_share_group_tests:
            raise cls.skipException('Share Group tests disabled.')

        utils.check_skip_if_microversion_lt(
            constants.MIN_SHARE_GROUP_MICROVERSION)

    @classmethod
    def resource_setup(cls):
        super(ShareGroupActionsTest, cls).resource_setup()

        # Create a share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

        cls.share_group_type = cls._create_share_group_type()
        cls.share_group_type_id = cls.share_group_type['id']

        # Create first share group
        cls.share_group_name = data_utils.rand_name("tempest-sg-name")
        cls.share_group_desc = data_utils.rand_name("tempest-sg-description")
        cls.share_group = cls.create_share_group(
            name=cls.share_group_name,
            description=cls.share_group_desc,
            share_group_type_id=cls.share_group_type_id,
            share_type_ids=[cls.share_type_id],
        )

        # Create second share group for purposes of sorting and snapshot
        # filtering
        cls.share_group2 = cls.create_share_group(
            name=cls.share_group_name,
            description=cls.share_group_desc,
            share_group_type_id=cls.share_group_type_id,
            share_type_ids=[cls.share_type_id],
        )

        # Create 2 shares - inside first and second share groups
        cls.share_name = data_utils.rand_name("tempest-share-name")
        cls.share_desc = data_utils.rand_name("tempest-share-description")
        cls.share_size = 1
        cls.share_size2 = 2
        cls.shares = cls.create_shares([
            {'kwargs': {
                'name': cls.share_name,
                'description': cls.share_desc,
                'size': size,
                'share_type_id': cls.share_type_id,
                'share_group_id': sg_id,
            }} for size, sg_id in ((cls.share_size, cls.share_group['id']),
                                   (cls.share_size2, cls.share_group['id']),
                                   (cls.share_size, cls.share_group2['id']))
        ])

        # Create share group snapshots
        cls.sg_snap_name = data_utils.rand_name("tempest-sg-snap-name")
        cls.sg_snap_desc = data_utils.rand_name("tempest-sg-snap-desc")

        cls.sg_snapshot = cls.create_share_group_snapshot_wait_for_active(
            cls.share_group["id"],
            name=cls.sg_snap_name,
            description=cls.sg_snap_desc,
        )

        cls.sg_snapshot2 = cls.create_share_group_snapshot_wait_for_active(
            cls.share_group2['id'],
            name=cls.sg_snap_name,
            description=cls.sg_snap_desc,
        )

    @decorators.idempotent_id('1e359389-09a7-4235-84c9-7b5c83632fff')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_get_share_group(self, version):
        self.skip_if_microversion_not_supported(version)

        # Get share group
        share_group = self.shares_v2_client.get_share_group(
            self.share_group['id'], version=version)

        # Verify keys
        actual_keys = set(share_group.keys())
        self.assertTrue(
            constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(actual_keys),
            'Not all required keys returned for share group %s. '
            'Expected at least: %s, found %s' % (
                share_group['id'],
                constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                actual_keys))

        # Verify values
        self.assertEqual(self.share_group_name, share_group["name"])
        self.assertEqual(self.share_group_desc, share_group["description"])

    @decorators.idempotent_id('45b77673-b1bb-43a1-b4b7-41351930adbd')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_get_share_min_supported_sg_microversion(self):

        # Get share
        share = self.shares_v2_client.get_share(
            self.shares[0]['id'],
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Verify keys
        expected_keys = {
            "status", "description", "links", "availability_zone",
            "created_at", "share_proto", "name", "snapshot_id",
            "id", "size", "share_group_id",
        }
        actual_keys = set(share.keys())
        self.assertTrue(
            expected_keys.issubset(actual_keys),
            'Not all required keys returned for share %s.  '
            'Expected at least: %s, found %s' % (
                share['id'], expected_keys, actual_keys))

        # Verify values
        self.assertEqual(self.share_name, share["name"])
        self.assertEqual(self.share_desc, share["description"])
        self.assertEqual(self.share_size, int(share["size"]))
        self.assertEqual(self.share_group["id"], share["share_group_id"])

    @decorators.idempotent_id('04fcd695-c5f8-4de7-ab09-131424e6bdfb')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_list_share_groups(self, version):
        self.skip_if_microversion_not_supported(version)

        # List share groups
        share_groups = self.shares_v2_client.list_share_groups(
            version=version)

        # Verify keys
        self.assertGreater(len(share_groups), 0)
        for sg in share_groups:
            keys = set(sg.keys())
            self.assertEqual(
                constants.SHARE_GROUP_SIMPLE_KEYS,
                keys,
                'Incorrect keys returned for share group %s. '
                'Expected: %s, found %s' % (
                    sg['id'],
                    constants.SHARE_GROUP_SIMPLE_KEYS,
                    ','.join(keys)))

        # Share group ids are in list exactly once
        for sg_id in (self.share_group["id"], self.share_group2["id"]):
            gen = [sg["id"] for sg in share_groups if sg["id"] == sg_id]
            msg = ("Expected id %s exactly once in share group list" % sg_id)
            self.assertEqual(1, len(gen), msg)

    @decorators.idempotent_id('16986c21-ecbc-429e-ab3d-8d1596a3eac4')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION, '2.36',
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_list_share_groups_with_detail_min(self, version):
        self.skip_if_microversion_not_supported(version)
        params = None
        if utils.is_microversion_ge(version, '2.36'):
            params = {'name~': 'tempest', 'description~': 'tempest'}
        # List share groups
        share_groups = self.shares_v2_client.list_share_groups(
            detailed=True, params=params, version=version)

        # Verify keys
        for sg in share_groups:
            keys = set(sg.keys())
            self.assertTrue(
                constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(
                    keys),
                'Not all required keys returned for share group %s.  '
                'Expected at least: %s, found %s' % (
                    sg['id'],
                    constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                    ','.join(keys),
                )
            )

        # Share group ids are in list exactly once
        for group_id in (self.share_group["id"], self.share_group2["id"]):
            gen = [share_group["id"] for share_group in share_groups
                   if share_group["id"] == group_id]
            msg = ("Expected id %s exactly once in share group list" %
                   group_id)
            self.assertEqual(1, len(gen), msg)

    @decorators.idempotent_id('e72be2f9-56db-467f-89d7-0dddbf7e37e9')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_filter_shares_by_share_group_id_min(self):
        shares = self.shares_v2_client.list_shares(
            detailed=True,
            params={'share_group_id': self.share_group['id']},
            version=constants.MIN_SHARE_GROUP_MICROVERSION,
        )

        share_ids = [share['id'] for share in shares]

        self.assertEqual(
            2, len(shares),
            'Incorrect number of shares returned. '
            'Expected 2, got %s' % len(shares))
        self.assertIn(
            self.shares[0]['id'], share_ids,
            'Share %s expected in returned list, but got %s' % (
                self.shares[0]['id'], share_ids))
        self.assertIn(
            self.shares[1]['id'], share_ids,
            'Share %s expected in returned list, but got %s' % (
                self.shares[0]['id'], share_ids))

    @decorators.idempotent_id('5d2ca4f5-04da-4528-af47-ec980b95e884')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_get_share_group_snapshot(self, version):
        self.skip_if_microversion_not_supported(version)

        # Get share group snapshot
        sg_snapshot = self.shares_v2_client.get_share_group_snapshot(
            self.sg_snapshot['id'],
            version=version,
        )

        # Verify keys
        actual_keys = set(sg_snapshot.keys())
        self.assertTrue(
            constants.SHARE_GROUP_SNAPSHOT_DETAIL_REQUIRED_KEYS.issubset(
                actual_keys),
            'Not all required keys returned for share group %s.  '
            'Expected at least: %s, found %s' % (
                sg_snapshot['id'],
                constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                actual_keys,
            )
        )

        # Verify values
        self.assertEqual(self.sg_snap_name, sg_snapshot["name"])
        self.assertEqual(self.sg_snap_desc, sg_snapshot["description"])

    @decorators.idempotent_id('67e8c099-f1c1-4972-9c51-bb7bfe1d7994')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_get_share_group_snapshot_members_min(self):
        sg_snapshot = self.shares_v2_client.get_share_group_snapshot(
            self.sg_snapshot['id'],
            version=constants.MIN_SHARE_GROUP_MICROVERSION,
        )
        sg_snapshot_members = sg_snapshot['members']
        member_share_ids = [m['share_id'] for m in sg_snapshot_members]
        self.assertEqual(
            2, len(sg_snapshot_members),
            'Unexpected number of share group snapshot members. '
            'Expected 2, got %s.' % len(sg_snapshot_members))
        # Verify each share is represented in the share group snapshot
        # appropriately
        for share_id in (self.shares[0]['id'], self.shares[1]['id']):
            self.assertIn(
                share_id, member_share_ids,
                'Share missing %s missing from share group '
                'snapshot. Found %s.' % (share_id, member_share_ids))
        for share in (self.shares[0], self.shares[1]):
            for member in sg_snapshot_members:
                if share['id'] == member['share_id']:
                    self.assertEqual(share['size'], member['size'])

    @decorators.idempotent_id('650c5fa7-11f2-48bd-b012-fc2e32b6f446')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_create_share_group_from_populated_share_group_snapshot(self,
                                                                    version):
        self.skip_if_microversion_not_supported(version)

        sg_snapshot = self.shares_v2_client.get_share_group_snapshot(
            self.sg_snapshot['id'],
            version=version,
        )
        snapshot_members = sg_snapshot['members']

        new_share_group = self.create_share_group(
            cleanup_in_class=False,
            source_share_group_snapshot_id=self.sg_snapshot['id'],
            version=version,
            share_group_type_id=self.share_group_type_id,
        )

        new_share_group = self.shares_v2_client.get_share_group(
            new_share_group['id'],
            version=version,
        )

        # Verify that share_network information matches source share group
        self.assertEqual(
            self.share_group['share_network_id'],
            new_share_group['share_network_id'])

        new_shares = self.shares_v2_client.list_shares(
            params={'share_group_id': new_share_group['id']},
            detailed=True,
            version=version,
        )

        # Verify each new share is available
        for share in new_shares:
            self.assertEqual(
                'available', share['status'],
                'Share %s is not in available status.' % share['id'])

        # Verify each sgsnapshot member is represented in the new sg
        # appropriately
        share_source_member_ids = [
            share['source_share_group_snapshot_member_id']
            for share in new_shares]
        for member in snapshot_members:
            self.assertIn(
                member['id'], share_source_member_ids,
                'Share group snapshot member %s not represented by '
                'share group %s.' % (member['id'], new_share_group['id']))
            for share in new_shares:
                if (share['source_share_group_snapshot_member_id'] == (
                        member['id'])):
                    self.assertEqual(member['size'], share['size'])
                    self.assertEqual(
                        self.share_group['share_network_id'],
                        share['share_network_id'])


@ddt.ddt
class ShareGroupRenameTest(base.BaseSharesMixedTest):

    @classmethod
    def skip_checks(cls):
        super(ShareGroupRenameTest, cls).skip_checks()
        if not CONF.share.run_share_group_tests:
            raise cls.skipException('Share Group tests disabled.')

        utils.check_skip_if_microversion_lt(
            constants.MIN_SHARE_GROUP_MICROVERSION)

    @classmethod
    def resource_setup(cls):
        super(ShareGroupRenameTest, cls).resource_setup()

        # Create a share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

        # Create a share group type
        cls.share_group_type = cls._create_share_group_type()
        cls.share_group_type_id = cls.share_group_type['id']

        # Create share group
        cls.share_group_name = data_utils.rand_name("tempest-sg-name")
        cls.share_group_desc = data_utils.rand_name("tempest-sg-description")
        cls.share_group = cls.create_share_group(
            name=cls.share_group_name,
            description=cls.share_group_desc,
            share_group_type_id=cls.share_group_type_id,
            share_type_ids=[cls.share_type_id]
        )

    def _rollback_share_group_update(self, version):
        self.shares_v2_client.update_share_group(
            self.share_group["id"],
            name=self.share_group_name,
            description=self.share_group_desc,
            version=version,
        )

    @decorators.idempotent_id('7f0a07ce-afdd-4c51-a29c-d8fe6cb5f6a5')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_update_share_group(self, version):
        self.skip_if_microversion_not_supported(version)

        # Get share_group
        share_group = self.shares_v2_client.get_share_group(
            self.share_group['id'],
            version=version
        )
        self.assertEqual(self.share_group_name, share_group["name"])
        self.assertEqual(self.share_group_desc, share_group["description"])

        # Update share_group
        new_name = data_utils.rand_name("tempest-new-name")
        new_desc = data_utils.rand_name("tempest-new-description")
        updated = self.shares_v2_client.update_share_group(
            share_group["id"],
            name=new_name,
            description=new_desc,
            version=version,
        )
        self.assertEqual(new_name, updated["name"])
        self.assertEqual(new_desc, updated["description"])

        # Get share_group
        share_group = self.shares_v2_client.get_share_group(
            self.share_group['id'],
            version=version,
        )
        self.assertEqual(new_name, share_group["name"])
        self.assertEqual(new_desc, share_group["description"])

        # Rollback the update since this is a ddt and the class resources are
        # going to be reused
        self._rollback_share_group_update(version)

    @decorators.idempotent_id('611b1555-df09-499b-8aef-e8261e3f6863')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_create_update_read_share_group_with_unicode(self, version):
        self.skip_if_microversion_not_supported(version)

        value1 = u'ಠ_ಠ'
        value2 = u'ಠ_ರೃ'

        # Create share_group
        share_group = self.create_share_group(
            cleanup_in_class=False,
            name=value1,
            description=value1,
            version=version,
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id]
        )
        self.assertEqual(value1, share_group["name"])
        self.assertEqual(value1, share_group["description"])

        # Update share group
        updated = self.shares_v2_client.update_share_group(
            share_group["id"],
            name=value2,
            description=value2,
            version=version,
        )
        self.assertEqual(value2, updated["name"])
        self.assertEqual(value2, updated["description"])

        # Get share group
        share_group = self.shares_v2_client.get_share_group(
            share_group['id'], version=version)
        self.assertEqual(value2, share_group["name"])
        self.assertEqual(value2, share_group["description"])

        # Rollback the update since this is a ddt and the class resources are
        # going to be reused
        self._rollback_share_group_update(version)
