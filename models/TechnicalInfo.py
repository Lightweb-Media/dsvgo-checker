
import pydig
import requests

class TechnicalInfo():
    def __init__(self, domain, parsed_url):
        label = 'Technische Informationen'
        self.label = label
        self.domain = domain
        self.protocol = parsed_url.scheme
        self.netloc = parsed_url.netloc

    def run(self):
        self.ip = pydig.query(self.netloc, 'A')
        self.txt = pydig.query(self.netloc, 'txt')
        headers = requests.get(self.domain).headers
        self.server = headers['Server']
       # self.link = headers['link']

        if(([x for x in self.txt if 'spf' in x])):
            self.spf = 'True'

        if(([x for x in self.txt if 'dkim' in x])):
            self.dkim = 'False'
