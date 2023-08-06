# (C) Copyright 2016-2018 Hewlett Packard Enterprise Development LP
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

import time
import urllib.parse as parse

from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions

from monasca_tempest_tests.tests.api import base
from monasca_tempest_tests.tests.api import constants
from monasca_tempest_tests.tests.api import helpers


GROUP_BY_ALLOWED_PARAMS = {'alarm_definition_id', 'name', 'state', 'severity',
                           'link', 'lifecycle_state', 'metric_name',
                           'dimension_name', 'dimension_value'}


class TestAlarmsCount(base.BaseMonascaTest):

    @classmethod
    def resource_setup(cls):
        super(TestAlarmsCount, cls).resource_setup()

        num_hosts = 20

        alarm_definitions = []
        expected_alarm_counts = []
        metrics_to_send = []

        # OK, LOW
        expression = "max(test_metric_01) > 10"
        name = data_utils.rand_name('test-counts-01')
        alarm_definitions.append(helpers.create_alarm_definition(
            name=name,
            expression=expression,
            severity='LOW',
            match_by=['hostname', 'unique']))
        for i in range(100):
            metrics_to_send.append(helpers.create_metric(
                name='test_metric_01',
                dimensions={'hostname': 'test_' + str(i % num_hosts),
                            'unique': str(i)},
                value=1
            ))
        expected_alarm_counts.append(100)

        # ALARM, MEDIUM
        expression = "max(test_metric_02) > 10"
        name = data_utils.rand_name('test-counts-02')
        alarm_definitions.append(helpers.create_alarm_definition(
            name=name,
            expression=expression,
            severity='MEDIUM',
            match_by=['hostname', 'unique']))
        for i in range(75):
            metrics_to_send.append(helpers.create_metric(
                name='test_metric_02',
                dimensions={'hostname': 'test_' + str(i % num_hosts),
                            'unique': str(i)},
                value=11
            ))
            # append again to move from undetermined to alarm
            metrics_to_send.append(helpers.create_metric(
                name='test_metric_02',
                dimensions={'hostname': 'test_' + str(i % num_hosts),
                            'unique': str(i)},
                value=11
            ))
        expected_alarm_counts.append(75)

        # OK, HIGH, shared dimension
        expression = "max(test_metric_03) > 100"
        name = data_utils.rand_name('test_counts-03')
        alarm_definitions.append(helpers.create_alarm_definition(
            name=name,
            expression=expression,
            severity='HIGH',
            match_by=['hostname', 'unique']))
        for i in range(50):
            metrics_to_send.append(helpers.create_metric(
                name='test_metric_03',
                dimensions={'hostname': 'test_' + str(i % num_hosts),
                            'unique': str(i),
                            'height': '55'},
                value=i
            ))
        expected_alarm_counts.append(50)

        # UNDERTERMINED, CRITICAL
        expression = "max(test_metric_undet) > 100"
        name = data_utils.rand_name('test-counts-04')
        alarm_definitions.append(helpers.create_alarm_definition(
            name=name,
            expression=expression,
            severity='CRITICAL',
            match_by=['hostname', 'unique']))
        for i in range(25):
            metrics_to_send.append(helpers.create_metric(
                name='test_metric_undet',
                dimensions={'hostname': 'test_' + str(i % num_hosts),
                            'unique': str(i)},
                value=1
            ))
        expected_alarm_counts.append(25)

        # create alarm definitions
        cls.alarm_definition_ids = []
        for definition in alarm_definitions:
            resp, response_body = cls.monasca_client.create_alarm_definitions(
                definition)
            if resp.status == 201:
                cls.alarm_definition_ids.append(response_body['id'])
            else:
                msg = "Failed to create alarm_definition during setup: {} {}".format(resp.status,
                                                                                     response_body)
                assert False, msg

        # Give Thresh time to process the new Alarm Definitions
        time.sleep(constants.ALARM_DEFINITION_CREATION_WAIT)

        # create alarms
        for metric in metrics_to_send:
            metric['timestamp'] = int(time.time() * 1000)
            cls.monasca_client.create_metrics(metric)
            # ensure metric timestamps are unique
            time.sleep(0.01)

        # check that alarms exist
        time_out = time.time() + 70
        while time.time() < time_out:
            setup_complete = True
            alarm_count = 0
            for i in range(len(cls.alarm_definition_ids)):
                resp, response_body = cls.monasca_client.list_alarms(
                    '?alarm_definition_id=' + cls.alarm_definition_ids[i])
                if resp.status != 200:
                    msg = "Error listing alarms: {} {}".format(resp.status, response_body)
                    assert False, msg
                if len(response_body['elements']) < expected_alarm_counts[i]:
                    setup_complete = False
                    alarm_count += len(response_body['elements'])
                    break

            if setup_complete:
                # allow alarm transitions to occur
                # time.sleep(15)
                return

        msg = "Failed to create all specified alarms" \
              " during setup, alarm_count was {}".format(alarm_count)
        assert False, msg

    @classmethod
    def resource_cleanup(cls):
        super(TestAlarmsCount, cls).resource_cleanup()

    def _verify_counts_format(self, response_body, group_by=None, expected_length=None):
        expected_keys = ['links', 'counts', 'columns']
        for key in expected_keys:
            self.assertIn(key, response_body)
            self.assertIsInstance(response_body[key], list)

        expected_columns = ['count']
        if isinstance(group_by, list):
            expected_columns.extend(group_by)
        self.assertEqual(expected_columns, response_body['columns'])

        if expected_length is not None:
            self.assertEqual(expected_length, len(response_body['counts']))
        else:
            expected_length = len(response_body['counts'])

        for i in range(expected_length):
            self.assertEqual(len(expected_columns), len(response_body['counts'][i]))

    # test with no params
    @decorators.attr(type='gate')
    def test_count(self):
        resp, response_body = self.monasca_client.count_alarms()
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body)
        self.assertEqual(250, response_body['counts'][0][0])

    # test with each group_by parameter singularly
    @decorators.attr(type='gate')
    def test_group_by_singular(self):
        resp, response_body = self.monasca_client.list_alarms("?state=ALARM")
        self.assertEqual(200, resp.status)
        alarm_state_count = len(response_body['elements'])
        resp, response_body = self.monasca_client.list_alarms("?state=undetermined")
        self.assertEqual(200, resp.status)
        undet_state_count = len(response_body['elements'])

        resp, response_body = self.monasca_client.count_alarms("?group_by=state")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body, group_by=['state'])

        self.assertEqual('ALARM', response_body['counts'][0][1])
        self.assertEqual(alarm_state_count, response_body['counts'][0][0])
        self.assertEqual('UNDETERMINED', response_body['counts'][-1][1])
        self.assertEqual(undet_state_count, response_body['counts'][-1][0])

        resp, response_body = self.monasca_client.count_alarms("?group_by=name")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body, group_by=['name'], expected_length=4)

    # test with group by a parameter that is not allowed
    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_group_by_not_allowed(self):
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.count_alarms, "?group_by=not_allowed")

    # test with a few group_by fields
    @decorators.attr(type='gate')
    def test_group_by_multiple(self):
        resp, response_body = self.monasca_client.list_alarms()
        alarm_low_count = 0
        for alarm in response_body['elements']:
            if alarm['state'] == 'ALARM' and alarm.get('severity', '') == 'LOW':
                alarm_low_count += 1

        # Using urlencode mimics the CLI behavior. Without the urlencode, falcon
        # treats group_by as a list, with the urlencode it treats group_by as
        # a string. The API needs to handle both.
        # test_with_all_group_by_params tests multiple group_by without
        # urlencode
        query_params = parse.urlencode([('group_by', 'state,severity')])
        resp, response_body = self.monasca_client.count_alarms("?" + query_params)
        self._verify_counts_format(response_body, group_by=['state', 'severity'])

    def run_count_test(self, query_string):
        resp, response_body = self.monasca_client.list_alarms(query_string)
        self.assertEqual(200, resp.status)
        expected_count = len(response_body['elements'])
        # Make sure something was found
        self.assertTrue(expected_count > 0)

        resp, response_body = self.monasca_client.count_alarms(query_string)
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body, expected_length=1)
        self.assertEqual(expected_count, response_body['counts'][0][0])

    # test filter by severity
    @decorators.attr(type='gate')
    def test_filter_severity(self):
        self.run_count_test("?severity=LOW")

    # test filter by state
    @decorators.attr(type='gate')
    def test_filter_state(self):
        self.run_count_test("?state=ALARM")

    # test filter by metric name
    @decorators.attr(type='gate')
    def test_filter_metric_name(self):
        self.run_count_test("?metric_name=test_metric_01")

    # test with multiple metric dimensions
    @decorators.attr(type='gate')
    def test_filter_multiple_dimensions(self):
        self.run_count_test("?metric_dimensions=hostname:test_1,unique:1")

    # test with multiple metric dimensions values
    @decorators.attr(type='gate')
    def test_filter_multiple_dimensions_values_1(self):
        self.run_count_test("?metric_dimensions=hostname:test_1|test_2,unique:1")

    # test with multiple metric dimensions values (order should not matter)
    @decorators.attr(type='gate')
    def test_filter_multiple_dimensions_values_2(self):
        self.run_count_test("?metric_dimensions=hostname:test_2|test_1,unique:1")

    # test with filter and group_by parameters
    @decorators.attr(type='gate')
    def test_filter_and_group_by_params(self):
        resp, response_body = self.monasca_client.list_alarms("?state=ALARM")
        self.assertEqual(200, resp.status)
        expected_count = 0
        for element in response_body['elements']:
            if element['alarm_definition']['severity'] == 'MEDIUM':
                expected_count += 1

        resp, response_body = self.monasca_client.count_alarms("?state=ALARM&group_by=severity")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body, group_by=['severity'])
        self.assertEqual(expected_count, response_body['counts'][0][0])

    @decorators.attr(type='gate')
    def test_with_all_group_by_params(self):
        resp, response_body = self.monasca_client.list_alarms()
        self.assertEqual(200, resp.status)
        expected_num_count = len(response_body['elements'])

        query_params = "?group_by=" + ','.join(GROUP_BY_ALLOWED_PARAMS)
        resp, response_body = self.monasca_client.count_alarms(query_params)
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body, group_by=list(GROUP_BY_ALLOWED_PARAMS))

        # Expect duplicates
        msg = "Not enough distinct counts. Expected at " \
              "least {}, found {}".format(expected_num_count, len(response_body['counts']))
        assert expected_num_count <= len(response_body['counts']), msg

    @decorators.attr(type='gate')
    def test_limit(self):
        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'])
        assert len(response_body['counts']) > 1, "Too few counts to test limit, found 1"

        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value&limit=1")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'],
                                   expected_length=1)

    @decorators.attr(type='gate')
    def test_offset(self):
        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'])
        expected_counts = len(response_body['counts']) - 1

        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value&offset=1")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'],
                                   expected_length=expected_counts)

    @decorators.attr(type='gate')
    @decorators.attr(type=['negative'])
    def test_invalid_offset(self):
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.count_alarms,
                          "?group_by=metric_name&offset=not_an_int")

    @decorators.attr(type='gate')
    def test_limit_and_offset(self):
        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'])
        expected_first_result = response_body['counts'][1]

        resp, response_body = self.monasca_client.count_alarms(
            "?group_by=metric_name,dimension_name,dimension_value&offset=1&limit=5")
        self.assertEqual(200, resp.status)
        self._verify_counts_format(response_body,
                                   group_by=['metric_name', 'dimension_name', 'dimension_value'],
                                   expected_length=5)
        self.assertEqual(expected_first_result, response_body['counts'][0])
