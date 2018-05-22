import json
import sys
import unittest

from io import StringIO
from bs4 import BeautifulSoup
import requests
import re
from requests import HTTPError


class DeadLinks:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.dead_data = {'url': self.url,
                          '404': {
                              'size': 0,
                              'urls': []
                          },
                          '50x': {
                              'size': 0,
                              'urls': []
                          },
                          'dead': 0,
                          'total': 0}

    def get_links(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.findAll('a', attrs={'href': re.compile("^https*://")}):
            self.links.append(link.get('href'))
        return soup

    def get_responses(self):
        for link in self.links:
            try:
                request = requests.get(link)
                if request.status_code == 404:
                    self.dead_data['404']['urls'].append(link)
                if request.status_code >= 500:
                    self.dead_data['50x']['urls'].append(link)
            except HTTPError:
                print(HTTPError.code)
        self.dead_data['404']['size'] = len(self.dead_data.get('404').get('urls'))
        self.dead_data['50x']['size'] = len(self.dead_data.get('50x').get('urls'))
        self.dead_data['dead']= self.dead_data['404']['size'] + self.dead_data['50x']['size']
        self.dead_data['total'] = len(self.links)

class MyTest(unittest.TestCase):
    def test_url(self):
        dead_links = DeadLinks("https://try.github.io/levels/1/challenges/1")
        self.assertEqual(dead_links.url, "https://try.github.io/levels/1/challenges/1")

    def test_json_output(self):
        saved_stdout = sys.stdout
        dead_links = DeadLinks("https://try.github.io/levels/1/challenges/1")
        try:
            capturedOutput = StringIO()
            sys.stdout = capturedOutput
            dead_links.get_links()
            dead_links.get_responses()
            json_out = json.loads(json.dumps(dead_links.dead_data, indent=1, sort_keys=True))
            print(json_out['404']['urls'][0])
            sys.stdout = sys.__stdout__
            self.assertEqual(capturedOutput.getvalue(), "https://twitter.com/share?url=http://bit.ly/TryGit&via=codeschool&text=I'm%20learning%20how%20to%20push%20it%20with%20Try%20Git!%20#trygit\n")
        finally:
            sys.stdout = saved_stdout

def main(url):
    dead_links = DeadLinks(url)
    dead_links.get_links()
    dead_links.get_responses()
    print(json.dumps(dead_links.dead_data, indent=1, sort_keys=True))

if __name__ == '__main__':
    main(sys.argv[1])
    unittest.main(argv=['first-arg-is-ignored'])