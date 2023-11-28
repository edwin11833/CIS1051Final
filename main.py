# https://github.com/googlemaps/google-maps-services-python/tree/master
#The URL above is the github repo provided by Google Maps for Developers, its a python repo that has the needed libraries.
#googlemaps library is installed. Check to see if I need anything else??? Maybe Beautiful soup??

import random
import googlemaps

api_key = ""

user_zipcode = int(input("Please enter your zipcode: "))


rest_list = ['applebees','fridays','chipotle','mcdonalds', 'olive garden','red lobster','five guys'] 
#eventually this has to be a dictionary for filters

def rand_choice():
  pick = random.choice(rest_list)
  return pick

if user_zipcode in googlemaps:
  googlemaps