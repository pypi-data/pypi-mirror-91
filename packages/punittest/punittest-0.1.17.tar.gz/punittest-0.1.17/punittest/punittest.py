#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from .testcase import Meta
from .testcase import skip, skip_if, tag, data, list_data
from .utils.logger import logger


class PUnittest(unittest.TestCase, metaclass=Meta):
    Exc_Stack = []
    skip = skip
    skip_if = skip_if
    tag = tag
    data = data
    list_data = list_data

    def setUp(self):
        logger.info(' Start '.center(100, '*'))

    def tearDown(self):
        logger.info(' End '.center(100, '*'))
        logger.info('')

    def clear_exc_stack(self):
        self.Exc_Stack.clear()

    def raise_exc(self):
        if self.Exc_Stack:
            exc_text = ', AssertionError: '.join(str(x) for x in self.Exc_Stack)
            self.clear_exc_stack()
            raise AssertionError(exc_text)

    def assertEqual(self, first, second, msg=None):
        super(PUnittest, self).assertEqual(first, second, msg=msg)

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        super(PUnittest, self).assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    def assertDictEqual(self, d1, d2, msg=None):
        super(PUnittest, self).assertDictEqual(d1=d1, d2=d2, msg=msg)

    def assertListEqual(self, list1, list2, msg=None):
        super(PUnittest, self).assertListEqual(list1=list1, list2=list2, msg=msg)

    def assertSetEqual(self, set1, set2, msg=None):
        super(PUnittest, self).assertSetEqual(set1=set1, set2=set2, msg=msg)

    def assertFalse(self, expr, msg=None):
        super(PUnittest, self).assertFalse(expr, msg=msg)

    def assertTrue(self, expr, msg=None):
        super(PUnittest, self).assertTrue(expr, msg=msg)

    def assertIn(self, member, container, msg=None):
        super(PUnittest, self).assertIn(member, container, msg=msg)

    def assertIs(self, expr1, expr2, msg=None):
        super(PUnittest, self).assertIs(expr1, expr2, msg=msg)

    def assertIsInstance(self, obj, cls, msg=None):
        super(PUnittest, self).assertIsInstance(obj, cls, msg=msg)

    def assertIsNone(self, obj, msg=None):
        super(PUnittest, self).assertIsNone(obj, msg=msg)

    def assertIsNotNone(self, obj, msg=None):
        super(PUnittest, self).assertIsNotNone(obj, msg=msg)

    def assertNotIn(self, member, container, msg=None):
        super(PUnittest, self).assertNotIn(member, container, msg=msg)

    def assertNotEqual(self, first, second, msg=None):
        super(PUnittest, self).assertNotEqual(first, second, msg=msg)

    def assertGreater(self, a, b, msg=None):
        super(PUnittest, self).assertGreater(a, b, msg=msg)

    def assertGreaterEqual(self, a, b, msg=None):
        super(PUnittest, self).assertGreaterEqual(a, b, msg=msg)

    def assertLess(self, a, b, msg=None):
        super(PUnittest, self).assertLess(a, b, msg=msg)

    def assertLessEqual(self, a, b, msg=None):
        super(PUnittest, self).assertLessEqual(a, b, msg=msg)

    def assertMultiLineEqual(self, first, second, msg=None):
        if first != second:
            standardMsg = '{} != {}'.format(first, second)
            self.fail(self._formatMessage(msg, standardMsg))
