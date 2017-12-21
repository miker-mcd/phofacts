import os
from flask import Flask, render_template, jsonify, Markup, redirect, url_for, request
import requests, time
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

def assign_imgsrc(restaurants,photo_sources):
  count = 0
  for restaurant in restaurants:
      restaurant['img_src'] = photo_sources[count]
      count += 1
  return restaurants;

@app.route('/restaurants', methods=['POST'])
def search_restaurants():
  zipcode = request.form['query']
  search_payload = {"key":place_consumer_key, "query": "pho+restaurants+in+" + zipcode}
  search_req = requests.get(search_url, params=search_payload)
  search_json = search_req.json()

  map_req = maps_url + maps_consumer_key + Markup('&zoom=10&q=pho+restaurants+in+') + zipcode

  restaurants = search_json["results"]

  photo_list = collect_photos(restaurants)
  photo_ids = collect_photo_refs(photo_list)

  photo_sources = []
  count = 0
  for id in photo_ids:
    photo_payload = {"key": place_consumer_key, "maxwidth": 500, "photoreference": id}
    photo_request = requests.get(photos_url, params=photo_payload)
    photo_type = imghdr.what("", photo_request.content)
    photo_name = "static/" + zipcode + str(count) + "." + photo_type
    # with open(photo_name, "wb") as photo:
    #   photo.write(photo_request.content)
    photo_sources.append(photo_name)
    count += 1
    time.sleep(.300)

  assign_imgsrc(restaurants, photo_sources)

  return render_template('show_restaurants.html', map_req=map_req, restaurants=restaurants)
