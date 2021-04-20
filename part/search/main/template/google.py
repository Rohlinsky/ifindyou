from part.search.main.proto_template import protoTemplate

class Google(protoTemplate):
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
    self.url = 'http://www.google.com/search?'
    self.page = 1
    self.country = ['countryCA', 'countryUA']
    self.lang = ['lang_fr', 'lang_ua']
    self.url_params = {
      'list': {
        'start': 0,
        'num': 10,
        'q': '_it_',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'cr': self.country[1],
        'lr': self.lang[1],
        'client': 'google-csbe',
        'output': 'xml_no_dtd',
        'cx': '00255077836266642015:u-scht7a-8i'
      },
      'skip': [
        'output',
        'cr',
        'lr'
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
    print(soup)
    return self.parser(soup)

  def parser (self, soup):
    self.output = []
    self.isolator = []
    self.link_list = []
    # if self.page == 0:
      # main = soup.find('div', {'class': 'main', 'id': 'main'})
      # center_col = main.find('div', {'id': 'center_col'})
      # navigation = soup.find('div', {'role': 'navigation'})
      # print(navigation.span.h1)

    for wrapper_item in soup.find_all('div', {'class':'g'}):
      item = wrapper_item.div
      uri = item.div.a["href"] if item.div.a and item.div.a.has_attr('href') else ''

      if uri in self.link_list:
        continue
      else:
        self.link_list.append(uri)

      title = item.a.h3.text if item.a.h3 else ''
      # print(wrapper_item)
      # print('-----')
      description_wrapper = wrapper_item.select('div.g > div > div > div:nth-child(2)')
      if len(description_wrapper) > 0:
        description_wrapper = description_wrapper[0]
        description = description_wrapper.span.span.text if description_wrapper.span and description_wrapper.span.span else ''
      else:
        description = ''

      result = {
        'url': uri,
        'title': title,
        'description': description,
        'type': {
          'logo': 'http://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
          'name': 'google.com'
        }
      }
      # print(result)
      # continue

      if not item.div.a or not item.div.a.has_attr('href'):
        self.isolator.append(item.div)
      else:
        self.output.append(result)

    if not len(self.isolator) == 0:
      print('---- Warning:')
      for item in self.isolator:
        print(soup)
        print(item)

    return self.output


