#################### Import all relevant libraries ##################################################
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
# from invokes import invoke_http

from math import radians, sin, cos, sqrt, asin

app = Flask(__name__)
CORS(app)

#################### Converting Customer Location to Lat and Long ####################################

API_KEY = 'example'

#this is now hardcoded but need to change the address to collect from the NearBy MS
address = '1 hack drive, menlo park, CA'

params  = {
    'key': API_KEY,
    'address': address
}

base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
response = requests.get(base_url,params=params).json()
response.keys()

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # raise an exception for 4xx and 5xx errors
    data = response.json()
    if data['status'] == 'OK':
        geometry = data['results'][0]['geometry']
        lat = geometry['location']['lat']
        lon = geometry['location']['lng']
        print(f'Latitude: {lat}, Longitude: {lon}')
    else:
        print(f'Geocoding failed. Status: {data["status"]}')
except requests.exceptions.HTTPError as err:
    print(f'Error: {err}')
except requests.exceptions.RequestException as err:
    print(f'Request error: {err}')


################# Finding the nearest location ########################################################


@app.route('/location')
def find_nearest_location():
    data = request.json

    #starting_location = {lat:...., lng:.....}
    #restaurant_location = [{lat:...., lng:.....},{lat:...., lng:.....},{lat:...., lng:.....}]
    customer_location = data['starting_location'] #make sure that this is in the complex MS and under payload 
    restaurant_location = data['restaurant_location'] #make sure that this is in the complex MS and under payload 

    # process the locations
    top_20_locations = get_nearest_locations(customer_location['lat'],customer_location['lng'],restaurant_location)

    # check if the .json thing works for here
    nearest_locations = top_20_locations.json()
    return jsonify({
        'status': 'success',
        'nearest_locations': nearest_locations
    })


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the Earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    return c * r

def get_nearest_locations(latitude, longitude, locations):
    """
    Get the nearest top 20 locations based on the provided latitude, longitude, and list of locations
    """
    # Calculate distances between the given location and all locations in the list
    distances = []
    for location in locations:
        dist = haversine(latitude, longitude, location['latitude'], location['longitude'])
        distances.append((location, dist))
    
    # Sort the list of locations by distance in ascending order and return the top 20 locations
    sorted_distances = sorted(distances, key=lambda x: x[1])
    nearest_locations = [x[0] for x in sorted_distances[:20]]
    
    return nearest_locations


