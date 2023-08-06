# Copyright 2015 Mirantis Inc.
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

from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils


class AvailabilityZonesNegativeTest(base.BaseSharesTest):

    @classmethod
    def skip_checks(cls):
        super(AvailabilityZonesNegativeTest, cls).skip_checks()
        utils.check_skip_if_microversion_not_supported('2.7')

    @decorators.idempotent_id('050fa9fb-4cc8-4064-9e91-bb169fca03db')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_list_availability_zones_api_not_found_with_legacy_url(self):
        # NOTE(vponomaryov): remove this test with removal of availability zone
        # extension url support.
        self.assertRaises(
            lib_exc.NotFound,
            self.shares_v2_client.list_availability_zones,
            url='os-availability-zone',
            version='2.7',
        )

    @decorators.idempotent_id('133ffc40-bff1-491a-a230-189cddd66e29')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_list_availability_zones_api_not_found(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.shares_v2_client.list_availability_zones,
            url='availability-zones',
            version='2.6',
        )
