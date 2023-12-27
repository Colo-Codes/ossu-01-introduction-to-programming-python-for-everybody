# Extracting Data from JSON
# =========================
# Source: https://www.py4e.com/tools/python-data/?PHPSESSID=cbf35c7055aa4465de0a838c7bfb4b9c
#
# # Assignment: Extracting Data from JSON
# ---------------------------------------
# In this assignment you will write a Python program somewhat similar to http://www.py4e.com/code3/json2.py. The program will prompt for a URL, 
# read the JSON data from that URL using urllib and then parse and extract the comment counts from the JSON data, compute the sum of the numbers 
# in the file and enter the sum below:
# We provide two files for this assignment. One is a sample file where we give you the sum for your testing and the other is the actual data you 
# need to process for the assignment.
# 
# Sample data: http://py4e-data.dr-chuck.net/comments_42.json (Sum=2553)
# Actual data: http://py4e-data.dr-chuck.net/comments_1931794.json (Sum ends with 30)
# You do not need to save these files to your folder since your program will read the data directly from the URL. Note: Each student will have a 
# distinct data url for the assignment - so only use your own data url for analysis.
#
# Data Format
# -----------
# The data consists of a number of names and comment counts in JSON as follows:
# 
#   {
#     comments: [
#       {
#         name: "Matthias"
#         count: 97
#       },
#       {
#         name: "Geomer"
#         count: 97
#       }
#       ...
#     ]
#   }
# The closest sample code that shows how to parse JSON and extract a list is json2.py. You might also want to look at geoxml.py to see how to 
# prompt for a URL and retrieve data from a URL.
# 
# Sample Execution
# ----------------
#
#   $ python3 solution.py
#   Enter location: http://py4e-data.dr-chuck.net/comments_42.json
#   Retrieving http://py4e-data.dr-chuck.net/comments_42.json
#   Retrieved 2733 characters
#   Count: 50
#   Sum: 2...

import urllib.request, urllib.parse, urllib.error
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter location: ')

print('Retrieving', url)
raw_json = urllib.request.urlopen(url, context=ctx).read()
decoded_json = raw_json.decode()
print('Retrieved',len(decoded_json), 'characters')

try:
    json_object = json.loads(decoded_json)
except:
    json_object = None

if not json_object:
    print('(!) Error in retrieving data')
    print(decoded_json)
else:
    sum = 0
    for comment in json_object['comments']:
        sum += comment['count']
    print('Count:', len(json_object['comments']))
    print('Sum:', sum)

