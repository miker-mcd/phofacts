import os
from flask import Flask, render_template, jsonify
import requests
from dotenv import load_dotenv
app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
place_consumer_key = os.getenv('GOOGLE_PLACES_KEY')

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/", methods=["GET"])
# def hello_world():
#   return "Hello, World!"
def show_restaurants():
  return render_template('index.html')

@app.route("/sendRequest/<string:query>")
def results(query):
  search_payload = {"key":place_consumer_key, "query":query}
  search_req = requests.get(search_url, params=search_payload)
  search_json = search_req.json()

  place_id = search_json["results"][0]["place_id"]

  details_payload = {"key": place_consumer_key, "placeid": place_id}
  details_resp = requests.get(details_url, params=details_payload)
  details_json = details_resp.json()

  url = details_json["result"]["url"]
  return jsonify({'result' : url})
