#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import unittest
from fasttest_selenium.common import Var
from fasttest_selenium.result.test_result import TestResult
from fasttest_selenium.result.html_result import HTMLTestRunner


class TestRunner(unittest.TextTestRunner):

    def __init__(self,stream=sys.stderr,
                 descriptions=True, verbosity=1,
                 failfast=False, buffer=False,resultclass=None):
        unittest.TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is None:
            self.resultclass = TestResult
        else:
            self.resultclass = resultclass

    def _makeResult(self):
            return  self.resultclass(self.stream,self.descriptions,self.verbosity)

    def run(self, test):
        '''
        :param test:
        :return:
        '''
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        starTime = time.time()
        test(result)
        stopTime = time.time()
        html_file = os.path.join(Var.report,'report.html')
        fp = open(html_file,'wb')
        html_runner = HTMLTestRunner(stream=fp,
                                     title='Test Results',
                                     description='Test')
        html_runner.generateReport(result,starTime,stopTime)
        Var.all_result = result
        fp.close()

        result_path = os.path.join(Var.ROOT, 'result.properties')
        with open(result_path, "w") as f:
            f.write(f'report={result.report}\n')
            f.write(f'total={result.testsRun}\n')
            f.write(f'successes={len(result.successes)}\n')
            f.write(f'failures={len(result.failures)}\n')
            f.write(f'errors={len(result.errors)}\n')
            f.write(f'skipped={len(result.skipped)}\n')

        return result




