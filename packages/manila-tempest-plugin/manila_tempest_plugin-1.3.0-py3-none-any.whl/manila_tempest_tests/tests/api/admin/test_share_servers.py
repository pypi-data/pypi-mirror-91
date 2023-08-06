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

import re

import ddt
import six
from tempest import config
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
import testtools
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

CONF = config.CONF


@ddt.ddt
class ShareServersAdminTest(base.BaseSharesAdminTest):

    @classmethod
    def skip_checks(cls):
        super(ShareServersAdminTest, cls).skip_checks()
        if not CONF.share.multitenancy_enabled:
            raise cls.skipException(
                'Share servers can be tested only with multitenant drivers.')

    @classmethod
    def resource_setup(cls):
        super(ShareServersAdminTest, cls).resource_setup()
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']
        # create share in this new share network
        cls.share = cls.create_share(
            share_type_id=cls.share_type_id)
        cls.share_network = cls.shares_v2_client.get_share_network(
            cls.shares_v2_client.share_network_id)

        if not cls.share_network["name"]:
            sn_id = cls.share_network["id"]
            cls.share_network = cls.shares_v2_client.update_share_network(
                sn_id, name="sn_%s" % sn_id)

        cls.sn_name_and_id = [
            cls.share_network["name"],
            cls.share_network["id"],
        ]
        cls.share_net_info = (
            utils.share_network_get_default_subnet(cls.share_network)
            if utils.share_network_subnets_are_supported()
            else cls.share_network)

        # Date should be like '2014-13-12T11:10:09.000000'
        cls.date_re = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2}[A-Z]{1}"
                                 "[0-9]{2}:[0-9]{2}:[0-9]{2}).*$")

    @decorators.idempotent_id('3f821248-2c05-4323-a95f-a0216a537b0a')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_without_filters(self):
        servers = self.shares_v2_client.list_share_servers()
        self.assertGreater(len(servers), 0)
        keys = [
            "id",
            "host",
            "status",
            "share_network_name",
            "updated_at",
            "project_id",
        ]

        for server in servers:
            # All expected keys are present
            for key in keys:
                self.assertIn(key, server.keys())
            # 'Updated at' is valid date if set
            if server["updated_at"]:
                self.assertTrue(self.date_re.match(server["updated_at"]))
            # Host is not empty
            self.assertGreater(len(server["host"]), 0)
            # Id is not empty
            self.assertGreater(len(server["id"]), 0)

        # Do not verify statuses because we get all share servers from whole
        # cluster and here can be servers with any state.
        # Server we used is present.
        any(s["share_network_name"] in self.sn_name_and_id for s in servers)

    @decorators.idempotent_id('515e3332-cce9-4a28-ad2e-96dbb2cc672e')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_with_host_filter(self):
        # Get list of share servers and remember 'host' name
        servers = self.shares_v2_client.list_share_servers()
        # Remember name of server that was used by this test suite
        # to be sure it will be still existing.
        for server in servers:
            if server["share_network_name"] in self.sn_name_and_id:
                if not server["host"]:
                    msg = ("Server '%s' has wrong value for host - "
                           "'%s'.") % (server["id"], server["host"])
                    raise lib_exc.InvalidContentType(message=msg)
                host = server["host"]
                break
        else:
            msg = ("Appropriate server was not found. Its share_network_data"
                   ": '%s'. List of servers: '%s'.") % (self.sn_name_and_id,
                                                        six.text_type(servers))
            raise lib_exc.NotFound(message=msg)
        search_opts = {"host": host}
        servers = self.shares_v2_client.list_share_servers(search_opts)
        self.assertGreater(len(servers), 0)
        for server in servers:
            self.assertEqual(server["host"], host)

    @decorators.idempotent_id('77a5c1c5-db2f-4ff6-872c-ed73a575acd0')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_with_status_filter(self):
        search_opts = {"status": "active"}
        servers = self.shares_v2_client.list_share_servers(search_opts)

        # At least 1 share server should exist always - the one created
        # for this class.
        self.assertGreater(len(servers), 0)
        for server in servers:
            self.assertEqual(server["status"], "active")

    @decorators.idempotent_id('ed671cbb-7732-4966-9f1e-b997b8aa05ff')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_with_project_id_filter(self):
        search_opts = {"project_id": self.share_network["project_id"]}
        servers = self.shares_v2_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertGreater(len(servers), 0)
        for server in servers:
            self.assertEqual(server["project_id"],
                             self.share_network["project_id"])

    @decorators.idempotent_id('70064129-df97-4dba-9482-2819558111ec')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_with_share_network_name_filter(self):
        search_opts = {"share_network": self.share_network["name"]}
        servers = self.shares_v2_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertGreater(len(servers), 0)
        for server in servers:
            self.assertEqual(server["share_network_name"],
                             self.share_network["name"])

    @decorators.idempotent_id('f64e8024-eb42-4a4c-be6b-97d35633a019')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_list_share_servers_with_share_network_id_filter(self):
        search_opts = {"share_network": self.share_network["id"]}
        servers = self.shares_v2_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertGreater(len(servers), 0)
        for server in servers:
            self.assertIn(server["share_network_name"],
                          self.sn_name_and_id)

    @decorators.idempotent_id('e1af24f4-bf63-467d-a857-3a402fa9b65b')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_show_share_server(self):
        share = self.shares_v2_client.get_share(self.share["id"])
        server = self.shares_v2_client.show_share_server(
            share["share_server_id"])
        keys = [
            "id",
            "host",
            "project_id",
            "status",
            "share_network_name",
            "created_at",
            "updated_at",
            "backend_details",
        ]
        if utils.is_microversion_ge(CONF.share.max_api_microversion, "2.49"):
            keys.append("is_auto_deletable")
            keys.append("identifier")
        if utils.is_microversion_ge(CONF.share.max_api_microversion, "2.51"):
            keys.append("share_network_subnet_id")
        # all expected keys are present
        for key in keys:
            self.assertIn(key, server.keys())

        # 'created_at' is valid date
        self.assertTrue(self.date_re.match(server["created_at"]))

        # 'updated_at' is valid date if set
        if server["updated_at"]:
            self.assertTrue(self.date_re.match(server["updated_at"]))

        # veriy that values for following keys are not empty
        for k in ('host', 'id', 'status'):
            self.assertGreater(len(server[k]), 0)

        # 'backend_details' should be a dict
        self.assertIsInstance(server["backend_details"], dict)

    @decorators.idempotent_id('782d8f5f-2c02-44dd-8d43-e06b651a71be')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    def test_show_share_server_details(self):
        share = self.shares_v2_client.get_share(self.share['id'])
        details = self.shares_v2_client.show_share_server_details(
            share['share_server_id'])

        # If details are present they and their values should be only strings
        for k, v in details.items():
            self.assertIsInstance(k, six.string_types)
            self.assertIsInstance(v, six.string_types)

    @decorators.idempotent_id('2fdf8d29-3ab8-4424-b684-6253f45b9666')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @ddt.data(True, False)
    @testtools.skipIf(CONF.share.share_network_id != "",
                      "This test is not suitable for pre-existing "
                      "share_network.")
    def test_delete_share_server(self, delete_share_network):
        # Get network and subnet from existing share_network and reuse it
        # to be able to delete share_server after test ends.
        # TODO(vponomaryov): attach security-services too. If any exist from
        #                    donor share-network.
        new_sn = self.create_share_network(
            add_security_services=True,
            neutron_net_id=self.share_net_info['neutron_net_id'],
            neutron_subnet_id=self.share_net_info['neutron_subnet_id'])

        # Create server with share
        self.create_share(share_type_id=self.share_type_id,
                          share_network_id=new_sn['id'])

        # List share servers, filtered by share_network_id
        servers = self.shares_v2_client.list_share_servers(
            {"share_network": new_sn["id"]})

        # There can be more than one share server for share network when retry
        # was used and share was created successfully not from first time.
        # So, iterate all share-servers, release all created resources. It will
        # allow share network to be deleted in cleanup.
        for serv in servers:
            # Verify that filtering worked as expected.
            self.assertEqual(new_sn["id"], serv["share_network_id"])

            # List shares by share server id
            shares = self.shares_v2_client.list_shares_with_detail(
                {"share_server_id": serv["id"]})
            for s in shares:
                self.assertEqual(new_sn["id"], s["share_network_id"])

            # Delete shares, so we will have share server without shares
            for s in shares:
                self.shares_v2_client.delete_share(s["id"])

            # Wait for shares deletion
            for s in shares:
                self.shares_v2_client.wait_for_resource_deletion(
                    share_id=s["id"])

            # List shares by share server id, we expect empty list
            empty = self.shares_v2_client.list_shares_with_detail(
                {"share_server_id": serv["id"]})
            self.assertEqual(0, len(empty))

            if delete_share_network:
                # Delete share network, it should trigger share server deletion
                self.shares_v2_client.delete_share_network(new_sn["id"])
            else:
                # Delete share server
                self.shares_v2_client.delete_share_server(serv["id"])

            # Wait for share server deletion
            self.shares_v2_client.wait_for_resource_deletion(
                server_id=serv["id"])

            if delete_share_network:
                self.shares_v2_client.wait_for_resource_deletion(
                    sn_id=new_sn["id"])

    @decorators.idempotent_id('960d49c5-f8d6-42be-aaf4-b7890a55df03')
    @testtools.skipIf(CONF.share.share_network_id != "",
                      "This test is not suitable for pre-existing "
                      "share_network.")
    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @utils.skip_if_microversion_not_supported("2.49")
    def test_share_server_reset_state(self):
        # Get network and subnet from existing share_network and reuse it
        # to be able to delete share_server after test ends.
        new_sn = self.create_share_network(
            add_security_services=True,
            neutron_net_id=self.share_net_info['neutron_net_id'],
            neutron_subnet_id=self.share_net_info['neutron_subnet_id'])
        share = self.create_share(
            share_type_id=self.share_type_id,
            share_network_id=new_sn['id']
        )
        share = self.shares_v2_client.get_share(share['id'])

        # obtain share server
        share_server = self.shares_v2_client.show_share_server(
            share['share_server_id']
        )

        for state in (constants.SERVER_STATE_ACTIVE,
                      constants.SERVER_STATE_CREATING,
                      constants.SERVER_STATE_DELETING,
                      constants.SERVER_STATE_ERROR,
                      constants.SERVER_STATE_MANAGE_ERROR,
                      constants.SERVER_STATE_MANAGE_STARTING,
                      constants.SERVER_STATE_UNMANAGE_ERROR,
                      constants.SERVER_STATE_UNMANAGE_STARTING):

            # leave it in a new state
            self.shares_v2_client.share_server_reset_state(
                share_server['id'],
                status=state,
            )
            self.shares_v2_client.wait_for_share_server_status(
                share_server['id'],
                status=state
            )

        # bring the share server back in the active state
        self.shares_v2_client.share_server_reset_state(
            share_server['id'],
            status=constants.SERVER_STATE_ACTIVE,
        )
        self.shares_v2_client.wait_for_share_server_status(
            share_server['id'],
            status=constants.SERVER_STATE_ACTIVE
        )

        # delete share
        self.shares_v2_client.delete_share(share["id"])
        self.shares_v2_client.wait_for_resource_deletion(
            share_id=share["id"]
        )

        # delete share network. This will trigger share server deletion
        self.shares_v2_client.delete_share_network(new_sn["id"])
        self.shares_v2_client.wait_for_resource_deletion(
            sn_id=new_sn['id'])
