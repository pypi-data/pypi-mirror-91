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


class SchedulerStatsNegativeTest(base.BaseSharesTest):

    @decorators.idempotent_id('33db76eb-7501-43f9-8c4f-8e6e35519a4d')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_list_pools_with_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.shares_client.list_pools)

    @decorators.idempotent_id('f89136cf-34a1-475b-8514-3114f9f159a5')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_list_pools_detailed_with_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.shares_client.list_pools,
                          detail=True)
