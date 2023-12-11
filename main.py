# https://github.com/googlemaps/google-maps-services-python/tree/master
#The URL above is the github repo provided by Google Maps for Developers, its a python repo that has the needed libraries.
#googlemaps library is installed. Check to see if I need anything else??? Maybe Beautiful soup?? Maybe Pygame? Maybe Tkinter?
#In order for the code to work, you need your own API key from googlemaps dev website. The python libraries - tkinter, googlemaps, and random. 
#ttk from tkinter is like dlc for tkinter, it adds buttons and dropdown menus. 

import tkinter as tk
from tkinter import ttk
import googlemaps
import random


#Googlemaps dev client uses meters, this function changes our usual way of thinking in miles to meters
def miles_to_meters(miles): 
    try:
        return miles * 1609.34
    except:
        return 0

#From the googlemaps docs, they go by latitude and longitude.
#so this function changes the zipcode into coordinates(Lati and Long)
#A zipcode is a wide area so im assuming it just tries to grab the coords of the center of a zipcode.
#According to googlemaps docs, the exception handles any wrong api keys or network issues when trying to get lat and long from zipcode.
def lat_long_from_zipcode(zipcode, gmaps_client):
    try:
        geocode_result = gmaps_client.geocode(zipcode)
        if geocode_result and len(geocode_result) > 0:
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            return lat, lng
        else:
            return None, None
    except Exception as error:
        print(f"Error occurred try again: {error}")
        return None, None

#gets the api key from my text file which will not be on GitHub for security reasons.
#When trying to use the program, you need to set your own API Key from GoogleMaps Dev website.
api_key = open('api key.txt', 'r').read()
gmaps = googlemaps.Client(api_key)

#Makes the GUI window from the library Tkinter
root = tk.Tk()
root.title("Restaurant Finder")
root.geometry("600x400")  #window size


#labels for zipcode dropdown
label1 = tk.Label(root, text="Enter your zipcode:")
label1.pack()
#allows text/dropdown selection on gui
zipcode_entry = tk.Entry(root)
zipcode_entry.pack()

# labels for type of culture for food dropdown menu
label2 = tk.Label(root, text="Select the type of food culture:")
label2.pack()

culture_list = sorted(["American", "Mexican", "Chinese", "Italian", "Indian", "Thai", "Japanese", "Mediterranean"])
culture_entry = ttk.Combobox(root, values=culture_list)
culture_entry.pack()

# labels for radius in miles dropdown menu
label3 = tk.Label(root, text="Select search radius in miles:")
label3.pack()

radius_options = [5, 10, 15, 20, 25, 30]
radius_entry = ttk.Combobox(root, values=radius_options)
radius_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

#google maps client search function linked to labels above
def gmaps_search():
    user_zipcode = zipcode_entry.get()
    type_of_culture_filter = culture_entry.get()
    selected_radius = radius_entry.get()
#radius, lati and long from zipcode to lat and long function.
#also search words are saved with the culture and restaurant search
    latitude, longitude = lat_long_from_zipcode(user_zipcode, gmaps)
    user_location = (latitude, longitude)
    search_words = 'restaurants ' + type_of_culture_filter
    user_radius = miles_to_meters(int(selected_radius))

    restaurant_list = []
    #googlemaps client has a places library within itself that helps you find businesses near a location with parameters
    gmaps_response = gmaps.places_nearby(
        location=user_location,
        keyword=search_words,
        radius=user_radius
    )
#makes sure there are results, then adds them to a dictionary
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
#applies print onto tkinter window
        if restaurant_list:
            random_restaurant = random.choice(restaurant_list)
            result_label.config(text=f"Here's a random restaurant you might like:\nName: {random_restaurant['name']}\nAddress: {random_restaurant['address']}\nRating: {random_restaurant['rating']}\nLatitude: {latitude}, Longitude: {longitude}")
        else:
            result_label.config(text="No restaurants found with the given filters.")
    else:
        result_label.config(text="No results found.")

search_button = tk.Button(root, text="Search", command=gmaps_search)
search_button.pack()

#starts program
root.mainloop()
