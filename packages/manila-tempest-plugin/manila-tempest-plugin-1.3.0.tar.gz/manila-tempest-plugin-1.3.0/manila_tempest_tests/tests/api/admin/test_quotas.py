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
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
import testtools
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF
PRE_SHARE_GROUPS_MICROVERSION = "2.39"
SHARE_GROUPS_MICROVERSION = "2.40"
PRE_SHARE_REPLICA_QUOTAS_MICROVERSION = "2.52"
SHARE_REPLICA_QUOTAS_MICROVERSION = "2.53"


@ddt.ddt
class SharesAdminQuotasTest(base.BaseSharesAdminTest):

    @classmethod
    def resource_setup(cls):
        if not CONF.share.run_quota_tests:
            msg = "Quota tests are disabled."
            raise cls.skipException(msg)
        super(SharesAdminQuotasTest, cls).resource_setup()
        cls.client = cls.shares_v2_client
        cls.user_id = cls.client.user_id
        cls.tenant_id = cls.client.tenant_id
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

    @decorators.idempotent_id('f62c48e3-9736-4f0c-9f9b-f139f393ac0a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_default_quotas(self):
        quotas = self.client.default_quotas(self.tenant_id)
        self.assertGreater(int(quotas["gigabytes"]), -2)
        self.assertGreater(int(quotas["snapshot_gigabytes"]), -2)
        self.assertGreater(int(quotas["shares"]), -2)
        self.assertGreater(int(quotas["snapshots"]), -2)
        self.assertGreater(int(quotas["share_networks"]), -2)
        if utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION):
            self.assertGreater(int(quotas["share_groups"]), -2)
            self.assertGreater(int(quotas["share_group_snapshots"]), -2)
        if utils.share_replica_quotas_are_supported():
            self.assertGreater(int(quotas["share_replicas"]), -2)
            self.assertGreater(int(quotas["replica_gigabytes"]), -2)

    @decorators.idempotent_id('1ff57cfa-cd8d-495f-86eb-9fead307428e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_show_quotas(self):
        quotas = self.client.show_quotas(self.tenant_id)
        self.assertGreater(int(quotas["gigabytes"]), -2)
        self.assertGreater(int(quotas["snapshot_gigabytes"]), -2)
        self.assertGreater(int(quotas["shares"]), -2)
        self.assertGreater(int(quotas["snapshots"]), -2)
        self.assertGreater(int(quotas["share_networks"]), -2)
        if utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION):
            self.assertGreater(int(quotas["share_groups"]), -2)
            self.assertGreater(int(quotas["share_group_snapshots"]), -2)
        if utils.share_replica_quotas_are_supported():
            self.assertGreater(int(quotas["share_replicas"]), -2)
            self.assertGreater(int(quotas["replica_gigabytes"]), -2)

    @decorators.idempotent_id('9b96dd45-7c0d-41ee-88e4-600185f61358')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_show_quotas_for_user(self):
        quotas = self.client.show_quotas(
            self.tenant_id, self.user_id)
        self.assertGreater(int(quotas["gigabytes"]), -2)
        self.assertGreater(int(quotas["snapshot_gigabytes"]), -2)
        self.assertGreater(int(quotas["shares"]), -2)
        self.assertGreater(int(quotas["snapshots"]), -2)
        self.assertGreater(int(quotas["share_networks"]), -2)
        if utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION):
            self.assertGreater(int(quotas["share_groups"]), -2)
            self.assertGreater(int(quotas["share_group_snapshots"]), -2)
        if utils.share_replica_quotas_are_supported():
            self.assertGreater(int(quotas["share_replicas"]), -2)
            self.assertGreater(int(quotas["replica_gigabytes"]), -2)

    @decorators.idempotent_id('2e98a13e-b2ed-4977-bafe-47ea48b504f2')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_not_supported(PRE_SHARE_GROUPS_MICROVERSION)
    def test_show_sg_quotas_using_too_old_microversion(self):
        quotas = self.client.show_quotas(
            self.tenant_id, version=PRE_SHARE_GROUPS_MICROVERSION)

        for key in ('share_groups', 'share_group_snapshots'):
            self.assertNotIn(key, quotas)

    @decorators.idempotent_id('b8bcbc04-68fb-4c8f-9f4c-a3b6c6b8911c')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_not_supported(PRE_SHARE_GROUPS_MICROVERSION)
    def test_show_sg_quotas_for_user_using_too_old_microversion(self):
        quotas = self.client.show_quotas(
            self.tenant_id, self.user_id,
            version=PRE_SHARE_GROUPS_MICROVERSION)

        for key in ('share_groups', 'share_group_snapshots'):
            self.assertNotIn(key, quotas)

    @decorators.idempotent_id('19fe431b-e83e-4c4e-acb8-018d7a470c8b')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_not_supported(
        PRE_SHARE_REPLICA_QUOTAS_MICROVERSION)
    def test_show_replica_quotas_for_user_using_too_old_microversion(self):
        quotas = self.client.show_quotas(
            self.tenant_id, self.user_id,
            version=PRE_SHARE_REPLICA_QUOTAS_MICROVERSION)

        for key in ('share_replicas', 'replica_gigabytes'):
            self.assertNotIn(key, quotas)

    @ddt.data(
        ('id', True),
        ('name', False),
    )
    @ddt.unpack
    @decorators.idempotent_id('836e1725-2853-4d54-b281-8173773d8527')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_lt("2.39")
    def test_show_share_type_quotas(self, share_type_key, is_st_public):
        # Check if the used microversion supports 'share_replica' and
        # 'replica_gigabytes' quotas
        replica_quotas_supported = utils.share_replica_quotas_are_supported()

        # Create share type
        share_type = self.create_share_type(
            data_utils.rand_name("tempest-manila"),
            is_public=is_st_public,
            cleanup_in_class=False,
            extra_specs=self.add_extra_specs_to_dict(),
        )
        if 'share_type' in share_type:
            share_type = share_type['share_type']

        keys = ['shares', 'gigabytes', 'snapshots', 'snapshot_gigabytes']

        if replica_quotas_supported:
            keys.append('share_replicas')
            keys.append('replica_gigabytes')

        # Get current project quotas
        p_quotas = self.client.show_quotas(self.tenant_id)

        # Get current share type quotas
        st_quotas = self.client.show_quotas(
            self.tenant_id, share_type=share_type[share_type_key])

        # Share type quotas have values equal to project's
        for key in keys:
            self.assertEqual(st_quotas[key], p_quotas[key])

        # Verify that we do not have share groups related quotas
        # for share types.
        for key in ('share_groups', 'share_group_snapshots'):
            self.assertNotIn(key, st_quotas)


@ddt.ddt
class SharesAdminQuotasUpdateTest(base.BaseSharesAdminTest):

    # We want to force a fresh project for this test class, since we'll be
    # manipulating project quotas - and any pre-existing projects may have
    # resources, quotas and the like that might interfere with our test cases.
    force_tenant_isolation = True

    @classmethod
    def skip_checks(cls):
        super(SharesAdminQuotasUpdateTest, cls).skip_checks()
        if not CONF.auth.use_dynamic_credentials:
            raise cls.skipException('Dynamic credentials are required')
        if not CONF.share.run_quota_tests:
            msg = "Quota tests are disabled."
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        super(SharesAdminQuotasUpdateTest, cls).resource_setup()
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']
        # create share group type
        cls.share_group_type = cls._create_share_group_type()
        cls.share_group_type_id = cls.share_group_type['id']
        cls.client = cls.shares_v2_client
        cls.tenant_id = cls.client.tenant_id
        cls.user_id = cls.client.user_id

    @decorators.idempotent_id('da16e906-e8e6-4aa0-9fc1-76ed48cfd428')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_tenant_quota_shares(self):
        # get current quotas
        quotas = self.client.show_quotas(self.tenant_id)
        new_quota = int(quotas["shares"]) + 2

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id, shares=new_quota)

        self.assertEqual(new_quota, int(updated["shares"]))

    @ddt.data(
        "share_groups",
        "share_group_snapshots",
    )
    @decorators.idempotent_id('cb09de7e-94e9-401a-b82b-8b2de210f8b9')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @testtools.skipUnless(
        CONF.share.run_share_group_tests, 'Share Group tests disabled.')
    @utils.skip_if_microversion_not_supported(SHARE_GROUPS_MICROVERSION)
    def test_update_tenant_quota_share_groups(self, quota_key):
        # Get current quotas
        quotas = self.client.show_quotas(self.tenant_id)
        new_quota = int(quotas[quota_key]) + 2

        # Set new quota
        updated = self.update_quotas(self.tenant_id, **{quota_key: new_quota})

        self.assertEqual(new_quota, int(updated[quota_key]))

    @decorators.idempotent_id('2c7f9e19-268d-4420-a046-a7faf21174a1')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quota_shares(self):
        # get current quotas
        quotas = self.client.show_quotas(self.tenant_id, self.user_id)
        new_quota = int(quotas["shares"]) - 1

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     shares=new_quota)

        self.assertEqual(new_quota, int(updated["shares"]))

    @ddt.data(
        "share_groups",
        "share_group_snapshots",
    )
    @decorators.idempotent_id('c32a716b-f971-4855-97ea-f30d4423d03d')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @testtools.skipUnless(
        CONF.share.run_share_group_tests, 'Share Group tests disabled.')
    @utils.skip_if_microversion_not_supported(SHARE_GROUPS_MICROVERSION)
    def test_update_user_quota_share_groups(self, quota_key):
        # Get current quotas
        quotas = self.client.show_quotas(self.tenant_id, self.user_id)
        new_quota = int(quotas[quota_key]) - 1

        # Set new quota
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     **{quota_key: new_quota})

        self.assertEqual(new_quota, int(updated[quota_key]))

    @ddt.data(("share_replicas", False),
              ("share_replicas", True),
              ("replica_gigabytes", False),
              ("replica_gigabytes", True),
              )
    @ddt.unpack
    @decorators.idempotent_id('af16dc89-c93d-43de-8902-2c88c75f107f')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_not_supported(SHARE_REPLICA_QUOTAS_MICROVERSION)
    def test_update_user_quota_replica_related(self, quota_key, use_user_id):
        kwargs = {}

        # Update the kwargs with user_id in case the user_id need to be
        # specified in the request
        kwargs.update({'user_id': self.user_id}) if use_user_id else None
        quotas = self.client.show_quotas(self.tenant_id, **kwargs)
        new_quota = int(quotas[quota_key]) - 1

        # Add the updated quota into the kwargs
        kwargs.update({quota_key: new_quota})

        # Set the new quota based on tenant or tenant and user_id
        updated = self.update_quotas(self.tenant_id, **kwargs)

        self.assertEqual(new_quota, int(updated[quota_key]))

    @ddt.data(
        ('id', True),
        ('name', False),
    )
    @ddt.unpack
    @decorators.idempotent_id('155ea3de-b3b5-4aa0-be8b-eebcc19ce874')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_lt("2.39")
    def test_update_share_type_quota(self, share_type_key, is_st_public):
        # Check if the used microversion supports 'share_replica' and
        # 'replica_gigabytes' quotas
        replica_quotas_supported = utils.share_replica_quotas_are_supported()
        share_type = self._create_share_type(is_public=is_st_public)

        # Get current quotas
        quotas = self.client.show_quotas(
            self.tenant_id, share_type=share_type[share_type_key])
        quota_keys = ['shares', 'gigabytes', 'snapshots', 'snapshot_gigabytes']

        if replica_quotas_supported:
            quota_keys.append('share_replicas')
            quota_keys.append('replica_gigabytes')

        # Update quotas
        for q in quota_keys:
            new_quota = int(quotas[q]) - 1

            # Set new quota, cleanup isn't necessary, share type will be
            # deleted when the test concludes, and that'll take care of
            # share type quotas
            updated = self.update_quotas(self.tenant_id,
                                         share_type=share_type[share_type_key],
                                         cleanup=False,
                                         **{q: new_quota})

            self.assertEqual(new_quota, int(updated[q]))

        current_quotas = self.client.show_quotas(
            self.tenant_id, share_type=share_type[share_type_key])

        for q in quota_keys:
            self.assertEqual(int(quotas[q]) - 1, current_quotas[q])

    @decorators.idempotent_id('78957d97-afad-4371-a21e-79641fff83f6')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_tenant_quota_snapshots(self):
        # get current quotas
        quotas = self.client.show_quotas(self.tenant_id)
        new_quota = int(quotas["snapshots"]) + 2

        # set new quota for snapshots
        updated = self.update_quotas(self.tenant_id, snapshots=new_quota)

        self.assertEqual(new_quota, int(updated["snapshots"]))

    @decorators.idempotent_id('53f4fd79-39aa-42be-82ce-e423ebffe837')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quota_snapshots(self):
        # get current quotas
        quotas = self.client.show_quotas(self.tenant_id, self.user_id)
        new_quota = int(quotas["snapshots"]) - 1

        # set new quota for snapshots
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     snapshots=new_quota)

        self.assertEqual(new_quota, int(updated["snapshots"]))

    @decorators.idempotent_id('37ee5bd2-db07-4817-b71a-7c3e78634399')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_tenant_quota_gigabytes(self):
        # get current quotas
        custom = self.client.show_quotas(self.tenant_id)

        # make quotas for update
        gigabytes = int(custom["gigabytes"]) + 2

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id, gigabytes=gigabytes)

        self.assertEqual(gigabytes, int(updated["gigabytes"]))

    @decorators.idempotent_id('284a2e95-48a1-4f1b-b952-f734b1b6238a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_tenant_quota_snapshot_gigabytes(self):
        # get current quotas
        custom = self.client.show_quotas(self.tenant_id)

        # make quotas for update
        snapshot_gigabytes = int(custom["snapshot_gigabytes"]) + 2

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id,
                                     snapshot_gigabytes=snapshot_gigabytes)

        self.assertEqual(snapshot_gigabytes,
                         int(updated["snapshot_gigabytes"]))

    @decorators.idempotent_id('75977d53-f06b-41a2-8365-0ce549e4a51a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quota_gigabytes(self):
        # get current quotas
        custom = self.client.show_quotas(self.tenant_id, self.user_id)

        # make quotas for update
        gigabytes = int(custom["gigabytes"]) - 1

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     gigabytes=gigabytes)

        self.assertEqual(gigabytes, int(updated["gigabytes"]))

    @decorators.idempotent_id('00a189fc-93ed-44c2-b9dc-1d9b6c26d005')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quota_snapshot_gigabytes(self):
        # get current quotas
        custom = self.client.show_quotas(self.tenant_id, self.user_id)

        # make quotas for update
        snapshot_gigabytes = int(custom["snapshot_gigabytes"]) - 1

        # set new quota for shares
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     snapshot_gigabytes=snapshot_gigabytes)

        self.assertEqual(snapshot_gigabytes,
                         int(updated["snapshot_gigabytes"]))

    @decorators.idempotent_id('da7f3179-f2f3-402e-82c2-e6855774a99a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_tenant_quota_share_networks(self):
        # get current quotas
        quotas = self.client.show_quotas(self.tenant_id)
        new_quota = int(quotas["share_networks"]) + 2

        # set new quota for share-networks
        updated = self.update_quotas(self.tenant_id, share_networks=new_quota)

        self.assertEqual(new_quota, int(updated["share_networks"]))

    @decorators.idempotent_id('f75f01a0-5921-44ab-b373-bb9e070f87eb')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quota_share_networks(self):
        # get current quotas
        quotas = self.client.show_quotas(
            self.tenant_id, self.user_id)
        new_quota = int(quotas["share_networks"]) - 1

        # set new quota for share-networks
        updated = self.update_quotas(self.tenant_id,
                                     user_id=self.user_id,
                                     share_networks=new_quota)

        self.assertEqual(new_quota, int(updated["share_networks"]))

    @decorators.idempotent_id('84e24c32-ee78-461e-ac1f-f9e4d99f88e2')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_reset_tenant_quotas(self):
        # Get default_quotas
        default = self.client.default_quotas(self.tenant_id)

        # Get current quotas
        custom = self.client.show_quotas(self.tenant_id)

        # Make quotas for update
        data = {
            "shares": int(custom["shares"]) + 2,
            "snapshots": int(custom["snapshots"]) + 2,
            "gigabytes": int(custom["gigabytes"]) + 2,
            "snapshot_gigabytes": int(custom["snapshot_gigabytes"]) + 2,
            "share_networks": int(custom["share_networks"]) + 2,
        }
        if (utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION) and
                CONF.share.run_share_group_tests):
            data["share_groups"] = int(custom["share_groups"]) + 2
            data["share_group_snapshots"] = (
                int(custom["share_group_snapshots"]) + 2)
        if utils.share_replica_quotas_are_supported():
            data["share_replicas"] = int(custom["share_replicas"]) + 2
            data["replica_gigabytes"] = int(custom["replica_gigabytes"]) + 2

        # set new quota, turn off cleanup - we'll do it right below
        updated = self.update_quotas(self.tenant_id, cleanup=False, **data)
        self.assertEqual(data["shares"], int(updated["shares"]))
        self.assertEqual(data["snapshots"], int(updated["snapshots"]))
        self.assertEqual(data["gigabytes"], int(updated["gigabytes"]))
        self.assertEqual(
            data["snapshot_gigabytes"], int(updated["snapshot_gigabytes"]))
        self.assertEqual(
            data["share_networks"], int(updated["share_networks"]))
        if (utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION) and
                CONF.share.run_share_group_tests):
            self.assertEqual(
                data["share_groups"], int(updated["share_groups"]))
            self.assertEqual(
                data["share_group_snapshots"],
                int(updated["share_group_snapshots"]))
        if utils.share_replica_quotas_are_supported():
            self.assertEqual(
                data["share_replicas"], int(updated["share_replicas"]))
            self.assertEqual(
                data["replica_gigabytes"], int(updated["replica_gigabytes"]))

        # Reset customized quotas
        self.client.reset_quotas(self.tenant_id)

        # Verify quotas
        reseted = self.client.show_quotas(self.tenant_id)
        self.assertEqual(int(default["shares"]), int(reseted["shares"]))
        self.assertEqual(int(default["snapshots"]), int(reseted["snapshots"]))
        self.assertEqual(int(default["gigabytes"]), int(reseted["gigabytes"]))
        self.assertEqual(
            int(default["snapshot_gigabytes"]),
            int(reseted["snapshot_gigabytes"]))
        self.assertEqual(
            int(default["share_networks"]), int(reseted["share_networks"]))
        if (utils.is_microversion_supported(SHARE_GROUPS_MICROVERSION) and
                CONF.share.run_share_group_tests):
            self.assertEqual(
                int(default["share_groups"]), int(reseted["share_groups"]))
            self.assertEqual(
                int(default["share_group_snapshots"]),
                int(reseted["share_group_snapshots"]))
        if utils.share_replica_quotas_are_supported():
            self.assertEqual(
                int(default["share_replicas"]), int(reseted["share_replicas"]))
            self.assertEqual(
                int(default["replica_gigabytes"]),
                int(reseted["replica_gigabytes"]))

    def _get_new_replica_quota_values(self, default_quotas, value_to_set):
        new_values = {
            'share_replicas': int(
                default_quotas['share_replicas']) + value_to_set,
            'replica_gigabytes': int(
                default_quotas['replica_gigabytes']) + value_to_set
        }
        return new_values

    @ddt.data(
        ('id', True),
        ('name', False),
    )
    @ddt.unpack
    @decorators.idempotent_id('15e57302-5a14-4be4-8720-95b639c2bfad')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_lt("2.39")
    def test_reset_share_type_quotas(self, share_type_key, is_st_public):
        share_type = self._create_share_type(is_public=is_st_public)
        quota_keys = ['shares', 'snapshots', 'gigabytes', 'snapshot_gigabytes']

        # get default_quotas
        default_quotas = self.client.default_quotas(self.tenant_id)

        kwargs = {}

        # check if the replica_gigabytes and share_replicas quotas are
        # supported
        if utils.share_replica_quotas_are_supported():
            kwargs.update(self._get_new_replica_quota_values(
                default_quotas, 5))
            quota_keys.append('share_replicas')
            quota_keys.append('replica_gigabytes')

        # set new project quota
        updated_p_quota = self.update_quotas(
            self.tenant_id,
            shares=int(default_quotas['shares']) + 5,
            snapshots=int(default_quotas['snapshots']) + 5,
            gigabytes=int(default_quotas['gigabytes']) + 5,
            snapshot_gigabytes=int(default_quotas['snapshot_gigabytes']) + 5,
            **kwargs
        )

        if utils.share_replica_quotas_are_supported():
            kwargs.update(self._get_new_replica_quota_values(
                default_quotas, 3))

        # set share type quota for project, don't cleanup, we'll do that below
        self.update_quotas(
            self.tenant_id,
            share_type=share_type[share_type_key],
            shares=int(default_quotas['shares']) + 3,
            snapshots=int(default_quotas['snapshots']) + 3,
            gigabytes=int(default_quotas['gigabytes']) + 3,
            snapshot_gigabytes=int(default_quotas['snapshot_gigabytes']) + 3,
            cleanup=False,
            **kwargs
        )

        # reset share type quotas
        self.client.reset_quotas(
            self.tenant_id, share_type=share_type[share_type_key])

        # verify quotas
        current_p_quota = self.client.show_quotas(self.tenant_id)
        current_st_quota = self.client.show_quotas(
            self.tenant_id, share_type=share_type[share_type_key])
        for key in quota_keys:
            self.assertEqual(updated_p_quota[key], current_p_quota[key])

            # Default share type quotas are current project quotas
            self.assertNotEqual(default_quotas[key], current_st_quota[key])
            self.assertEqual(current_p_quota[key], current_st_quota[key])

    @decorators.idempotent_id('d4bba375-7111-4b93-b6dd-4f0532febc3e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_quota_for_shares(self):
        self.update_quotas(self.tenant_id, shares=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('shares'))

    @decorators.idempotent_id('756ffd0e-a476-49af-ac85-9bb4ce5e29b7')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_user_quota_for_shares(self):
        self.update_quotas(self.tenant_id, user_id=self.user_id, shares=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('shares'))

    @decorators.idempotent_id('9779d166-09d3-4745-8acc-2243eadec3ea')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_quota_for_snapshots(self):
        self.update_quotas(self.tenant_id, snapshots=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('snapshots'))

    @decorators.idempotent_id('245b3bf3-09ef-4b6d-8643-f156bf1bf23c')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_user_quota_for_snapshots(self):
        self.update_quotas(self.tenant_id, user_id=self.user_id, snapshots=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('snapshots'))

    @decorators.idempotent_id('b6a94e87-091a-48dc-9b51-13d81541869c')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_quota_for_gigabytes(self):
        self.update_quotas(self.tenant_id, gigabytes=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('gigabytes'))

    @decorators.idempotent_id('0d044db4-ae5b-416d-aa51-098afb72cd6c')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_quota_for_snapshot_gigabytes(self):
        self.update_quotas(self.tenant_id, snapshot_gigabytes=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('snapshot_gigabytes'))

    @decorators.idempotent_id('2de4b7cf-9189-413f-858b-860ecf5fd18b')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_user_quota_for_gigabytes(self):
        self.update_quotas(self.tenant_id, user_id=self.user_id, gigabytes=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('gigabytes'))

    @decorators.idempotent_id('cbe63027-1108-4779-9fd3-22f41f60d6bb')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_user_quota_for_snapshot_gigabytes(self):
        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           snapshot_gigabytes=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('snapshot_gigabytes'))

    @decorators.idempotent_id('e35455f5-92db-4669-ac21-9daf170df248')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_quota_for_share_networks(self):
        self.update_quotas(self.tenant_id, share_networks=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('share_networks'))

    @decorators.idempotent_id('66b04887-e611-4d4f-a40b-c8b14766b6af')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_unlimited_user_quota_for_share_networks(self):
        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           share_networks=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('share_networks'))

    @decorators.idempotent_id('7c2cd2d4-4352-4811-9e39-70f56e6297c2')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @testtools.skipUnless(
        CONF.share.run_share_group_tests, 'Share Group tests disabled.')
    @utils.skip_if_microversion_not_supported(SHARE_GROUPS_MICROVERSION)
    def test_unlimited_quota_for_share_groups(self):
        self.update_quotas(self.tenant_id, share_groups=-1)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get('share_groups'))

    @decorators.idempotent_id('76d270d5-f314-47cb-9c3f-409f8ff12ce2')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @testtools.skipUnless(
        CONF.share.run_share_group_tests, 'Share Group tests disabled.')
    @utils.skip_if_microversion_not_supported(SHARE_GROUPS_MICROVERSION)
    def test_unlimited_user_quota_for_share_group_snapshots(self):
        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           share_group_snapshots=-1)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get('share_group_snapshots'))

    @ddt.data("share_replicas", "replica_gigabytes")
    @decorators.idempotent_id('15aa5df5-b2ae-4a3a-acb8-efbbc84581be')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @utils.skip_if_microversion_not_supported(
        SHARE_REPLICA_QUOTAS_MICROVERSION)
    def test_unlimited_quota_for_replica_quotas(self, quota_key):
        kwargs = {quota_key: -1}
        self.update_quotas(self.tenant_id, **kwargs)

        quotas = self.client.show_quotas(self.tenant_id)

        self.assertEqual(-1, quotas.get(quota_key))

    @ddt.data("share_replicas", "replica_gigabytes")
    @decorators.idempotent_id('84b99731-f748-44fe-a291-162d05da9e25')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @utils.skip_if_microversion_not_supported(
        SHARE_REPLICA_QUOTAS_MICROVERSION)
    def test_unlimited_user_quota_for_replica_quotas(self, quota_key):
        kwargs = {quota_key: -1}
        self.update_quotas(self.tenant_id, user_id=self.user_id, **kwargs)

        quotas = self.client.show_quotas(self.tenant_id, self.user_id)

        self.assertEqual(-1, quotas.get(quota_key))

    @ddt.data(11, -1)
    @decorators.idempotent_id('43f58705-3cad-46bc-816c-41e8fa55dd8d')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_user_quotas_bigger_than_project_quota(self, user_quota):
        self.update_quotas(self.tenant_id, shares=10)

        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           force=True,
                           shares=user_quota)

    @ddt.data(11, -1)
    @decorators.idempotent_id('315cb76f-920d-4cb9-ac7d-16be8e95e1b2')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_lt("2.39")
    def test_update_share_type_quotas_bigger_than_project_quota(self, st_q):
        share_type = self._create_share_type()

        self.update_quotas(self.tenant_id, shares=10)

        # no need to cleanup share type quota, share type will be deleted at
        # the end of the test
        self.update_quotas(self.tenant_id,
                           share_type=share_type['name'],
                           force=True,
                           cleanup=False,
                           shares=st_q)

    @decorators.idempotent_id('c95be1eb-6331-4c37-9fac-ed6c36270457')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @base.skip_if_microversion_lt("2.39")
    def test_set_share_type_quota_bigger_than_users_quota(self):
        share_type = self._create_share_type()

        self.update_quotas(self.tenant_id, force=False, shares=13)

        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           force=True,
                           shares=11)

        # Share type quota does not depend on user's quota, so we should be
        # able to update it. No need for cleanup, since the share type will
        # be deleted when the test completes, cleaning up quotas and usages
        self.update_quotas(self.tenant_id,
                           share_type=share_type['name'],
                           force=False,
                           cleanup=False,
                           shares=12)

    @decorators.idempotent_id('4687eb25-17b3-4995-ace2-62f8bda29c57')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @base.skip_if_microversion_lt("2.39")
    def test_quotas_usages(self):
        # Create share types
        st_1, st_2 = (self._create_share_type()
                      for i in (1, 2))

        # Set quotas for project, user and both share types
        self.update_quotas(self.tenant_id, shares=3, gigabytes=10)

        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           shares=2,
                           gigabytes=7)

        for st in (st_1['id'], st_2['name']):
            # no need for cleanup, since share types will be deleted at the
            # end of the test
            self.update_quotas(self.tenant_id,
                               share_type=st,
                               shares=2,
                               gigabytes=4,
                               cleanup=False)

        # Create share, 4Gb, st1 - ok
        share_1 = self.create_share(
            size=4, share_type_id=st_1['id'], client=self.client,
            cleanup_in_class=False)

        # Try create shares twice, failing on user and share type quotas
        for size, st_id in ((3, st_1['id']), (4, st_2['id'])):
            self.assertRaises(
                lib_exc.OverLimit,
                self.create_share,
                size=size, share_type_id=st_id, client=self.client,
                cleanup_in_class=False)

        # Create share, 3Gb, st2 - ok
        share_2 = self.create_share(
            size=3, share_type_id=st_2['id'], client=self.client,
            cleanup_in_class=False)

        # Check quota usages
        for g_l, g_use, s_l, s_use, kwargs in (
                (10, 7, 3, 2, {}),
                (7, 7, 2, 2, {'user_id': self.user_id}),
                (4, 4, 2, 1, {'share_type': st_1['id']}),
                (4, 3, 2, 1, {'share_type': st_2['name']})):
            quotas = self.client.detail_quotas(
                tenant_id=self.tenant_id, **kwargs)
            self.assertEqual(0, quotas['gigabytes']['reserved'])
            self.assertEqual(g_l, quotas['gigabytes']['limit'])
            self.assertEqual(g_use, quotas['gigabytes']['in_use'])
            self.assertEqual(0, quotas['shares']['reserved'])
            self.assertEqual(s_l, quotas['shares']['limit'])
            self.assertEqual(s_use, quotas['shares']['in_use'])

        # Delete shares and then check usages
        for share_id in (share_1['id'], share_2['id']):
            self.client.delete_share(share_id)
            self.client.wait_for_resource_deletion(share_id=share_id)
        for kwargs in ({}, {'share_type': st_1['name']},
                       {'user_id': self.user_id}, {'share_type': st_2['id']}):
            quotas = self.client.detail_quotas(
                tenant_id=self.tenant_id, **kwargs)
            for key in ('shares', 'gigabytes'):
                self.assertEqual(0, quotas[key]['reserved'])
                self.assertEqual(0, quotas[key]['in_use'])

    def _check_sg_usages(self, quotas, in_use, limit):
        """Helper method for 'test_share_group_quotas_usages' test."""
        self.assertEqual(0, int(quotas['share_groups']['reserved']))
        self.assertEqual(in_use, int(quotas['share_groups']['in_use']))
        self.assertEqual(limit, int(quotas['share_groups']['limit']))

    def _check_sgs_usages(self, quotas, in_use):
        """Helper method for 'test_share_group_quotas_usages' test."""
        self.assertEqual(0, int(quotas['share_group_snapshots']['reserved']))
        self.assertEqual(
            in_use, int(quotas['share_group_snapshots']['in_use']))
        self.assertEqual(1, int(quotas['share_group_snapshots']['limit']))

    def _check_usages(self, sg_in_use, sgs_in_use):
        """Helper method for 'test_share_group_quotas_usages' test."""
        p_quotas = self.client.detail_quotas(tenant_id=self.tenant_id)
        u_quotas = self.client.detail_quotas(
            tenant_id=self.tenant_id, user_id=self.user_id)
        self._check_sg_usages(p_quotas, sg_in_use, 3)
        self._check_sg_usages(u_quotas, sg_in_use, 2)
        self._check_sgs_usages(p_quotas, sgs_in_use)
        self._check_sgs_usages(u_quotas, sgs_in_use)

    @decorators.idempotent_id('fe357398-12d4-4a63-b5ae-0d5091ba3442')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipUnless(
        CONF.share.run_share_group_tests, 'Share Group tests disabled.')
    @base.skip_if_microversion_lt(SHARE_GROUPS_MICROVERSION)
    def test_share_group_quotas_usages(self):
        # Set quotas for project (3 SG, 1 SGS) and user (2 SG, 1 SGS)
        self.update_quotas(self.tenant_id,
                           share_groups=3,
                           share_group_snapshots=1)

        self.update_quotas(self.tenant_id,
                           user_id=self.user_id,
                           share_groups=2,
                           share_group_snapshots=1)

        # Check usages, they should be 0s
        self._check_usages(0, 0)

        # Create SG1 and check usages
        share_group1 = self.create_share_group(
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id],
            cleanup_in_class=False,
            client=self.client)
        self._check_usages(1, 0)

        # Create SGS1 and check usages
        sg_snapshot = self.create_share_group_snapshot_wait_for_active(
            share_group1['id'], cleanup_in_class=False, client=self.client)
        self._check_usages(1, 1)

        # Create SG2 from SGS1 and check usages
        share_group2 = self.create_share_group(
            share_group_type_id=self.share_group_type_id,
            cleanup_in_class=False,
            client=self.client,
            source_share_group_snapshot_id=sg_snapshot['id'])
        self._check_usages(2, 1)

        # Try create SGS2, fail, then check usages
        self.assertRaises(
            lib_exc.OverLimit,
            self.create_share_group,
            share_group_type_id=self.share_group_type_id,
            share_type_ids=[self.share_type_id],
            client=self.client, cleanup_in_class=False)
        self._check_usages(2, 1)

        # Delete SG2 and check usages
        self.client.delete_share_group(share_group2['id'])
        self.client.wait_for_resource_deletion(
            share_group_id=share_group2['id'])
        self._check_usages(1, 1)

        # Delete SGS1 and check usages
        self.client.delete_share_group_snapshot(sg_snapshot['id'])
        self.client.wait_for_resource_deletion(
            share_group_snapshot_id=sg_snapshot['id'])
        self._check_usages(1, 0)

        # Delete SG1 and check usages
        self.client.delete_share_group(share_group1['id'])
        self.client.wait_for_resource_deletion(
            share_group_id=share_group1['id'])
        self._check_usages(0, 0)
