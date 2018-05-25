#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup, SoupStrainer
import sys
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


class FilteredLinks(object):

    def __init__(self, links, live):
        self._links = links
        self._live = live

    def __iter__(self):
        for link in self._links:
            response = requests.head(link, allow_redirects=True)
            if (self._live and response.ok)\
                or (not self._live and not response.ok):
                yield (response.status_code, response.url)

    def __len__(self):
        return len([link for link in self])


class LiveLinks(FilteredLinks):

    def __init__(self, links):
        super(LiveLinks, self).__init__(links, True)


class DeadLinks(FilteredLinks):

    def __init__(self, links):
        super(DeadLinks, self).__init__(links, False)


def check_url(url):
    all_links = Links(url)
    result = {
        'url': url,
        '404': {
            'size': 0,
            'urls': []
        },
        '50x': {
            'size': 0,
            'urls': []
        },
        'dead': len(DeadLinks(all_links)),
        'total': len(all_links)
    }
    for (status, link) in LiveLinks(all_links):
        if status==404:
            result['404']['urls'].append(link)
            result['404']['size']+=1
        elif status>=500:
            result['50x']['urls'].append(link)
            result['50x']['size']+=1
        return result


if __name__ == '__main__':
    print(json.dumps(check_url(sys.argv[1]), indent=4))
