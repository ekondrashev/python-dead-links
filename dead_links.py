import json
import sys

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

def main(url):
    dead_links = DeadLinks(url)
    dead_links.get_links()
    dead_links.get_responses()
    print(json.dumps(dead_links.dead_data, indent=1, sort_keys=True))

if __name__ == '__main__':
    main(sys.argv[1])