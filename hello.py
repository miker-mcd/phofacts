import os
from flask import Flask, render_template, jsonify
import requests
import imghdr
from dotenv import load_dotenv
app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
place_consumer_key = os.getenv('GOOGLE_PLACES_KEY')
# Your Google Maps Embed API Key
maps_consumer_key = os.getenv('GOOGLE_MAPS_EMBED_KEY')

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo?"
maps_url = "https://www.google.com/maps/embed/v1/search?key="

@app.route("/")
def show_restaurants():
  return render_template('index.html')

@app.route("/sendRequest/<string:query>")
def results(query):
  search_payload = {"key":place_consumer_key, "query": "pho+restaurants+in+" + query}
  search_req = requests.get(search_url, params=search_payload)
  search_json = search_req.json()

  map_req = maps_url + maps_consumer_key + "&zoom=12&q=pho+restaurants+in+" + query

  map = "<iframe width='450' height='250' frameborder='0' style='border:0' src='" + map_req + "' allowfullscreen></iframe>"

  restaurants = search_json["results"][0]
  restaurant_name = search_json["results"][0]["name"]

  return map
