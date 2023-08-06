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
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF


@ddt.ddt
class ShareGroupsTest(base.BaseSharesMixedTest):
    """Covers share group functionality."""

    @classmethod
    def skip_checks(cls):
        super(ShareGroupsTest, cls).skip_checks()
        if not CONF.share.run_share_group_tests:
            raise cls.skipException('Share Group tests disabled.')

        utils.check_skip_if_microversion_lt(
            constants.MIN_SHARE_GROUP_MICROVERSION)

    @classmethod
    def resource_setup(cls):
        super(ShareGroupsTest, cls).resource_setup()
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

        # create share group type
        cls.share_group_type = cls._create_share_group_type()
        cls.share_group_type_id = cls.share_group_type['id']

    @decorators.idempotent_id('809d5e3d-5a4b-458a-a985-853d59800da5')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_populate_delete_share_group_min(self):
        # Create a share group
        share_group = self.create_share_group(
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION,
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id],
        )

        keys = set(share_group.keys())
        self.assertTrue(
            constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(keys),
            'At least one expected element missing from share group '
            'response. Expected %(expected)s, got %(actual)s.' % {
                "expected": constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                "actual": keys}
        )
        # Populate
        share = self.create_share(
            share_type_id=self.share_type_id,
            share_group_id=share_group['id'],
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Delete
        params = {"share_group_id": share_group['id']}
        self.shares_v2_client.delete_share(
            share['id'],
            params=params,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)
        self.shares_client.wait_for_resource_deletion(share_id=share['id'])
        self.shares_v2_client.delete_share_group(
            share_group['id'], version=constants.MIN_SHARE_GROUP_MICROVERSION)
        self.shares_v2_client.wait_for_resource_deletion(
            share_group_id=share_group['id'])

        # Verify
        self.assertRaises(
            lib_exc.NotFound,
            self.shares_v2_client.get_share_group, share_group['id'])
        self.assertRaises(
            lib_exc.NotFound, self.shares_client.get_share, share['id'])

    @decorators.idempotent_id('cf7984af-1e1d-4eaf-bf9a-d8ddf5cebd01')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_delete_empty_share_group_snapshot_min(self):
        # Create base share group
        share_group = self.create_share_group(
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id],
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Create share group snapshot
        sg_snapshot = self.create_share_group_snapshot_wait_for_active(
            share_group["id"],
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        keys = set(sg_snapshot.keys())
        self.assertTrue(
            constants.SHARE_GROUP_SNAPSHOT_DETAIL_REQUIRED_KEYS.issubset(keys),
            'At least one expected element missing from share group snapshot '
            'response. Expected %(e)s, got %(a)s.' % {
                "e": constants.SHARE_GROUP_SNAPSHOT_DETAIL_REQUIRED_KEYS,
                "a": keys})

        sg_snapshot_members = sg_snapshot['members']
        self.assertEmpty(
            sg_snapshot_members,
            'Expected 0 share_group_snapshot members, got %s' % len(
                sg_snapshot_members))

        # Delete snapshot
        self.shares_v2_client.delete_share_group_snapshot(
            sg_snapshot["id"], version=constants.MIN_SHARE_GROUP_MICROVERSION)
        self.shares_v2_client.wait_for_resource_deletion(
            share_group_snapshot_id=sg_snapshot["id"])
        self.assertRaises(
            lib_exc.NotFound,
            self.shares_v2_client.get_share_group_snapshot,
            sg_snapshot['id'],
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

    @decorators.idempotent_id('727d9c69-4c3b-4375-a91b-8b3efd349976')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_share_group_from_empty_share_group_snapshot_min(self):
        # Create base share group
        share_group = self.create_share_group(
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id],
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Create share group snapshot
        sg_snapshot = self.create_share_group_snapshot_wait_for_active(
            share_group["id"], cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        snapshot_members = sg_snapshot['members']

        self.assertEmpty(
            snapshot_members,
            'Expected 0 share group snapshot members, got %s' %
            len(snapshot_members))

        new_share_group = self.create_share_group(
            share_group_type_id=self.share_group_type_id,
            cleanup_in_class=False,
            source_share_group_snapshot_id=sg_snapshot['id'],
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        new_shares = self.shares_v2_client.list_shares(
            params={'share_group_id': new_share_group['id']},
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        self.assertEmpty(
            new_shares, 'Expected 0 new shares, got %s' % len(new_shares))

        msg = ('Expected source_ishare_group_snapshot_id %s '
               'as source of share group %s' % (
                   sg_snapshot['id'],
                   new_share_group['source_share_group_snapshot_id']))
        self.assertEqual(
            new_share_group['source_share_group_snapshot_id'],
            sg_snapshot['id'],
            msg)

        msg = ('Unexpected share_types on new share group. Expected '
               '%s, got %s.' % (share_group['share_types'],
                                new_share_group['share_types']))
        self.assertEqual(
            sorted(share_group['share_types']),
            sorted(new_share_group['share_types']), msg)

        # Assert the share_network information is the same
        msg = 'Expected share_network %s as share_network of cg %s' % (
            share_group['share_network_id'],
            new_share_group['share_network_id'])
        self.assertEqual(
            share_group['share_network_id'],
            new_share_group['share_network_id'],
            msg)

    @base.skip_if_microversion_lt("2.34")
    @decorators.idempotent_id('14fd6d88-87ff-4af2-ad17-f95dbd8dcd61')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        'sg', 'sg_and_share', 'none',
    )
    def test_create_sg_and_share_specifying_az(self, where_specify_az):
        # Get list of existing availability zones, at least one always
        # should exist
        azs = self.get_availability_zones_matching_share_type(
            self.share_type)

        sg_kwargs = {
            'share_group_type_id': self.share_group_type_id,
            'share_type_ids': [self.share_type_id],
            'version': '2.34',
            'cleanup_in_class': False,
        }
        if where_specify_az in ('sg', 'sg_and_share'):
            sg_kwargs['availability_zone'] = azs[0]

        # Create share group
        share_group = self.create_share_group(**sg_kwargs)

        # Get latest share group info
        share_group = self.shares_v2_client.get_share_group(
            share_group['id'], '2.34')

        self.assertIn('availability_zone', share_group)
        if where_specify_az in ('sg', 'sg_and_share'):
            self.assertEqual(azs[0], share_group['availability_zone'])
        else:
            self.assertIn(share_group['availability_zone'], azs)

        # Test 'consistent_snapshot_support' as part of 2.33 API change
        self.assertIn('consistent_snapshot_support', share_group)
        self.assertIn(
            share_group['consistent_snapshot_support'], ('host', 'pool', None))

        s_kwargs = {
            'share_type_id': self.share_type_id,
            'share_group_id': share_group['id'],
            'version': '2.33',
            'cleanup_in_class': False,
        }
        if where_specify_az == 'sg_and_share':
            s_kwargs['availability_zone'] = azs[0]

        # Create share in share group
        share = self.create_share(**s_kwargs)

        # Get latest share info
        share = self.shares_v2_client.get_share(share['id'], '2.34')

        # Verify that share always has the same AZ as share group does
        self.assertEqual(
            share_group['availability_zone'], share['availability_zone'])
