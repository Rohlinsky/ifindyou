from part.search.main.proto_template import protoTemplate

class Yahoo(protoTemplate):
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
    self.session = self.requests.Session()
    self.url = 'https://search.yahoo.com/search?'
    self.page = 1
    self.country = ['countryCA', 'countryUA']
    self.lang = ['lang_fr', 'lang_ua']
    self.url_params = {
      'list': {
        'start': 0,
        # 'pstart': 0,
        'num': 10,
        # 'b': 10,
        'p': '_it_',
        # 'cr': self.country[1],
        # 'lr': self.lang[1],
        'fr': 'yfp-t',
        'ei': 'UTF-8',
        'fp': 1,
        'output': 'xml_no_dtd',
        'cx': '00255077836266642015:u-scht7a-8i'
      },
      'skip': [
        'output'
      ]
    }

  def add_params(self):
    self.url_params['list']['start'] = self.url_params['list']['num'] * self.page
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
      headers=self.header
    )
    soup = self.bs(response.text, "html.parser")
    # print(soup)
    return self.parser(soup)

  def parser (self, soup):
    self.output = []
    self.isolator = []
    # if self.page == 0:
      # main = soup.find('div', {'class': 'main', 'id': 'main'})
      # center_col = main.find('div', {'id': 'center_col'})
      # navigation = soup.find('div', {'role': 'navigation'})
      # print(navigation.span.h1)

    result_list = soup.find_all('ol', {'class':'reg searchCenterMiddle'})
    result_list = result_list[0] if len(result_list) > 0 else []
    result_list = result_list.select('ol > li')
    for wrapper_item in result_list:
      item = wrapper_item.div
      uri = item.div.h3.a["href"] if item.div.h3.a and item.div.h3.a.has_attr('href') else ''
      # print(wrapper_item)
      # continue
      title = item.div.h3.a.text if item.div.h3 else ''
      # description = item.div.span.span.text if item.div.span.span is not None else ''
      description = item.div.p.text if item.div.p and item.div.p else ''
      # item = searchWrapper.select('cite').text
      result = {
        'url': uri,
        'text': title,
        'description': description,
        'type': {
          'logo': 'https://s.yimg.com/pv/static/img/yahoo-search-logo-88x21.png',
          'name': 'google.com'
        }
      }
      # print(result)
      # continue

      if not item.div.h3.a or not item.div.h3.a.has_attr('href'):
        self.isolator.append(item.div)
      else:
        self.output.append(result)

    if not len(self.isolator) == 0:
      print('---- Warning:')
      for item in self.isolator:
        print(soup)
        print(item)

    return self.output


