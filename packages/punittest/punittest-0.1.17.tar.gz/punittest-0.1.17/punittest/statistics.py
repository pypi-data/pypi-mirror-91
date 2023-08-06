#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from copy import deepcopy
from importlib import import_module
from .settings import Settings
from .testcase import CASE_SKIP_FLAG, CASE_TAG_FLAG
from .testset import CodeTestSet

KEYWORDS = ["testrunner", "testset", "testresult", "testcase", "testsuite"]


class Statistics:
    """由测试类继承，负责统计测试类中的数据"""
    def __init__(self):
        self.run_file = __file__
        self.suite_path = Settings.TEST_SUITE_PATH.lower()
        self.test_prefix = Settings.TEST_PREFIX.lower()
        self.skip_prefix = Settings.SKIP_PREFIX.lower()

    def _file_info(self, file_path):
        """根据file_path获取file_info"""
        dir_, name = os.path.split(file_path)[0], os.path.split(file_path)[1]
        if not name.startswith("_") and os.path.splitext(name)[-1] == ".py":
            file_info = {"file_name": name, "file_path": file_path}
            import_list = CodeTestSet.get_import_list_by_path(file_path)
            file_info["file_import_list"] = import_list
            if import_list is not None:
                _import_list = import_list.split('.')
                for sub_path in _import_list:
                    if sub_path.lower().startswith(self.skip_prefix):
                        file_info["file_skip"] = True
                        break
                else:
                    file_info["file_skip"] = False
            return file_info

    def _test_file(self):
        result = []
        if os.path.isdir(self.suite_path):
            for root, _, files in os.walk(self.suite_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_info = self._file_info(file_path)
                    if file_info is not None:
                        result.append(file_info)
        else:
            file_info = self._file_info(self.suite_path)
            if file_info is not None:
                result.append(file_info)
        return result

    def _test_class(self, file_info):
        result = []
        module = import_module(file_info['file_import_list'])
        for cls_name in module.__dict__:
            if cls_name.lower().startswith(self.test_prefix) and cls_name.lower() not in KEYWORDS:
                cls_ = getattr(module, cls_name)
                file_info['class_name'] = cls_name
                file_info['class_skip'] = getattr(cls_, CASE_SKIP_FLAG, False)
                class_info = deepcopy(file_info)
                result.append(class_info)
        return result

    def _test_case(self, class_info):
        result = []
        module = import_module(class_info['file_import_list'])
        cls_ = getattr(module, class_info['class_name'])
        for func_name in cls_.__dict__:
            if func_name.lower().startswith(self.test_prefix):
                func = getattr(cls_, func_name)
                class_info['case_name'] = func_name
                class_info['case_skip'] = getattr(func, CASE_SKIP_FLAG, False)
                class_info['case_tag'] = getattr(func, CASE_TAG_FLAG, {'all'})
                case_info = deepcopy(class_info)
                result.append(case_info)
        return result

    @staticmethod
    def test_files():
        state = Statistics()
        files = state._test_file()
        for i, file_info in enumerate(files):
            file_skip = file_info.pop('file_skip')
            new_file = {'num': i + 1}
            new_file.update(file_info)
            new_file['if_skip'] = file_skip
            files[i] = new_file
        return files

    @staticmethod
    def test_classes():
        classes = []
        i = 1
        state = Statistics()
        for file_info in state._test_file():
            for class_info in state._test_class(file_info):
                file_skip = class_info.pop('file_skip')
                class_skip = class_info.pop('class_skip')
                new_class = {'num': i}
                new_class.update(class_info)
                new_class['if_skip'] = file_skip or class_skip
                classes.append(new_class)
                i += 1
        return classes

    @staticmethod
    def test_cases():
        cases = []
        i = 1
        state = Statistics()
        for file_info in state._test_file():
            for class_info in state._test_class(file_info):
                for case_info in state._test_case(class_info):
                    file_skip = case_info.pop('file_skip')
                    class_skip = case_info.pop('class_skip')
                    case_skip = case_info.pop('case_skip')
                    new_case = {'num': i}
                    new_case.update(case_info)
                    new_case['if_skip'] = file_skip or class_skip or case_skip
                    cases.append(new_case)
                    i += 1
        return cases
