# https://github.com/googlemaps/google-maps-services-python/tree/master
#The URL above is the github repo provided by Google Maps for Developers, its a python repo that has the needed libraries.
#googlemaps library is installed. Check to see if I need anything else??? Maybe Beautiful soup??

import googlemaps
import pandas as pd
import random

def miles_to_meters(miles):
    try:
        return miles * 1609.34
    except:
        return 0

def lat_long_from_zipcode(zipcode, gmaps_client):
    try:
        geocode_result = gmaps_client.geocode(zipcode)
        if geocode_result and len(geocode_result) > 0:
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            return lat, lng
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None


api_key = open('api key.txt', 'r').read()


gmaps = googlemaps.Client(api_key)


user_zipcode = input("Please enter your zipcode: ")
type_of_culture_filter = input("What type of culture is the food from? i.e(American, Mexican, Chinese, etc) ")


latitude, longitude = lat_long_from_zipcode(user_zipcode, gmaps)
user_location = (latitude, longitude)
search_words = 'restaurants ' + type_of_culture_filter
user_radius = miles_to_meters(10)
restaurant_list = []

gmaps_response = gmaps.places_nearby(
    location=user_location,
    keyword=search_words,
    radius=user_radius
)

if 'results' in gmaps_response:
    for place in gmaps_response['results']:
        name = place.get('name')
        address = place.get('vicinity')
        rating = place.get('rating', 'No rating') 
        place_id = place.get('place_id')
        restaurant_lati = place['geometry']['location']['lat']
        restaurant_long = place['geometry']['location']['lng']

        restaurant = {
            'name': name,
            'address': address,
            'rating': rating,
            'latitude': restaurant_lati, 
            'longitude': restaurant_long, 
            'place_id': place_id
        }
        restaurant_list.append(restaurant)

    if restaurant_list:
        random_restaurant = random.choice(restaurant_list)
        print("Here's a random restaurant you might like:")
        print(f"Name: {random_restaurant['name']}")
        print(f"Address: {random_restaurant['address']}")
        print(f"Rating: {random_restaurant['rating']}")
        
    else:
        print("No restaurants found with the given filters.")

else:
    print("No results found.")



if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Could not find longitude and latitude for the zipcode.")
