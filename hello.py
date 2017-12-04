import os
from flask import Flask, render_template, jsonify, Markup, redirect, url_for, request
import requests
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
def home():
  return render_template('index.html')

@app.route('/restaurants', methods=['POST'])
def search_restaurants():
  zipcode = request.form['query']
  search_payload = {"key":place_consumer_key, "query": "pho+restaurants+in+" + zipcode}
  search_req = requests.get(search_url, params=search_payload)
  search_json = search_req.json()

  map_req = maps_url + maps_consumer_key + Markup('&zoom=12&q=pho+restaurants+in+') + zipcode

  map = Markup('<iframe width="450" height="250" frameborder="0" style="border:0" src="') + map_req + Markup('" allowfullscreen></iframe>')

  restaurants = search_json["results"][0]
  restaurant_name = search_json["results"][0]["name"]

  return render_template('show_restaurants.html', map=map, restaurant_name=restaurant_name)
