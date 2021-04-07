from part.search.main.proto_template import protoTemplate

class Yandex(protoTemplate):
  """docstring for Google"""
  def __init__(self):
    super().__init__()
    self.header.update({
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1'
    })
    self.proxies = {
     "http": "http://107.152.47.41:8080",
     "https": "https://107.152.47.41:8080"
    }
    self.session = self.requests.Session()
    self.url = 'http://yandex.ua/search/?'
    self.page = 1

    self.url_params = {
      'list': {
        'lr': 143,
        'p': 0,
        'format': 'json',
        'text': '_it_'
      },
      'skip': []
    }

  def add_params(self):
    self.session.verify = False
    _list = []
    for key in self.url_params['list']:
      if key not in self.url_params['skip']:
        value = self.url_params['list'][key]
        _list.append(key + '=' + str(value))

    param_list = '&'.join(_list)
    self.url = self.url + param_list

  def look (self, it='', page=0):
    self.page = page
    self.add_params()
    self.query = '+'.join(it.split())
    response = self.session.get(
      self.url.replace('_it_', self.query), 
      headers=self.header,
      proxies=self.proxies
    )
    soup = self.bs(response.text, "html.parser")
    return self.parser(soup)

  def parser (self, soup):
    self.output = []
    self.isolator = []
    # if self.page == 0:
      # main = soup.find('div', {'class': 'main', 'id': 'main'})
      # center_col = main.find('div', {'id': 'center_col'})
      # navigation = soup.find('div', {'role': 'navigation'})
      # print(navigation.span.h1)

    print(soup)
    return
    for wrapper_item in soup.find_all('div', {'class':'results'}):
      pass

    return self.output


