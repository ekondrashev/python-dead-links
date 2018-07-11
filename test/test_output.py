#!/usr/bin/env python
#-*- coding:utf-8 -*-
import unittest
from http.server import SimpleHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE
from threading import Thread
import socket
import json


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Configuring a simple HTTP-request handler"""
    buffer = 1
    log_file = open('test/server.log', 'w', buffer)
    
    def log_message(self, format, *args):
        """Configuring the logging of requests to the HTTP-server"""
        self.log_file.write("%s - - [%s] %s\n" %
            (self.client_address[0],
            self.log_date_time_string(),
            format%args))


class OutputTests(unittest.TestCase):
    """Testing the correctness of the script output data"""

    @classmethod
    def setUpClass(cls):
        """Running the HTTP-server on an idle port"""
        sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        cls._address, cls._port = sock.getsockname()
        sock.close()
        test_server = HTTPServer(('localhost', cls._port), CustomHTTPRequestHandler)
        server_thread = Thread(target=test_server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()

    def setUp(self):
        """Initializing the URL value before running each test"""
        self._url = 'http://localhost:{port}/test/pages/'.format(port=self._port)

    def tearDown(self):
        """Clear the URL value after each test"""
        self._url = None

    def check_html(self, page):
        """Running the main script and getting the results of its work"""
        self._url += page
        output, err = Popen(['python', 'main.py', self._url], stdout=PIPE).communicate()
        return json.loads(output), err

    def test_url_to_check(self):
        """Verification of the tested url-address"""
        actual, err = self.check_html('index.html')
        self.assertEqual(actual.get('url'), self._url)
        self.assertIsNone(err, "No errors found")

    def test_urls_404(self):
        """Checking URLs with status code 404"""
        actual, err = self.check_html('index.html')
        self.assertEqual(actual.get('404').get('size'), 4)
        self.assertEqual(len(actual.get('404').get('urls')), actual.get('404').get('size'))
        self.assertIsNone(err, "No errors found")

    def test_urls_50x(self):
        """Checking URLs with status code 50x"""
        actual, err = self.check_html('index.html')
        self.assertEqual(actual.get('50x').get('size'), 1)
        self.assertEqual(len(actual.get('50x').get('urls')), actual.get('50x').get('size'))
        self.assertIsNone(err, "No errors found")

    def test_total_dead_urls(self):
        """Checking the total number of broken URLs"""
        actual, err = self.check_html('index.html')
        self.assertEqual(actual.get('dead'), 5)
        self.assertIsNone(err, "No errors found")

    def test_total_urls(self):
        """Checking the total number of URLs found on the page"""
        actual, err = self.check_html('index.html')
        self.assertEqual(actual.get('total'), 7)
        self.assertIsNone(err, "No errors found")


if __name__ == "__main__":
    unittest.main()
