import foursquare
import os


FOURSQUARE_CLIENT_ID=os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET=os.environ.get('FOURSQUARE_CLIENT_SECRET')
# Construct the client object
client = foursquare.Foursquare(client_id=FOURSQUARE_CLIENT_ID, client_secret=FOURSQUARE_CLIENT_SECRET)

class SearchForVenue(object):
	"""docstring for SearchForVenue"""
	def __init__(self, venuename,venuecity):
		super(SearchForVenue, self).__init__()
		self.venuename = venuename
		self.venuecity = venuecity
		
	def fetch(self):
		likely_places = client.venues.search(params={'query': self.venuename,
                                                    'near': self.venuecity,
                                                    'verified': True,
                                                    'intent': 'checkin',
                                                    })
		likely_venues = likely_places['venues']
		for i in likely_venues:
			i['location']['distance'] = 0
			i['user_rating'] = -1

		return likely_venues
