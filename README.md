Half Full
=========
<h5>Half Full is a web app for introverts, misanthropes, and people who people who might actually want a bit of elbow room at a bar.</h5>
<p>
While there are many apps to help you find people, there are very few to help you avoid them: Half Full does just that.</p>
<p>
Frustrated by feeling like she was always waiting for a table, ending up at bars that were too crowded and too loud, and just generally having to be around too many people, <a href="https://www.linkedin.com/in/katekuchin">Kate</a> decided to build Half Full for her Hackbright final project to address this problem. 
</p>
<p>
When a user first navigates to Half Full, they input their location (or the location where they are hoping to go out around), and using Google Maps Typeahead API, Half Full autocompletes the address or location they enter.
<br>
<img src="/static/img/GoogleMapsTypeahead.gif" alt="Typeahead">
</p>
<br>
```
class Geocoder(object):
	"""Convert user-inputed location to lat long"""
	def __init__(self, user_location):
		super(Geocoder, self).__init__()
		self.user_location = user_location

	def fetch(self):
		r = requests.get("""https://maps.googleapis.com/maps/api/geocode/json?sensor=false
		&key=AIzaSyDjesZT-7Vc5qErTJjS2tDIvxLQdYBxOEY&address="""+self.user_location)
		user_latitude = r.json()['results'][0]['geometry']['location']['lat']
		user_longitude = r.json()['results'][0]['geometry']['location']['lng']
		user_longitude = str(user_longitude)
		user_latitude = str(user_latitude)

		location = user_latitude + ',' + user_longitude
		return location

```
<p>Using the Google Maps API, Half Full then geocodes the input location, and manipulates that data into the format the Foursquare API requires to query for information about venues (a comma-delimited string).
</p>
<p>
Half Full then uses the location string to query the Foursquare API, along with the category of venue the user selected. The resulting page lists venues that match the user's criteria, along with information about each venue and an indication of how full or empty the venue is expected to be.
<img src="/static/img/ResultsPage.gif" alt="ResultsPage" style="width:80%;">
</p>
