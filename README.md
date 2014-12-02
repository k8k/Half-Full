Half Full
=========
#### Built by [Kate Kuchin](https://www.linkedin.com/in/katekuchin)
Half Full is a web app for introverts, misanthropes, and people who people who might actually want a bit of elbow room at a bar. While there are many apps to help you find people, there are very few to help you avoid them: Half Full does just that.

#### The Inspiration for Half Full
One of my biggest pain points is wanting to leave my house, but not wanting to have to be around people to do so. I have long joked that there needed to be an app to help you actively avoid people, so when it came time to build my Hackbright Final Project, Half Full was the obvious choice.


####Table of Contents
- [Building Half Full](#building-half-full)
- [The Stack](#the-stack)
- [How Half Full Works](#how-half-full-works)
  - [Searching Nearby](#searching-nearby)
  - [Querying the Foursquare API](#querying-the-foursquare-api)
  - [Querying Instagram and Foursquare's APIs](#querying-instagram-and-foursquares-apis)
  - [User Reports](#user-reports)
    - [Reporting in the UI](#reporting-in-the-UI)
    - [Reporting via Twilio](#reporting-via-twilio)
    - [Weighting reports](#weighting-reports)
- [Cloning Half Full](#cloning-half-full)

#### Building Half Full
Half Full was built in 4 weeks. Roughly, the breakdown of the project, week-by-week was:
-  <b>Week 1</b>
  -  Exploring APIs (Foursquare, Instagram, and Google Maps)
  -  Scoping the Project
  -  Wireframing
  -  Writing test queries and other test code
-  <b>Week 2</b>
  -  Building Homepage and incorporating Google Maps API into search functionality
  -  Creating queries for Foursquare and Instagram APIs
  -  Creating user reporting mechanism using the Twilio API
-  <b>Week 3</b>  
  -  Building a SQL Database in which to store user reports
  -  Building functionality to enable the user report Database to interface with the Foursquare API
  -  Beginning to work on the User Interface
-  <b>Week 4</b>
  -  Working on User Interface, incorporating Sass and Bourbon
  -  Adding UI reporting mechanism to supplement Twilio reporting mechanism
  -  Refactoring codebase to make code cleaner and more maintainable

#### The Stack
 -  HTML5
 -  CSS3
 -  Sass
 -  Bourbon
 -  JavaScript
 -  JQuery
 -  Python
 -  Flask
 -  Foursquare Venues API
 -  Instagram API: Media and Venues
 -  Google Maps API: Typeahead and Geocoding
 -  Twilio API (with sessions and conversation tracking)

#### How Half Full Works
Half Full relies on data from the Foursquare and Instagram APIs, as well as data from Half Full user reports. It reconciles these different data types to provide the user with an indication if a venue is "Half Full" or "Slammed." If the data is inconclusive, users are warned to proceed with caution.

#### Seaching Nearby
When a user first navigates to Half Full, they input their location (or any location), and using Google Maps Typeahead API, Half Full autocompletes the address.

<img src="/static/img/GoogleMapsTypeahead.gif" alt="HomepageTypeahead">

<br>

Using the Google Maps API, Half Full then geocodes the input location. This geocoded location is a JSON object and must be manipulated into a format the Foursquare API can recognize (a comma-delimited string).

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
#### Querying The Foursquare API
Half Full then uses the lat-long location string to query the Foursquare API. At this stage, the category of venue (bar, restaurant, or cafe) is translated into a Foursquare category ID, which is also used in the API query. The resulting page lists venues that match the user's criteria, along with information about each venue and an indication of how busy the venue is expected to be.
<img src="/static/img/ResultsPage.gif" alt="ResultsPage">

####Querying Instagram and Foursquare's APIs
From the results page, the user can click through for more information and recent Instagram photos, which is queried from a different endpoint on the Foursquare API as well as from the Instagram API.
<img src="/static/img/SpecificVenue.gif" alt="Specific Venue Information">

In order to get the Instagram pictures, Half Full uses the Foursquare ID of the venue and maps it to the Instagram ID, then queries the instagram API for recent media from that venue.


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
