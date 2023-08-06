# (C) Copyright 2016-2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from monasca_tempest_tests.tests.api import base
from tempest.lib import decorators


class TestNotificationMethodType(base.BaseMonascaTest):

    @classmethod
    def resource_setup(cls):
        super(TestNotificationMethodType, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        super(TestNotificationMethodType, cls).resource_cleanup()

    @decorators.attr(type="gate")
    def test_list_notification_method_type(self):
        resp, response_body = (self.monasca_client.
                               list_notification_method_types())
        self.assertEqual(200, resp.status)
