import constants as c
import foursquare
import os
from predictive_db_model import Status, Venue, Checkin, Session as SQLsession, connect

from datetime import datetime
import numpy as np
from specificsearch import SearchForVenue
from venue import VenueType


class UpdateDatabase(object):
	"""Updates the database to reflect user reports.

	Is called by both the Twilio reporting mechanism as well as the UI."""
	def __init__(self):
		super(UpdateDatabase, self).__init__()

	def add_new_rating(self, venue_name, foursquare_id, status_code):
		self.sqlsession 			= connect()
		self.s 						= Status()
		self.s.venue_name 			= venue_name
		self.s.foursquare_id 		= foursquare_id
		self.s.status 				= status_code
		self.s.time 				= datetime.utcnow()
		self.s.expiration_status 	= 'Fresh'

		self.sqlsession.add(self.s)
		self.sqlsession.commit()
		return self.s.id

	def delete_by_id(self, id):
		self.sqlsession 	= connect()
		self.sqlsession.query(Status).filter_by(id=id).delete()
		self.sqlsession.commit()
	
	
	def add_venue_info(self, venue_name, category, foursquare_id, latitude, longitude):
		self.sqlsession 			= connect()
		self.v 						= Venue()
		self.v.venue_name 			= venue_name
		self.v.category				= category
		self.v.foursquare_id		= foursquare_id
		self.v.latitude 			= latitude
		self.v.longitude			= longitude

		self.sqlsession.add(self.v)
		self.sqlsession.commit()

	def add_new_checkins(self, venue_name, foursquare_id, current_checkins, checkin_time):
		self.sqlsession 			= connect()
		self.c 						= Checkin()
		self.c.venue_name			= venue_name
		self.c.foursquare_id		= foursquare_id
		self.c.current_checkins 	= current_checkins
		self.c.checkin_time			= checkin_time

		self.sqlsession.add(self.c)
		self.sqlsession.commit()

	def commit_to_db(self):
		return self.sqlsession.commit()



class QueryFoursquare(object):
	"""docstring for QueryFoursquare"""
	def __init__(self):
		super(QueryFoursquare, self).__init__()
		

	def lat_long_bounds(self, latmin, latmax, longmin, longmax):
		seed_lats	= np.arange(latmin,latmax,0.01).tolist()
		latitudes 	= []
		for i in seed_lats:
			latitudes.append("{0:.3f}".format(i))

		seed_longs	= np.arange(longmin,longmax,0.01).tolist()
		longitudes 	= []
		for i in seed_longs:
			longitudes.append("{0:.3f}".format(i))

		lat_longs = []
		for i in latitudes:
			for j in longitudes:
				lat_longs.append((i,j))

		string_latlongs = []
		for i in lat_longs:
			string_latlongs.append(','.join(i))

		return string_latlongs

	def foursquare_query_sf(self):
		sf_coordinates = self.lat_long_bounds(37.71, 37.82, -122.54,-122.38)
		print len(sf_coordinates)
		return sf_coordinates
		venues = []
		for i in sf_coordinates:
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['bar'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['restaurant'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['coffee'].value))
		

		list_venues = []
		for i in venues:
			list_venues = list_venues + i
		return list_venues


	def test_query(self):
		coordinates = self.lat_long_bounds(37.75, 37.76, -122.5,-122.49)
		print coordinates
		venues = []
		for i in coordinates:
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['bar'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['restaurant'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['coffee'].value))
		

		list_venues = venues[0]+venues[1]+venues[2]
		return list_venues

	def update_venue_info(self):
		venues = self.foursquare_query_sf()
		self.sqlsession 	= connect()

		for i in venues:
			name 			= i['name']
			category 		= i['categories'][0]['shortName']
			foursquare_id	= i['id']
			latitude		= i['location']['lat']
			longitude 		= i['location']['lng']
			
			UpdateDatabase().add_venue_info(name, category, foursquare_id, latitude, longitude)
			self.sqlsession.add(self.c)

		self.sqlsession.commit()

	def update_checkin_info(self):
		venues 						= self.foursquare_query_sf()
		self.sqlsession 			= connect()

		for i in venues:
			venue_name 					= i['name']
			foursquare_id				= i['id']
			current_checkins			= i['hereNow']['count']
			checkin_time				= datetime.utcnow()

			self.c 						= Checkin()
			self.c.venue_name			= venue_name
			self.c.foursquare_id		= foursquare_id
			self.c.current_checkins 	= current_checkins
			self.c.checkin_time			= checkin_time
			self.sqlsession.add(self.c)
		
		self.sqlsession.commit()
			


# QueryFoursquare().update_venue_info()
QueryFoursquare().foursquare_query_sf()
# UpdateDatabase().commit_to_db()






