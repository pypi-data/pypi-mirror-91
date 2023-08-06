#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import datetime
import shutil

from .settings import Settings
from .testset import ApiTestSet, CodeTestSet, ExcelTestSet
from .testcase import TestCaseHandler
from .testresult import TestResult
from .utils.logger import logger


result_data = dict()
result_data['testResult'] = []
STATUS = {
    0: 'Pass',
    1: 'Fail',
    2: 'Error',
    3: 'Skip',
}


class TestRunner:
    def __init__(self, report_title, verbosity=1, description=""):
        self.verbosity = verbosity
        self.title = report_title
        self.description = description
        self.start_time = datetime.datetime.now()
        self.stop_time = None

    def _run(self, test):
        msg = "开始测试，测试标签[{}]，用例数量总共{}个，跳过{}个，实际运行{}个"
        logger.info(msg.format(
            ', '.join(Settings.RUN_TAGS),
            TestCaseHandler.total_case_num,
            TestCaseHandler.total_case_num - TestCaseHandler.actual_case_num,
            TestCaseHandler.actual_case_num
        ))
        logger.info("")
        result = TestResult(self.verbosity)
        test(result)
        self.stop_time = datetime.datetime.now()
        self.analyze_test_result(result)
        logger.info('')
        logger.info('执行完毕: 成功{}，跳过{}，失败{}，报错{}'.format(
            result_data['testPass'], result_data['testSkip'],
            result_data['testFail'], result_data['testError']
        ))
        logger.info('测试时间: {}'.format(self.stop_time - self.start_time))
        logger.info('')
        logger.info('失败用例:')
        for tr in result_data['testResult']:
            if tr['status'] == '失败':
                logger.info('{} - {} - {}'.format(tr['moduleName'], tr['className'], tr['methodName']))
        logger.info('')
        logger.info('报错用例:')
        for tr in result_data['testResult']:
            if tr['status'] == '报错':
                logger.info('{} - {} - {}'.format(tr['moduleName'], tr['className'], tr['methodName']))
        if Settings.LOG_REPORT_SWITCH:
            report_dir = Settings.REPORT_DIR
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)
            root = os.path.abspath(os.path.dirname(__file__))
            static_src_path = os.path.join(root, "static")
            static_tar_path = os.path.join(report_dir, "static")
            if not os.path.exists(static_tar_path):
                shutil.copytree(static_src_path, static_tar_path)
            from .report_template import style_2
            file_path = os.path.join(report_dir, r"{}.html".format(self.start_time.strftime("%Y-%m-%d_%H-%M-%S")))
            style_2.build_report(file_path, result_data)

    @staticmethod
    def sort_result(case_results):
        rmap = {}
        classes = []
        for n, t, o, e, run_time, start_time, end_time in case_results:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e, run_time, start_time, end_time))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def analyze_test_result(self, result):
        result_data["reportName"] = self.title
        result_data["beginTime"] = str(self.start_time)
        result_data["finishTime"] = str(self.stop_time)
        result_data["totalTime"] = str(self.stop_time - self.start_time)[0: -5] + "s"

        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            pass_num = fail_num = error_num = skip_num = 0
            for case_state, *_ in cls_results:
                if case_state == 0:
                    pass_num += 1
                elif case_state == 1:
                    fail_num += 1
                elif case_state == 2:
                    error_num += 1
                else:
                    skip_num += 1

            for tid, (state_id, t, o, e, run_time, start_time, end_time) in enumerate(cls_results):
                name = t.id().split('.')[-1]
                doc = t.shortDescription() or ""
                case_data = dict()
                case_data['moduleName'] = cls.__module__
                case_data['className'] = cls.__name__
                case_data['methodName'] = name
                case_data['spendTime'] = str(run_time)[0: -5] + "s"
                case_data['startTime'] = str(start_time)
                case_data['endTime'] = str(end_time)
                case_data['description'] = doc
                case_data['log'] = o + e
                if STATUS[state_id] == "Pass":
                    case_data['status'] = "成功"
                if STATUS[state_id] == "Fail":
                    case_data['status'] = "失败"
                if STATUS[state_id] == "Error":
                    case_data['status'] = "报错"
                if STATUS[state_id] == "Skip":
                    case_data['status'] = "跳过"
                result_data['testResult'].append(case_data)

        result_data["testPass"] = result.success_count
        result_data["testAll"] = result.success_count + result.failure_count + result.error_count + result.skip_count
        result_data["testFail"] = result.failure_count
        result_data["testSkip"] = result.skip_count
        result_data["testError"] = result.error_count

    def run(self, api_data=None):
        if Settings.TEST_SET_FORM == "CODE":
            test_set = CodeTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX)
        elif Settings.TEST_SET_FORM == "EXCEL":
            test_set = ExcelTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX)
        elif Settings.TEST_SET_FORM == "API":
            test_set = ApiTestSet(api_data, Settings.TEST_PREFIX, Settings.SKIP_PREFIX)
        else:
            test_set = CodeTestSet(Settings.TEST_PREFIX, Settings.SKIP_PREFIX)
        suite = test_set.convert_test_suite()
        self._run(suite)
        return result_data
