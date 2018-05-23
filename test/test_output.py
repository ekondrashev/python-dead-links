#!/usr/bin/env python
#-*- coding:utf-8 -*-
import unittest
import json
from subprocess import Popen, PIPE, STDOUT


class OutputTests(unittest.TestCase):
    """Testing the correctness of the script output data"""

    @classmethod
    def setUpClass(cls):
        """Running the script and retrieving data"""
        cls._url = 'http://massage.zt.ua'
        p = Popen(['python', 'main.py', cls._url], stderr=STDOUT, stdout=PIPE, shell=True)
        cls._stdout = p.stdout.read()

    @classmethod
    def tearDownClass(cls):
        """Resetting data"""
        cls._stdout = ''

    def test_url_to_check(self):
        """Verification of the tested url-address"""
        actual = json.loads(self._stdout).get('url')
        self.assertEqual(actual, self._url)

    def test_urls_404(self):
        """Checking URLs with status 404"""
        actual = json.loads(self._stdout).get('404')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    def test_urls_50x(self):
        """Checking URLs with status 50x"""
        actual = json.loads(self._stdout).get('50x')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    def test_total_dead_urls(self):
        """Checking the total number of broken URLs"""
        actual = json.loads(self._stdout).get('dead')
        self.assertEqual(actual, 0)

    def test_total_urls(self):
        """Checking the total number of URLs found on the page"""
        actual = json.loads(self._stdout).get('total')
        self.assertEqual(actual, 17)


if __name__ == "__main__":
    unittest.main()
