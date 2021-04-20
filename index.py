from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from part.search.main.template.google import Google
from part.search.main.template.bing import Bing
from part.search.main.template.yandex import Yandex
from part.search.main.template.yahoo import Yahoo
from part.search.main.template.duckduckgo import Duckduckgo
app = Flask(__name__, template_folder='view', static_url_path='')
CORS(app)

@app.route("/", methods = ['GET'])
def home():
  return render_template('home.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('view/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('view/css', path)

@app.route('/look/<string:it>/page/<int:page_number>', methods = ['GET'])
def look(it, page_number):
  result = []
  
  link_list = []

  google = Google()
  bing = Bing()
  yandex = Yandex()
  yahoo = Yahoo()
  # duckduckgo = Duckduckgo()

  google.link_list = link_list
  google_result = google.look(it=it, page=page_number)
  result.extend(google_result)
  link_list = google.link_list
  # print('google_')
  # print(link_list)

  yahoo.link_list = link_list
  yahoo_result = yahoo.look(it=it, page=page_number)
  result.extend(yahoo_result)
  link_list = yahoo.link_list
  # print('yahoo_')
  # print(link_list)

  bing.link_list = link_list
  bing_result = bing.look(it=it, page=page_number)
  result.extend(bing_result)
  link_list = bing.link_list
  # print('bing_')
  # print(link_list)

  # duckduckgo.look(it=it, page=page_number)
  # result.update(duckduckgo.look(it=it, page=page_number))
  # finder = yandex.look(it=it, page=page_number)
  # print(finder)


  def drop_bublicate(result):
    for i in len(result):
      if result[i]['url'] == result[i+1]['url']:
        pass

  return jsonify(result)

if __name__ == "__main__":
  app.run()
