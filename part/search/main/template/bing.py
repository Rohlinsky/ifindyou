from part.search.main.proto_template import protoTemplate

class Bing(protoTemplate):
  """docstring for Bing"""
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
    self.url = 'http://www.bing.com/search?'
    self.page = 1
    self.country = ['countryCA', 'countryUA']
    self.lang = ['lang_fr', 'lang_ua']
    self.url_params = {
      'list': {
        'start': 0,
        'num': 10,
        'q': '_it_',
        'pq': '_it_',
        'form': 'QBLH',
        'sp': '-1',
        'sc': '0-11',
        'qs': 'n',
        'output': 'xml_no_dtd',
        'cvid': '3899808C2A454B2384955BE2EBE279EA'
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
    # print(soup)
    return self.parser(soup)

  def parser (self, soup):
    self.output = []
    self.isolator = []
    self.link_list = []

    result_list = soup.find_all('ol', {'id':'b_results'})
    result_list = result_list[0] if len(result_list) > 0 else []
    # print(result_list)

    if result_list != []:
      result_list = result_list.select('ol > li')

      # TODO: First item add results

      for wrapper_item in result_list:
        item = wrapper_item.div
        uri = item.h2.a["href"] if item.h2 and item.h2.a and item.h2.a.has_attr('href') else ''

        if uri in self.link_list:
          continue
        else:
          self.link_list.append(uri)

        title = item.h2.a.text if item.h2 and item.h2.a else ''

        description_wrapper = item.parent.select('.b_caption')
        if len(description_wrapper) > 0:
          description_wrapper = description_wrapper[0]
          description = description_wrapper.p.text if description_wrapper.p is not None else ''
        else:
          description = ''

        result = {
          'url': uri,
          'title': title,
          'description': description,
          'type': {
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/e/e8/Microsoft_Bing_logo.svg',
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
        print(item)

    return self.output


