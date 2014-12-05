import constants as c
import foursquare
import os
import constants as c
from datetime import datetime
import numpy as np
import itertools
from specificsearch import SearchForVenue
from venue import VenueType


class QueryFoursquare(object):
	"""docstring for QueryFoursquare"""
	def __init__(self):
		super(QueryFoursquare, self).__init__()
		

	def lat_long_bounds(self, latmin, latmax, longmin, longmax):
		seed_lats	= np.arange(latmin,latmax,0.01).tolist()
		latitudes 	= []
		for i in seed_lats:
			latitudes.append("{0:.2f}".format(i))

		seed_longs	= np.arange(longmin,longmax,0.01).tolist()
		longitudes 	= []
		for i in seed_longs:
			longitudes.append("{0:.2f}".format(i))

		lat_longs = []
		for i in latitudes:
			for j in longitudes:
				lat_longs.append((i,j))

		string_latlongs = []
		for i in lat_longs:
			string_latlongs.append(','.join(i))

		return string_latlongs

	def foursquare_query_sf(self):
		sf_coordinates = self.lat_long_bounds(37.73, 37.8, -122.54,-122.38)
		print sf_coordinates
		venues = []
		for i in sf_coordinates:
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['bar'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['restaurant'].value))
			venues.append(SearchForVenue().query_for_averages_db(i, VenueType['coffee'].value))


		print len(venues)
		return venues

QueryFoursquare().foursquare_query_sf()

sf_coordinates = QueryFoursquare().lat_long_bounds(37.73, 37.8, -122.54,-122.38)
print len(sf_coordinates)
