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

# TODO: Replace with dynamic location info from user input or geolocation instead of explicit San Diego region.
@app.route("/")
def show_restaurants():
  return render_template('index.html')

# The commented code below was a test for using the Google Places API from this guide (https://www.youtube.com/watch?v=kWncnBBxoJ4)
@app.route("/sendRequest/<string:query>")
def results(query):
  # search_payload = {"key":place_consumer_key, "query":query}
  # search_req = requests.get(search_url, params=search_payload)
  # search_json = search_req.json()

  # place_id = search_json["results"][0]["place_id"]
  # place_location = search_json["results"][0]["geometry"]["location"]

  # details_payload = {"key": place_consumer_key, "placeid": place_id}
  # details_resp = requests.get(details_url, params=details_payload)
  # details_json = details_resp.json()

  # photo_id = search_json["results"][0]["photos"][0]["photo_reference"]

  # photo_payload = {"key":place_consumer_key, "maxwidth": 500, "photoreference":photo_id}
  # photo_request = requests.get(photos_url, params=photo_payload)

  # photo_type = imghdr.what("", photo_request.content)
  # photo_name = "static/" + query + "." + photo_type

  # with open(photo_name, "wb") as photo:
    # photo.write(photo_request.content)

  # url = details_json["result"]["url"]

  # return "<img src=" + photo_name + ">"
  # return jsonify({'result' : url})
  # return jsonify(place_location)

  map_req = maps_url + maps_consumer_key + "&zoom=12&q=pho+restaurants+in+" + query

  return "<iframe width='450' height='250' frameborder='0' style='border:0' src=" + map_req + " allowfullscreen></iframe>"
