from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class protoTemplate():
  """docstring for Google"""
  def __init__(self):
    self.header = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    self.query = ''
    # self.session = requests.Session()
    self.output = []
    self.url = ''
    self.bs = BeautifulSoup
    self.requests = requests
    self.page = {
      'list': [],
      'current': 0
    }

  def look (self, it):
    pass

  def parser (self, soup):
    pass


