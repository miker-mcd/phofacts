import os
from flask import Flask, render_template, jsonify, Markup, redirect, url_for, request
import requests, time
import imghdr
from dotenv import load_dotenv
try:
  from urllib.parse import quote
except ImportError:
  from urllib import quote

app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
place_consumer_key = os.getenv('GOOGLE_PLACES_KEY')
# Your Google Maps Embed API Key
maps_consumer_key = os.getenv('GOOGLE_MAPS_EMBED_KEY')
yelp_search_key = os.getenv('YELP_FUSION_KEY')

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo?"
maps_url = "https://www.google.com/maps/embed/v1/search?key="

yelp_host ="https://api.yelp.com"
yelp_search = "/v3/businesses/search"
business_path = "/v3/businesses/"

@app.route("/")
def home():
  return render_template('index.html')

def search_request(host, path, api_key, url_params=None):
  url_params = url_params or {}
  url = "{0}{1}".format(host, quote(path.encode("utf8")))
  headers = {
    "Authorization": "Bearer %s" % api_key,
  }

  response = requests.request("GET", url, headers=headers, params=url_params)

  return response.json()

def collect_photos(restaurants):
  photos = []
  for restaurant in restaurants:
    photos.append(restaurant['image_url'])
  return photos;

def collect_photo_refs(photos):
  photo_refs = []
  for photo in photos:
    photo_refs.append(photo[0]['photo_reference'])
  return photo_refs;

def assign_imgsrc(restaurants,photo_sources):
  count = 0
  for restaurant in restaurants:
      restaurant['img_src'] = photo_sources[count]
      count += 1
  return restaurants;

@app.route('/restaurants', methods=['POST'])
def search_restaurants():
  zipcode = request.form["query"]
  url_params = {"term": "pho+restaurants", "location": zipcode, "limit": 3}
  search_json = search_request(yelp_host, yelp_search, yelp_search_key, url_params=url_params)

  restaurants = search_json["businesses"]

  map_req = maps_url + maps_consumer_key + Markup('&zoom=10&q=pho+restaurants+in+') + zipcode

  return render_template('show_restaurants.html', map_req=map_req, restaurants=restaurants)
