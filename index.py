from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from part.search.main.template.google import Google
from part.search.main.template.yandex import Yandex
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
  google = Google()
  yandex = Yandex()
  result = google.look(it=it, page=page_number)
  # duckduckgo = Duckduckgo()
  # duckduckgo.look(it=it, page=page_number)
  # result.update(duckduckgo.look(it=it, page=page_number))
  finder = yandex.look(it=it, page=page_number)
  print(finder)
  return jsonify(result)

if __name__ == "__main__":
  app.run()
