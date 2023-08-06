# (C) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
# (C) Copyright 2017-2018 SUSE LLC
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
import urllib.parse as urlparse
from urllib.parse import urlencode

from monasca_tempest_tests.tests.api import base
from monasca_tempest_tests.tests.api import constants
from monasca_tempest_tests.tests.api import helpers
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions

NUM_MEASUREMENTS = 100
MIN_REQUIRED_MEASUREMENTS = 2
WAIT_TIME = 30


class TestStatistics(base.BaseMonascaTest):

    @classmethod
    def resource_setup(cls):
        super(TestStatistics, cls).resource_setup()
        name = data_utils.rand_name('name')
        key = data_utils.rand_name('key')
        value1 = data_utils.rand_name('value1')
        value2 = data_utils.rand_name('value2')
        cls._test_name = name
        cls._test_key = key
        cls._test_value1 = value1
        cls._start_timestamp = int(time.time() * 1000)
        metrics = [
            helpers.create_metric(name=name,
                                  dimensions={key: value1},
                                  timestamp=cls._start_timestamp,
                                  value=1.23),
            helpers.create_metric(name=name,
                                  dimensions={key: value2},
                                  timestamp=cls._start_timestamp + 1000,
                                  value=4.56)
        ]
        cls.metric_values = [m['value'] for m in metrics]
        cls.monasca_client.create_metrics(metrics)
        start_time_iso = helpers.timestamp_to_iso(cls._start_timestamp)
        query_param = '?name=' + str(name) + '&start_time=' + \
                      start_time_iso + '&merge_metrics=true' + '&end_time=' + \
                      helpers.timestamp_to_iso(cls._start_timestamp + 1000 * 2)
        start_time_iso = helpers.timestamp_to_iso(cls._start_timestamp)
        cls._start_time_iso = start_time_iso

        num_measurements = 0
        for i in range(constants.MAX_RETRIES):
            resp, response_body = cls.monasca_client.\
                list_measurements(query_param)
            elements = response_body['elements']
            if len(elements) > 0:
                num_measurements = len(elements[0]['measurements'])
                if num_measurements >= MIN_REQUIRED_MEASUREMENTS:
                    break
            time.sleep(constants.RETRY_WAIT_SECS)

        if num_measurements < MIN_REQUIRED_MEASUREMENTS:
            assert False, "Required {} measurements, found {}".format(MIN_REQUIRED_MEASUREMENTS,
                                                                      num_measurements)

        cls._end_timestamp = cls._start_timestamp + 3000
        cls._end_time_iso = helpers.timestamp_to_iso(cls._end_timestamp)

        name2 = data_utils.rand_name("group-by")
        cls._group_by_metric_name = name2
        cls._group_by_end_time_iso = helpers.timestamp_to_iso(cls._start_timestamp + 4000)

        group_by_metrics = [
            helpers.create_metric(name=name2,
                                  dimensions={'key1': 'value1', 'key2': 'value5', 'key3': 'value7'},
                                  timestamp=cls._start_timestamp + 1, value=2),
            helpers.create_metric(name=name2,
                                  dimensions={'key1': 'value2', 'key2': 'value5', 'key3': 'value7'},
                                  timestamp=cls._start_timestamp + 1001, value=3),
            helpers.create_metric(name=name2,
                                  dimensions={'key1': 'value3', 'key2': 'value6', 'key3': 'value7'},
                                  timestamp=cls._start_timestamp + 2001, value=5),
            helpers.create_metric(name=name2,
                                  dimensions={'key1': 'value4', 'key2': 'value6', 'key3': 'value8'},
                                  timestamp=cls._start_timestamp + 3001, value=7),
        ]

        cls.monasca_client.create_metrics(group_by_metrics)
        query_param = '?name=' + str(name2) + \
                      '&start_time=' + start_time_iso + \
                      '&merge_metrics=true' + \
                      '&end_time=' + cls._group_by_end_time_iso

        num_measurements = 0
        for i in range(constants.MAX_RETRIES):
            resp, response_body = cls.monasca_client. \
                list_measurements(query_param)
            elements = response_body['elements']
            if len(elements) > 0:
                num_measurements = len(elements[0]['measurements'])
                if num_measurements >= len(group_by_metrics):
                    break
            time.sleep(constants.RETRY_WAIT_SECS)

        if num_measurements < len(group_by_metrics):
            assert False, "Required {} measurements, found {}".format(len(group_by_metrics),
                                                                      response_body)

    @classmethod
    def resource_cleanup(cls):
        super(TestStatistics, cls).resource_cleanup()

    @decorators.attr(type="gate")
    def test_list_statistics(self):
        self._test_list_statistic(with_end_time=True)

    @decorators.attr(type="gate")
    def test_list_statistics_with_no_end_time(self):
        self._test_list_statistic(with_end_time=False)

    def _test_list_statistic(self, with_end_time=True):
        query_parms = '?name=' + str(self._test_name) + \
                      '&statistics=' + urlparse.quote('avg,sum,min,max,count') + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&merge_metrics=true' + '&period=100000'
        if with_end_time is True:
            query_parms += '&end_time=' + str(self._end_time_iso)

        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        self.assertTrue(set(['links', 'elements']) == set(response_body))
        element = response_body['elements'][0]
        self._verify_element(element)
        column = element['columns']
        num_statistics_method = 5
        statistics = element['statistics'][0]
        self._verify_column_and_statistics(
            column, num_statistics_method, statistics, self.metric_values)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_no_name(self):
        query_parms = '?merge_metrics=true&statistics=avg&start_time=' + \
                      str(self._start_time_iso) + '&end_time=' + \
                      str(self._end_time_iso)
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_no_statistics(self):
        query_parms = '?name=' + str(self._test_name) + '&start_time=' + str(
            self._start_time_iso) + '&end_time=' + str(self._end_time_iso)
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_no_start_time(self):
        query_parms = '?name=' + str(self._test_name) + '&statistics=avg'
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_invalid_statistics(self):
        query_parms = '?name=' + str(self._test_name) + '&statistics=abc' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._end_time_iso)
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    def test_list_statistics_with_dimensions(self):
        query_parms = '?name=' + str(self._test_name) + '&statistics=avg' \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._end_time_iso) + \
                      '&dimensions=' + str(self._test_key) + ':' + \
                      str(self._test_value1) + '&period=100000'
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        dimensions = response_body['elements'][0]['dimensions']
        self.assertEqual(dimensions[self._test_key], self._test_value1)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_end_time_equals_start_time(self):
        query_parms = '?name=' + str(self._test_name) + \
                      '&merge_metrics=true&statistics=avg&' \
                      'start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._start_time_iso) + \
                      '&period=100000'
        self.assertRaises(exceptions.BadRequest,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    def test_list_statistics_with_period(self):
        query_parms = '?name=' + str(self._test_name) + \
                      '&merge_metrics=true&statistics=avg&' \
                      'start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._end_time_iso) + \
                      '&period=1'
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        time_diff = self._end_timestamp - self._start_timestamp
        len_statistics = len(response_body['elements'][0]['statistics'])
        self.assertEqual(time_diff / 1000, len_statistics)

    @decorators.attr(type="gate")
    def test_list_statistics_with_offset_limit(self):
        start_timestamp = int(time.time() * 1000)
        name = data_utils.rand_name()
        metric = [
            helpers.create_metric(name=name, timestamp=start_timestamp + 1,
                                  dimensions={'key1': 'value-1',
                                              'key2': 'value-1'},
                                  value=1),
            helpers.create_metric(name=name, timestamp=start_timestamp + 1001,
                                  dimensions={'key1': 'value-2',
                                              'key2': 'value-2'},
                                  value=2),
            helpers.create_metric(name=name, timestamp=start_timestamp + 2001,
                                  dimensions={'key1': 'value-3',
                                              'key2': 'value-3'},
                                  value=3),
            helpers.create_metric(name=name, timestamp=start_timestamp + 3001,
                                  dimensions={'key1': 'value-4',
                                              'key2': 'value-4'},
                                  value=4)
        ]

        num_metrics = len(metric)
        self.monasca_client.create_metrics(metric)
        query_parms = '?name=' + name
        for i in range(constants.MAX_RETRIES):
            resp, response_body = self.monasca_client.list_metrics(query_parms)
            self.assertEqual(200, resp.status)
            elements = response_body['elements']
            if elements and len(elements) == num_metrics:
                break
            else:
                time.sleep(constants.RETRY_WAIT_SECS)
        self._check_timeout(i, constants.MAX_RETRIES, elements, num_metrics)

        start_time = helpers.timestamp_to_iso(start_timestamp)
        end_timestamp = start_timestamp + 4001
        end_time = helpers.timestamp_to_iso(end_timestamp)
        query_parms = '?name=' + name + '&merge_metrics=true&statistics=avg' \
                      + '&start_time=' + str(start_time) + '&end_time=' + \
                      str(end_time) + '&period=1'
        resp, body = self.monasca_client.list_statistics(query_parms)
        self.assertEqual(200, resp.status)
        elements = body['elements'][0]['statistics']
        first_element = elements[0]

        query_parms = '?name=' + name + '&merge_metrics=true&statistics=avg'\
                      + '&start_time=' + str(start_time) + '&end_time=' + \
                      str(end_time) + '&period=1' + '&limit=' + str(num_metrics)
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        elements = response_body['elements'][0]['statistics']
        self.assertEqual(num_metrics, len(elements))
        self.assertEqual(first_element, elements[0])

        for limit in range(1, num_metrics):
            start_index = 0
            params = [('name', name),
                      ('merge_metrics', 'true'),
                      ('statistics', 'avg'),
                      ('start_time', str(start_time)),
                      ('end_time', str(end_time)),
                      ('period', 1),
                      ('limit', limit)]
            offset = None
            while True:
                num_expected_elements = limit
                if (num_expected_elements + start_index) > num_metrics:
                    num_expected_elements = num_metrics - start_index

                these_params = list(params)
                # If not the first call, use the offset returned by the last call
                if offset:
                    these_params.extend([('offset', str(offset))])
                query_parms = '?' + urlencode(these_params)
                resp, response_body = self.monasca_client.list_statistics(query_parms)
                self.assertEqual(200, resp.status)
                if not response_body['elements']:
                    self.fail("No metrics returned")
                if not response_body['elements'][0]['statistics']:
                    self.fail("No statistics returned")
                new_elements = response_body['elements'][0]['statistics']

                self.assertEqual(num_expected_elements, len(new_elements))
                expected_elements = elements[start_index:start_index + limit]
                self.assertEqual(expected_elements, new_elements)
                start_index += num_expected_elements
                if start_index >= num_metrics:
                    break
                # Get the next set
                offset = self._get_offset(response_body)

    @decorators.attr(type="gate")
    def test_list_statistics_with_group_by_one(self):
        query_parms = '?name=' + self._group_by_metric_name + \
                      '&group_by=key2' + \
                      '&statistics=max,avg,min' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._group_by_end_time_iso)
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        elements = response_body['elements']
        self.assertEqual(len(elements), 2)
        for statistics in elements:
            self.assertEqual(1, len(statistics['dimensions'].keys()))
            self.assertEqual([u'key2'], list(statistics['dimensions'].keys()))

    @decorators.attr(type="gate")
    def test_list_statistics_with_group_by_multiple(self):
        query_parms = '?name=' + self._group_by_metric_name + \
                      '&group_by=key2,key3' + \
                      '&statistics=max,avg,min' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._group_by_end_time_iso)
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        elements = response_body['elements']
        self.assertEqual(len(elements), 3)
        for statistics in elements:
            self.assertEqual(2, len(statistics['dimensions'].keys()))
            self.assertEqual({u'key2', u'key3'}, set(statistics['dimensions'].keys()))

    @decorators.attr(type="gate")
    def test_list_statistics_with_group_by_all(self):
        query_parms = '?name=' + self._group_by_metric_name + \
                      '&group_by=*' + \
                      '&statistics=max,avg,min' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._group_by_end_time_iso)
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        elements = response_body['elements']
        self.assertEqual(len(elements), 4)

    @decorators.attr(type="gate")
    def test_list_statistics_with_group_by_offset_limit(self):
        query_parms = '?name=' + str(self._group_by_metric_name) + \
                      '&group_by=key2' + \
                      '&statistics=avg,max' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._group_by_end_time_iso) + \
                      '&period=1'
        resp, response_body = self.monasca_client.list_statistics(query_parms)
        self.assertEqual(200, resp.status)
        all_expected_elements = response_body['elements']

        for limit in range(1, 4):
            offset = None
            for i in range(4 - limit):
                query_parms = '?name=' + str(self._group_by_metric_name) + \
                              '&group_by=key2' + \
                              '&statistics=avg,max' + \
                              '&start_time=' + str(self._start_time_iso) + \
                              '&end_time=' + str(self._group_by_end_time_iso) + \
                              '&period=1' + \
                              '&limit=' + str(limit)
                if i > 0:
                    offset = self._get_offset(response_body)
                    query_parms += "&offset=" + offset

                expected_elements = helpers.get_expected_elements_inner_offset_limit(
                    all_expected_elements,
                    offset,
                    limit,
                    'statistics')

                resp, response_body = self.monasca_client.list_statistics(query_parms)
                self.assertEqual(200, resp.status)
                self.assertEqual(expected_elements, response_body['elements'])

    @decorators.attr(type="gate")
    def test_list_statistics_with_long_start_time(self):
        query_parms = '?name=' + str(self._test_name) + \
                      '&statistics=' + urlparse.quote('avg,sum,min,max,count') + \
                      '&start_time=' + "2017-01-01T00:00:00.00Z" + \
                      '&end_time=' + str(self._end_time_iso) + \
                      '&merge_metrics=true' + '&period=100000'
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        self.assertTrue(set(['links', 'elements']) == set(response_body))
        element = response_body['elements'][0]
        self._verify_element(element)
        column = element['columns']
        num_statistics_method = 5
        statistics = element['statistics'][0]
        self._verify_column_and_statistics(
            column, num_statistics_method, statistics, self.metric_values)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_no_merge_metrics(self):
        key = data_utils.rand_name('key')
        value = data_utils.rand_name('value')
        metric3 = helpers.create_metric(
            name=self._test_name,
            dimensions={key: value},
            timestamp=self._start_timestamp + 2000)
        self.monasca_client.create_metrics(metric3)
        query_param = '?name=' + str(self._test_name) + '&start_time=' + \
                      self._start_time_iso + '&end_time=' + helpers.\
            timestamp_to_iso(self._start_timestamp + 1000 * 4) + \
                      '&merge_metrics=True'

        for i in range(constants.MAX_RETRIES):
            resp, response_body = self.monasca_client.\
                list_measurements(query_param)
            elements = response_body['elements']
            for element in elements:
                if str(element['name']) == self._test_name and len(
                        element['measurements']) == 3:
                    end_time_iso = helpers.timestamp_to_iso(
                        self._start_timestamp + 1000 * 4)
                    query_parms = '?name=' + str(self._test_name) + \
                                  '&statistics=avg' + '&start_time=' + \
                                  str(self._start_time_iso) + '&end_time=' +\
                                  str(end_time_iso) + '&period=100000'
                    self.assertRaises(exceptions.Conflict,
                                      self.monasca_client.list_statistics,
                                      query_parms)
                    return
            time.sleep(constants.RETRY_WAIT_SECS)
        self._check_timeout(i, constants.MAX_RETRIES, elements, 3)

    @decorators.attr(type="gate")
    @decorators.attr(type=['negative'])
    def test_list_statistics_with_name_exceeds_max_length(self):
        long_name = "x" * (constants.MAX_LIST_STATISTICS_NAME_LENGTH + 1)
        query_parms = '?name=' + str(long_name) + '&merge_metrics=true' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._end_time_iso)
        self.assertRaises(exceptions.UnprocessableEntity,
                          self.monasca_client.list_statistics, query_parms)

    @decorators.attr(type="gate")
    def test_list_statistics_response_body_statistic_result_type(self):
        query_parms = '?name=' + str(self._test_name) + '&period=100000' + \
                      '&statistics=avg' + '&merge_metrics=true' + \
                      '&start_time=' + str(self._start_time_iso) + \
                      '&end_time=' + str(self._end_time_iso)
        resp, response_body = self.monasca_client.list_statistics(
            query_parms)
        self.assertEqual(200, resp.status)
        element = response_body['elements'][0]
        statistic = element['statistics']
        statistic_result_type = type(statistic[0][1])
        self.assertEqual(statistic_result_type, float)

    def _verify_element(self, element):
        self.assertTrue(set(['id', 'name', 'dimensions', 'columns',
                             'statistics']) == set(element))
        self.assertTrue(type(element['id']) is str)
        self.assertTrue(element['id'] is not None)
        self.assertTrue(type(element['name']) is str)
        self.assertTrue(type(element['dimensions']) is dict)
        self.assertEqual(len(element['dimensions']), 0)
        self.assertTrue(type(element['columns']) is list)
        self.assertTrue(type(element['statistics']) is list)
        self.assertEqual(element['name'], self._test_name)

    def _verify_column_and_statistics(
            self, column, num_statistics_method, statistics, values):
        self.assertTrue(type(column) is list)
        self.assertTrue(type(statistics) is list)
        self.assertEqual(len(column), num_statistics_method + 1)
        self.assertEqual(column[0], 'timestamp')
        for i, method in enumerate(column):
            if method == 'avg':
                self.assertAlmostEqual(statistics[i], float(sum(values) / len(values)))
            elif method == 'max':
                self.assertEqual(statistics[i], max(values))
            elif method == 'min':
                self.assertEqual(statistics[i], min(values))
            elif method == 'sum':
                self.assertAlmostEqual(statistics[i], sum(values))
            elif method == 'count':
                self.assertEqual(statistics[i], len(values))

    def _check_timeout(self, timer, max_retries, elements,
                       expect_num_elements):
        if timer == max_retries - 1:
            error_msg = ("Failed: timeout on waiting for metrics: {} elements "
                         "are needed. Current number of elements = {}").\
                format(expect_num_elements, len(elements))
            raise self.fail(error_msg)
