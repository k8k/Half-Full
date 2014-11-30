import requests

class Geocoder(object):
	"""Convert user-inputed location to lat long"""
	def __init__(self, user_location):
		super(Geocoder, self).__init__()
		self.user_location = user_location

	def fetch(self):
		r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?sensor=false&key=AIzaSyDjesZT-7Vc5qErTJjS2tDIvxLQdYBxOEY&address="+self.user_location)
		user_latitude = r.json()['results'][0]['geometry']['location']['lat']
		user_longitude = r.json()['results'][0]['geometry']['location']['lng']
		user_longitude = str(user_longitude)
		user_latitude = str(user_latitude)

		location = user_latitude + ',' + user_longitude
		return location

