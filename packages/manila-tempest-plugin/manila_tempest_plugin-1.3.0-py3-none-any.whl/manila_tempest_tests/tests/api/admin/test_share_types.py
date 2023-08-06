# Copyright 2014 OpenStack Foundation
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
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF

LATEST_MICROVERSION = CONF.share.max_api_microversion


@ddt.ddt
class ShareTypesAdminTest(base.BaseSharesAdminTest):

    @decorators.idempotent_id('34000fb9-b595-4a10-8306-7465f9ebc45d')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_share_type_create_delete(self):
        name = data_utils.rand_name("tempest-manila")
        extra_specs = self.add_extra_specs_to_dict()

        # Create share type
        st_create = self.shares_v2_client.create_share_type(
            name, extra_specs=extra_specs)
        self.assertEqual(name, st_create['share_type']['name'])
        st_id = st_create['share_type']['id']

        # Delete share type
        self.shares_v2_client.delete_share_type(st_id)

        # Verify deletion of share type
        self.shares_v2_client.wait_for_resource_deletion(st_id=st_id)
        self.assertRaises(lib_exc.NotFound,
                          self.shares_v2_client.get_share_type,
                          st_id)

    def _verify_is_public_key_name(self, share_type, version):
        old_key_name = 'os-share-type-access:is_public'
        new_key_name = 'share_type_access:is_public'
        if utils.is_microversion_gt(version, "2.6"):
            self.assertIn(new_key_name, share_type)
            self.assertNotIn(old_key_name, share_type)
        else:
            self.assertIn(old_key_name, share_type)
            self.assertNotIn(new_key_name, share_type)

    def _verify_description(self, expect_des, share_type, version):
        if utils.is_microversion_ge(version, "2.41"):
            self.assertEqual(expect_des, share_type['description'])
        else:
            self.assertNotIn('description', share_type)

    @decorators.idempotent_id('228d8bab-0b31-433e-956f-9db9877e6573')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @ddt.data('2.0', '2.6', '2.7', '2.40', '2.41')
    def test_share_type_create_get(self, version):
        self.skip_if_microversion_not_supported(version)

        name = data_utils.rand_name("tempest-manila")
        description = None
        if utils.is_microversion_ge(version, "2.41"):
            description = "Description for share type"
        extra_specs = self.add_extra_specs_to_dict({"key": "value", })

        # Create share type
        st_create = self.create_share_type(
            name, extra_specs=extra_specs, version=version,
            description=description)
        self.assertEqual(name, st_create['share_type']['name'])
        self._verify_description(
            description, st_create['share_type'], version)
        self._verify_is_public_key_name(st_create['share_type'], version)
        st_id = st_create["share_type"]["id"]

        # Get share type
        get = self.shares_v2_client.get_share_type(st_id, version=version)
        self.assertEqual(name, get["share_type"]["name"])
        self.assertEqual(st_id, get["share_type"]["id"])
        self._verify_description(description, get['share_type'], version)
        self.assertEqual(extra_specs, get["share_type"]["extra_specs"])
        self._verify_is_public_key_name(get['share_type'], version)

        # Check that backwards compatibility didn't break
        self.assertDictMatch(get["volume_type"], get["share_type"])

    @base.skip_if_microversion_lt("2.50")
    @decorators.idempotent_id('a9af19e1-e789-4c4f-a39b-dd8df6ed00b1')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @ddt.data(
        ('2.50', data_utils.rand_name("type_updated"),
         'description_updated', True),
        ('2.50', data_utils.rand_name("type_updated"), None, None),
        ('2.50', None, 'description_updated', None),
        ('2.50', None, None, True),
        ('2.50', None, None, False),
        (LATEST_MICROVERSION, data_utils.rand_name("type_updated"),
         'description_updated', True),
        (LATEST_MICROVERSION, data_utils.rand_name("type_updated"),
         None, None),
        (LATEST_MICROVERSION, None, 'description_updated', None),
        (LATEST_MICROVERSION, None, None, True),
        (LATEST_MICROVERSION, None, None, False),
    )
    @ddt.unpack
    def test_share_type_create_update(self, version, st_name,
                                      st_description, st_is_public):
        name = data_utils.rand_name("tempest-manila")
        description = "Description for share type"
        extra_specs = self.add_extra_specs_to_dict({"key": "value", })

        # Create share type
        st_create = self.create_share_type(
            name, extra_specs=extra_specs, version=version,
            description=description)
        self.assertEqual(name, st_create['share_type']['name'])
        self._verify_description(
            description, st_create['share_type'], version)
        self._verify_is_public_key_name(st_create['share_type'], version)
        st_id = st_create["share_type"]["id"]

        # Update share type
        updated_st = self.shares_v2_client.update_share_type(
            st_id, name=st_name, is_public=st_is_public,
            description=st_description, version=version)
        if st_name is not None:
            self.assertEqual(st_name, updated_st["share_type"]["name"])
        if st_description is not None:
            self._verify_description(st_description,
                                     updated_st['share_type'], version)
        if st_is_public is not None:
            self.assertEqual(
                st_is_public,
                updated_st["share_type"]["share_type_access:is_public"])

    @base.skip_if_microversion_lt("2.50")
    @decorators.idempotent_id('9019dc61-b2b1-472d-9b15-a3986439d4c3')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @ddt.data(
        ('2.50', None, '', None),
        (LATEST_MICROVERSION, None, '', None),
    )
    @ddt.unpack
    def test_share_type_unset_description(
            self, version, st_name, st_description, st_is_public):
        name = data_utils.rand_name("tempest-manila")
        description = "Description for share type"
        extra_specs = self.add_extra_specs_to_dict({"key": "value", })

        # Create share type
        st_create = self.create_share_type(
            name, extra_specs=extra_specs, version=version,
            description=description)
        self.assertEqual(name, st_create['share_type']['name'])
        self._verify_description(
            description, st_create['share_type'], version)
        self._verify_is_public_key_name(st_create['share_type'], version)
        st_id = st_create["share_type"]["id"]

        # Update share type
        updated_st = self.shares_v2_client.update_share_type(
            st_id, name=st_name, is_public=st_is_public,
            description=st_description, version=version)

        self._verify_description(None, updated_st['share_type'], version)

    @decorators.idempotent_id('5cc4c2e5-d2a4-4bfc-9208-3455ac551f20')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @ddt.data('2.0', '2.6', '2.7', '2.40', '2.41')
    def test_share_type_create_list(self, version):
        self.skip_if_microversion_not_supported(version)

        name = data_utils.rand_name("tempest-manila")
        description = None
        if utils.is_microversion_ge(version, "2.41"):
            description = "Description for share type"
        extra_specs = self.add_extra_specs_to_dict()

        # Create share type
        st_create = self.create_share_type(
            name, extra_specs=extra_specs, version=version,
            description=description)
        self._verify_is_public_key_name(st_create['share_type'], version)
        st_id = st_create["share_type"]["id"]

        # list share types
        st_list = self.shares_v2_client.list_share_types(version=version)
        sts = st_list["share_types"]
        self.assertGreaterEqual(len(sts), 1)
        self.assertTrue(any(st_id in st["id"] for st in sts))
        for st in sts:
            self._verify_is_public_key_name(st, version)

        # Check that backwards compatibility didn't break
        vts = st_list["volume_types"]
        self.assertEqual(len(sts), len(vts))
        for i in range(len(sts)):
            self.assertDictMatch(sts[i], vts[i])

    @decorators.idempotent_id('4e2ad320-9f3d-4797-a3ad-bf800bcd1831')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_get_share_with_share_type(self):

        # Data
        share_name = data_utils.rand_name("share")
        shr_type_name = data_utils.rand_name("share-type")
        extra_specs = self.add_extra_specs_to_dict({
            "storage_protocol": CONF.share.capability_storage_protocol,
        })

        # Create share type
        st_create = self.create_share_type(
            shr_type_name, extra_specs=extra_specs)

        # Create share with share type
        share = self.create_share(
            name=share_name, share_type_id=st_create["share_type"]["id"])
        self.assertEqual(share["name"], share_name)
        self.shares_client.wait_for_share_status(share["id"], "available")

        # Verify share info
        get = self.shares_v2_client.get_share(share["id"], version="2.5")
        self.assertEqual(share_name, get["name"])
        self.assertEqual(share["id"], get["id"])
        self.assertEqual(shr_type_name, get["share_type"])

        get = self.shares_v2_client.get_share(share["id"], version="2.6")
        self.assertEqual(st_create["share_type"]["id"], get["share_type"])
        self.assertEqual(shr_type_name, get["share_type_name"])

    @decorators.idempotent_id('d2261a27-d4a4-4237-9fad-f6fd8f27783a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_private_share_type_access(self):
        name = data_utils.rand_name("tempest-manila")
        extra_specs = self.add_extra_specs_to_dict({"key": "value", })
        project_id = self.shares_client.tenant_id

        # Create private share type
        st_create = self.create_share_type(
            name, False, extra_specs=extra_specs)
        self.assertEqual(name, st_create['share_type']['name'])
        st_id = st_create["share_type"]["id"]

        # It should not be listed without access
        st_list = self.shares_v2_client.list_share_types()
        sts = st_list["share_types"]
        self.assertFalse(any(st_id in st["id"] for st in sts))

        # List projects that have access for share type - none expected
        access = self.shares_v2_client.list_access_to_share_type(st_id)
        self.assertEmpty(access)

        # Add project access to share type
        access = self.shares_v2_client.add_access_to_share_type(
            st_id, project_id)

        # Now it should be listed
        st_list = self.shares_client.list_share_types()
        sts = st_list["share_types"]
        self.assertTrue(any(st_id in st["id"] for st in sts))

        # List projects that have access for share type - one expected
        access = self.shares_v2_client.list_access_to_share_type(st_id)
        expected = [{'share_type_id': st_id, 'project_id': project_id}, ]
        self.assertEqual(expected, access)

        # Remove project access from share type
        access = self.shares_v2_client.remove_access_from_share_type(
            st_id, project_id)

        # It should not be listed without access
        st_list = self.shares_client.list_share_types()
        sts = st_list["share_types"]
        self.assertFalse(any(st_id in st["id"] for st in sts))

        # List projects that have access for share type - none expected
        access = self.shares_v2_client.list_access_to_share_type(st_id)
        self.assertEmpty(access)

    @decorators.idempotent_id('90dca5c5-f28e-4f16-90ed-78f5d725664e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @ddt.data(*utils.deduplicate(('2.45', '2.46', LATEST_MICROVERSION)))
    def test_share_type_create_show_list_with_is_default_key(self, version):
        self.skip_if_microversion_not_supported(version)
        name = data_utils.rand_name("tempest-manila")
        extra_specs = self.add_extra_specs_to_dict()

        # Create share type
        st_create = self.create_share_type(
            name, extra_specs=extra_specs, version=version)['share_type']

        if utils.is_microversion_ge(version, '2.46'):
            self.assertIn('is_default', st_create)
            self.assertIs(False, st_create['is_default'])
        else:
            self.assertNotIn('is_default', st_create)

        # list share types
        st_list = self.shares_v2_client.list_share_types(version=version)
        for st_get in st_list['share_types']:
            if utils.is_microversion_ge(version, '2.46'):
                self.assertIn('is_default', st_get)
                if st_create['id'] == st_get['id']:
                    self.assertIs(False, st_get['is_default'])
                else:
                    self.assertTrue(st_get['is_default'] in (True, False))
            else:
                self.assertNotIn('is_default', st_get)

        # show share types
        st_id = st_create['id']
        st_show = self.shares_v2_client.get_share_type(
            st_id, version=version)['share_type']

        if utils.is_microversion_ge(version, '2.46'):
            self.assertIn('is_default', st_show)
            self.assertIs(False, st_show['is_default'])
        else:
            self.assertNotIn('is_default', st_show)
