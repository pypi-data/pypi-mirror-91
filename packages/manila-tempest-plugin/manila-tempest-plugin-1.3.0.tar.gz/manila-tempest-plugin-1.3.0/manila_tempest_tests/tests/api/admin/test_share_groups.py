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
from tempest.lib import exceptions
import testtools
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF
LATEST_MICROVERSION = CONF.share.max_api_microversion


@ddt.ddt
class ShareGroupsTest(base.BaseSharesAdminTest):

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
        # Create 2 share_types
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

        cls.share_type2 = cls._create_share_type()
        cls.share_type_id2 = cls.share_type2['id']

        # Create a share group type
        name = data_utils.rand_name("unique_sgt_name")
        cls.sg_type = cls.create_share_group_type(
            name=name,
            share_types=[cls.share_type_id, cls.share_type_id2],
            cleanup_in_class=True,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)
        cls.sg_type_id = cls.sg_type['id']

    @decorators.idempotent_id('79eaa86f-4c8f-49fd-acb2-ec051aa6bf93')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_create_share_group_with_single_share_type_min(self, version):
        self.skip_if_microversion_not_supported(version)
        share_group = self.create_share_group(
            share_group_type_id=self.sg_type_id,
            cleanup_in_class=False,
            share_type_ids=[self.share_type_id],
            version=version)

        keys = set(share_group.keys())
        self.assertTrue(
            constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(keys),
            'At least one expected element missing from share group '
            'response. Expected %(expected)s, got %(actual)s.' % {
                "expected": constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                "actual": keys})

        actual_sg_type = share_group['share_group_type_id']
        expected_sg_type = self.sg_type_id
        self.assertEqual(
            expected_sg_type, actual_sg_type,
            'Incorrect share group type applied to share group '
            '%s. Expected %s, got %s' % (
                share_group['id'], expected_sg_type, actual_sg_type))

        actual_share_types = share_group['share_types']
        expected_share_types = [self.share_type_id]
        self.assertEqual(
            sorted(expected_share_types),
            sorted(actual_share_types),
            'Incorrect share types applied to share group %s. '
            'Expected %s, got %s' % (
                share_group['id'], expected_share_types, actual_share_types))

    @decorators.idempotent_id('ff6c17af-03ba-4506-923d-b6c229492d0e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_share_group_with_multiple_share_types_min(self):
        share_group = self.create_share_group(
            share_group_type_id=self.sg_type_id,
            cleanup_in_class=False,
            share_type_ids=[self.share_type_id, self.share_type_id2],
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        keys = set(share_group.keys())
        self.assertTrue(
            constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(keys),
            'At least one expected element missing from share group '
            'response. Expected %(expected)s, got %(actual)s.' % {
                "expected": constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                "actual": keys})

        actual_sg_type = share_group['share_group_type_id']
        expected_sg_type = self.sg_type_id
        self.assertEqual(
            expected_sg_type, actual_sg_type,
            'Incorrect share group type applied to share group %s. '
            'Expected %s, got %s' % (
                share_group['id'], expected_sg_type, actual_sg_type))

        actual_share_types = share_group['share_types']
        expected_share_types = [self.share_type_id, self.share_type_id2]
        self.assertEqual(
            sorted(expected_share_types),
            sorted(actual_share_types),
            'Incorrect share types applied to share group %s. '
            'Expected %s, got %s' % (
                share_group['id'], expected_share_types, actual_share_types))

    @decorators.idempotent_id('99f0471c-e978-42ac-b50b-848b16692eab')
    @testtools.skipUnless(
        CONF.share.default_share_type_name, "Only if defaults are defined.")
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(
        *utils.deduplicate([constants.MIN_SHARE_GROUP_MICROVERSION,
                            constants.SHARE_GROUPS_GRADUATION_VERSION,
                            LATEST_MICROVERSION]))
    def test_default_share_group_type_applied(self, version):
        self.skip_if_microversion_not_supported(version)
        try:
            default_type = self.shares_v2_client.get_default_share_group_type(
                version=version
            )
        except exceptions.NotFound:
            msg = "There is no default share group type"
            raise self.skipException(msg)
        default_share_types = default_type['share_types']

        share_group = self.create_share_group(
            cleanup_in_class=False,
            share_type_ids=default_share_types,
            version=version)

        keys = set(share_group.keys())
        self.assertTrue(
            constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS.issubset(keys),
            'At least one expected element missing from share group '
            'response. Expected %(expected)s, got %(actual)s.' % {
                "expected": constants.SHARE_GROUP_DETAIL_REQUIRED_KEYS,
                "actual": keys})

        actual_sg_type = share_group['share_group_type_id']
        expected_sg_type = default_type['id']
        self.assertEqual(
            expected_sg_type, actual_sg_type,
            'Incorrect share group type applied to share group %s. '
            'Expected %s, got %s' % (
                share_group['id'], expected_sg_type, actual_sg_type))

    @decorators.idempotent_id('8ca1f0a0-2a36-4adb-af6b-6741b00307c5')
    @testtools.skipUnless(
        CONF.share.multitenancy_enabled, "Only for multitenancy.")
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_sg_from_snapshot_verify_share_server_information_min(self):
        # Create a share group
        orig_sg = self.create_share_group(
            share_group_type_id=self.sg_type_id,
            cleanup_in_class=False,
            share_type_ids=[self.share_type_id],
            version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Get latest share group information
        orig_sg = self.shares_v2_client.get_share_group(
            orig_sg['id'], version=constants.MIN_SHARE_GROUP_MICROVERSION)

        # Assert share server information
        self.assertIsNotNone(orig_sg['share_network_id'])
        self.assertIsNotNone(orig_sg['share_server_id'])

        sg_snapshot = self.create_share_group_snapshot_wait_for_active(
            orig_sg['id'], cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION)
        new_sg = self.create_share_group(
            share_group_type_id=self.sg_type_id,
            cleanup_in_class=False,
            version=constants.MIN_SHARE_GROUP_MICROVERSION,
            source_share_group_snapshot_id=sg_snapshot['id'])

        # Assert share server information
        self.assertEqual(
            orig_sg['share_network_id'], new_sg['share_network_id'])
        self.assertEqual(
            orig_sg['share_server_id'], new_sg['share_server_id'])

    @decorators.idempotent_id('93fd4a97-a25a-4a17-b5ae-c8894c1adfc5')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_create_sg_with_sg_type_but_without_any_group_specs(self):
        # Create share group type not specifying any group specs
        sg_type = self.create_share_group_type(
            name=data_utils.rand_name("tempest-manila"),
            share_types=[self.share_type_id],
            group_specs={},
            cleanup_in_class=False)

        # Create share group, it should be created always, because we do not
        # restrict choice anyhow.
        self.create_share_group(
            share_type_ids=[self.share_type_id],
            share_group_type_id=sg_type['id'],
            cleanup_in_class=False)
