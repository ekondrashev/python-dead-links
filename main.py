#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json


class Links(object):

    def __init__(self, url):
        self._url = url
        self._protocol = url.split('://')[0] if url.find('://')>0 else 'http'
        self._host = url.split('://')[1].split('/')[0]

    def __iter__(self):
        """Iteration over the collection of links found on the page"""
        response = requests.get(self._url, allow_redirects=True)
        for link in BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer('a')):
            if link.has_attr('href') and link.get('href'):
                url = link.get('href')
                if not url.startswith(self._protocol):
                    if not url.startswith(self._host):
                        url = '{}://{}/{}'.format(self._protocol, self._host, url)
                    else:
                        url = '{}://{}'.format(self._protocol, url)
                yield url

    def __len__(self):
        return len([link for link in self])
