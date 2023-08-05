import unittest
import requests
import uuid
import json
import traceback

from nose2.events import Plugin
from nose2.events import Event
from nose2.util import format_traceback
from nose2 import result
from nose2 import session


class Rt(Plugin):
    configSection = 'rt'
    commandLineSwitch = (None, 'rt', 'Enable data collector for Testgr')

    def __init__(self):

        self.endpoint = self.config.as_str(
            'endpoint', '')
        self.screenshots_var = self.config.as_str('screenshots_var', '')
        self.show_errors = self.config.as_bool(
            'show_errors', '')
        self.session_obj = session.Session()
        self.test_prefix = self.session_obj.testMethodPrefix
        self.uuid = str(uuid.uuid4())
        self.success = 0
        self.errors = 0
        self.failed = 0
        self.skipped = 0
        self.timeTaken = 0
        self.start = None
        self.stop = None
        self.test_outcome = None
        self.attrs = []
        self.tests = None
        self.addArgument(self.attrs, None, "rte", "With --rte \"your_environment\" option you can send "
                                                  "environment name or info to Testgr server")                                      
        group = self.session.pluginargs
        group.add_argument('--rt-job-report', action='store_true', dest='rt_job_report',
                           help='Send Testgr job result via email')
        group.add_argument('--rt-custom-data', dest='rt_custom_data',
                           help='With --rt-custom-data {\"key\": \"value\"} option you can send additional data to Testgr server')

    def handleArgs(self, event):
        self.send_report_arg = event.args.rt_job_report
        self.rt_custom_data = event.args.rt_custom_data

    def send_report(self):
        if self.send_report_arg is True:
            return "1"
        return "0"

    def post(self, payload):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            requests.post(self.endpoint, data=json.dumps(payload), headers=headers)
        except requests.exceptions.ConnectionError as error:
            if self.show_errors:
                print(error)
            else:
                pass

    def startTestRun(self, event):
        self.tests = self.getTests(event)
        if len(self.attrs) > 0:
            env = self.attrs[0]
        else:
            env = None
        if self.rt_custom_data:
            custom_data = self.rt_custom_data
        else:
            custom_data = None
        self.post({
            'fw': "1",
            'type': "startTestRun",
            'job_id': self.uuid,
            'tests': self.tests[0],
            'test_uuids': self.tests[1],
            'test_descriptions': self.tests[2],
            'env': env,
            'custom_data': custom_data,
            'startTime': str(event.startTime)
        })

    def startTest(self, event):
        self.test_outcome = None
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        self.post({
            'fw': "1",
            'type': 'startTestItem',
            'job_id': self.uuid,
            'test': test_id,
            'uuid': self.tests[1][test_id],
            'startTime': str(event.startTime)})

    def testOutcome(self, event):
        msg = ''
        trace = ''
        if event.exc_info:
            msg = event.exc_info
            trace = event.exc_info[2]
            # for -N arg
            if not isinstance(trace, str):
                trace = traceback.format_tb(tb=trace)
                trace = "\n".join(trace).replace("  ", "\t")
            else:
                if trace in msg:
                    msg = list(msg)
                    msg[2] = ""
                    msg = tuple(msg)  
        elif event.reason:
            msg = event.reason
        error_text = ''
        status = ''
        if event.outcome == result.ERROR:
            error_text = msg
            status = 'error'
        elif event.outcome == result.FAIL and not event.expected:
            error_text = msg
            status = 'failed'
        elif event.outcome == result.PASS and not event.expected:
            status = 'skipped'
        elif event.outcome == result.SKIP:
            status = 'skipped'
        elif event.outcome == result.FAIL and event.expected:
            error_text = msg
            status = 'skipped'
        elif event.outcome == result.PASS and event.expected:
            error_text = msg
            status = 'passed'
        self.test_outcome = status, error_text, trace

    def stopTest(self, event):
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        screens_for_upload = ""
        try:
            screens = getattr(test, self.screenshots_var)
            if screens and len(screens):
                screens_for_upload = screens
        except:
            pass
        self.post({
            'fw': "1",
            'type': 'stopTestItem',
            'job_id': self.uuid,
            'test': test_id,
            'screens': screens_for_upload,
            'uuid': self.tests[1][test_id],
            'stopTime': str(event.stopTime),
            'status': str(self.test_outcome[0]),
            'msg': str(self.test_outcome[1]),
            'trace': str(self.test_outcome[2])
        })

    def stopTestRun(self, event):
        self.timeTaken = "%.3f" % event.timeTaken
        self.post({
            'fw': "1",
            'type': 'stopTestRun',
            'job_id': self.uuid,
            'stopTime': str(event.stopTime),
            'timeTaken': self.timeTaken,
            'send_report': self.send_report()})

    def getTests(self, event):
        suite = event.suite
        tests = []
        test_uuids = {}
        test_descriptions = {}
        for suite_data in suite:
            for test_data in suite_data:
                try:
                    for test_list in test_data:
                        # Single
                        if isinstance(test_list, unittest.suite.TestSuite):
                            for test in test_list._tests:
                                test_uuid = str(uuid.uuid4())
                                test_data = (str(test).split(" "))
                                tests.append(({str(test_data[0]): test.id()}))
                                test_uuids[test.id()] = test_uuid
                                test_descriptions[test_uuid] = test.shortDescription()
                        # Multiple
                        else:
                            test_uuid = str(uuid.uuid4())
                            test_data = (str(test_list).split(" "))
                            tests.append(({str(test_data[0]): test_list.id()}))
                            test_uuids[test_list.id()] = test_uuid
                            test_descriptions[test_uuid] = test_list.shortDescription()
                except:
                    print("FAIL: " + str(test_data))
        return tests, test_uuids, test_descriptions

