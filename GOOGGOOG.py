import requests
import json
import os
# from flask import request

def user_venue_search():
		# Sent the Places API key for your application
	print 'wtf'
	AUTH_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

		# Define the location coordinates
	LOCATION = 


	# request.args.get("user_location")
	print LOCATION

		# Define the radius (in meters) for the search
	RADIUS = 1000
	print RADIUS

# Compose a URL to query a predefined location with a radius of 5000 meters
	url = 'https://maps.googleapis.com/maps/api/place/search/json'
	print url
# Send the GET request to the Place details service (using url from above)
	response = requests.get(url,
				params={'location': LOCATION,
						'radius': RADIUS,
						'key': AUTH_KEY,
				})

	print response.json()


	# Get the response and use the JSON library to decode the JSON
	# json_raw = response.read()
	# json_data = json.loads(json_raw)

		# Iterate through the results and print them to the console

	# venue_list = []
	# if json_data["status"] == "OK":
	# 	for place in json_data["results"]:
	# 		venue_list.append(place['name'])

	# return (venue_list)

print user_venue_search()