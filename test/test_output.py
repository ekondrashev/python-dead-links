#!/usr/bin/env python
#-*- coding:utf-8 -*-
import unittest
from http.server import SimpleHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
import socket
import json


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    buffer = 1
    log_file = open('test/server.log', 'w', buffer)
    
    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
            (self.client_address[0],
            self.log_date_time_string(),
            format%args))


class OutputTests(unittest.TestCase):
    """Testing the correctness of the script output data"""

    @classmethod
    def setUpClass(cls):
        """Running the HTTP server"""
        sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        cls._address, cls._port = sock.getsockname()
        sock.close()
        test_server = HTTPServer(('localhost', cls._port), CustomHTTPRequestHandler)
        server_thread = Thread(target=test_server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()

    def setUp(self):
        self._url = 'http://localhost:{port}/test/pages/'.format(port=self._port)

    def tearDown(self):
        self._url = None

    def check_html(self, page):
        self._url += page
        p = Popen(['env\\scripts\\python.exe', 'main.py', self._url], stderr=STDOUT, stdout=PIPE, shell=True)
        z=p.stdout.read()
        print(str(z))
        return json.loads(z)

    def test_url_to_check(self):
        """Verification of the tested url-address"""
        actual = self.check_html('index.html').get('url')
        self.assertEqual(actual, self._url)

    @unittest.skip('')
    def test_urls_404(self):
        """Checking URLs with status 404"""
        actual = self.check_html('index.html').get('404')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    @unittest.skip('')
    def test_urls_50x(self):
        """Checking URLs with status 50x"""
        actual = self.check_html('index.html').get('50x')
        self.assertEqual(actual.get('size'), 0)
        self.assertEqual(actual.get('urls'), [])
        self.assertEqual(len(actual.get('urls')), actual.get('size'))

    @unittest.skip('')
    def test_total_dead_urls(self):
        """Checking the total number of broken URLs"""
        actual = self.check_html('index.html').get('dead')
        self.assertEqual(actual, 0)

    @unittest.skip('')
    def test_total_urls(self):
        """Checking the total number of URLs found on the page"""
        actual = self.check_html('index.html').get('total')
        self.assertEqual(actual, 17)


if __name__ == "__main__":
    unittest.main()
