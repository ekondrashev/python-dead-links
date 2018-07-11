#!/usr/bin/python
#-*- coding:utf-8 -*-
import unittest
from test import test_output

testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(test_output.OutputTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(testSuite)
