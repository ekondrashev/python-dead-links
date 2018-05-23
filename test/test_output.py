#!/usr/bin/env python
#-*- coding:utf-8 -*-
import unittest
import json
from subprocess import Popen, PIPE, STDOUT


class OutputTests(unittest.TestCase):
    """x"""

    @classmethod
    def setUpClass(cls):
        cls._url = 'http://massage.zt.ua'
        p = Popen(['python', 'main.py', cls._url], stderr=STDOUT, stdout=PIPE, shell=True)
        cls._stdout = p.stdout.read()

    @classmethod
    def tearDownClass(cls):
        cls._stdout = ''

    def test_url_to_check(self):
        """x"""
        actual = json.loads(self._stdout).get('url')
        self.assertEqual(actual, self._url)

    def test_urls_404(self):
        """x"""
        actual = json.loads(self._stdout).get('404')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    def test_urls_50x(self):
        """x"""
        actual = json.loads(self._stdout).get('50x')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    def test_total_dead_urls(self):
        """x"""
        actual = json.loads(self._stdout).get('dead')
        self.assertEqual(actual, 0)

    def test_total_urls(self):
        """x"""
        actual = json.loads(self._stdout).get('total')
        self.assertEqual(actual, 17)


if __name__ == "__main__":
    unittest.main()
