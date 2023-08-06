# Copyright 2019 FUJITSU LIMITED
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

import json

from tempest.lib.common import rest_client


class EventApiClient(rest_client.RestClient):

    _uri = '/v1.0/events'

    def __init__(self, auth_provider, service, region):
        super(EventApiClient, self).__init__(
            auth_provider,
            service,
            region
        )

    def send_events(self, events, headers=None):
        msg = json.dumps(events)
        resp, body = self.post(self._uri, body=msg, headers=headers)
        return resp, body
