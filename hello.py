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

def collect_photos(restaurants):
  photos = []
  for restaurant in restaurants:
    photos.append(restaurant['photos'])
  return photos;

def collect_photo_refs(photos):
  photo_refs = []
  for photo in photos:
    photo_refs.append(photo[0]['photo_reference'])
  return photo_refs;

@app.route('/restaurants', methods=['POST'])
def search_restaurants():
  zipcode = request.form['query']
  search_payload = {"key":place_consumer_key, "query": "pho+restaurants+in+" + zipcode}
  search_req = requests.get(search_url, params=search_payload)
  search_json = search_req.json()

  map_req = maps_url + maps_consumer_key + Markup('&zoom=10&q=pho+restaurants+in+') + zipcode

  restaurants = search_json["results"]
  # print(restaurants[0]['photos'][0]['photo_reference'])

  photo_list = collect_photos(restaurants);
  print(collect_photo_refs(photo_list))

  return render_template('show_restaurants.html', map_req=map_req, restaurants=restaurants)

