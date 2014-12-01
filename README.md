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
<p>
<br>
<br>
If the user would rather search for a specific venue, they can do so from the top navigation bar.
<img src="/static/img/SpecificVenueSearch.gif" alt="Specific Venue Search">
</p>

The results page when searching for a specific venue looks very similar to the general results page - the one small difference being that since the user doesn't provide an exact location for the specific search (just a city), the address and city are displayed where the distance away (measured in steps) is displayed on the general results page.
<br>
<img src="/static/img/ComparisonResult.png" width="50%">
<br>
</p>
<p>
From the results page, the user can click through for more information, as well as to see Instagram pictures that have been recently taken at the location. 
<br>
<img src="/static/img/SpecificVenue.gif" alt="Specific Venue Information">
<br>

In order to get the Instagram pictures, Half Full uses the Foursquare ID of the venue and maps it to the Instagram ID, then queries the instagram API for recent media from that venue.
</p>
<br>

```
class InstagramSearch(object):
        """Query Instagram API for recent media"""
        def __init__(self):
                super(InstagramSearch, self).__init__()
                self.access_token       = c.INSTAGRAM_CONFIG['access_token']
                

        def recent_media_search(self,foursquare_id):
                api = instagram_client.InstagramAPI(access_token=self.access_token)
                
                # Getting Instagram ID objects from Foursquare ID
                instagram_id_info = api.location_search(foursquare_v2_id=foursquare_id)
                instagram_id = int(instagram_id_info[0].id)
                
                # Searching for all media tagged at location, based on Instagram ID
                media_search = api.location_recent_media(location_id=int(instagram_id))
                
                # Stripping unnecessary info out of media_search list       
                media_search = media_search[0]

                print dir(media_search[0])
                print media_search[0].location

                return media_search
```
