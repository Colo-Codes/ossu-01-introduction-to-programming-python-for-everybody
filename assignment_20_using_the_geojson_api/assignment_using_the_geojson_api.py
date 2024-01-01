# Using the GeoJSON API
# =====================
# Source: https://www.py4e.com/tools/python-data/?PHPSESSID=2cf5b5f6915885a5fb679d2adb2793a6
#
# Assignment: Calling a JSON API
# ------------------------------
#
# In this assignment you will write a Python program somewhat similar to http://www.py4e.com/code3/geojson.py. The program will prompt 
# for a location, contact a web service and retrieve JSON for the web service and parse that data, and retrieve the first place_id from 
# the JSON. A place ID is a textual identifier that uniquely identifies a place as within Google Maps.
# API End Points
# 
# To complete this assignment, you should use this API endpoint that has a static subset of the Google Data:
# 
#   http://py4e-data.dr-chuck.net/json?
#
# This API uses the same parameter (address) as the Google API. This API also has no rate limit so you can test as often as you like. If 
# you visit the URL with no parameters, you get "No address..." response.
# To call the API, you need to include a key= parameter and provide the address that you are requesting as the address= parameter that is 
# properly URL encoded using the urllib.parse.urlencode() function as shown in http://www.py4e.com/code3/geojson.py
# 
# Make sure to check that your code is using the API endpoint as shown above. You will get different results from the geojson and json 
# endpoints so make sure you are using the same end point as this autograder is using.
# 
# Test Data / Sample Execution
# ----------------------------
#
# You can test to see if your program is working with a location of "South Federal University" which will have a place_id of 
# "ChIJNeHD4p-540AR2Q0_ZjwmKJ8".
# 
#   $ python3 solution.py
#   Enter location: South Federal University
#   Retrieving http://...
#   Retrieved 6052 characters
#   Place id ChIJNeHD4p-540AR2Q0_ZjwmKJ8
#
# Turn In
# -------
# 
# Please run your program to find the place_id for this location:
# 
#   University of Evora
#
# Make sure to enter the name and case exactly as above and enter the place_id and your Python code below. Hint: The first seven characters 
# of the place_id are "ChIJrdL ..."
# Make sure to retreive the data from the URL specified above and not the normal Google API. Your program should work with the Google API - 
# but the place_id may not match for this assignment.

import urllib.request, urllib.parse, urllib.error
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_key = 42
api_endpoint = 'http://py4e-data.dr-chuck.net/json?'

location = input('Enter location: ')

params = dict()
params['key'] = api_key
params['address'] = location
url = api_endpoint + urllib.parse.urlencode(params)

print('Retrieving ', url)
raw_json = urllib.request.urlopen(url, context=ctx).read()
decoded_json = raw_json.decode()
print('Retrieved',len(decoded_json), 'characters')

try:
    json_object = json.loads(decoded_json)
except:
    json_object = None

if not json_object or 'status' not in json_object or json_object['status'] != 'OK':
    print('(!) Error in retrieving data')
    print(decoded_json)
else:
    place_id = json_object['results'][0]['place_id']
    print('Place ID:', place_id)