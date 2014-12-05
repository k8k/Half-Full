import foursquare
import os
from user_report_model import Status, Session as SQLsession, connect
import constants as c
from datetime import datetime


class SearchForVenue(object):
	"""Querying the Foursquare API for venues by lat long or by city and venue"""
	def __init__(self):
		super(SearchForVenue, self).__init__()
		self.client 	= foursquare.Foursquare(client_id=c.FOURSQUARE_CLIENT_ID, client_secret=c.FOURSQUARE_CLIENT_SECRET)

		
	def search_by_name_city(self, venuename, venuecity):
		likely_venues = self.likely_venues(venuename, venuecity)
		for i in likely_venues:
			i['location']['distance'] = 0
			i['user_rating'] = -1

		return likely_venues

	def specific_venue_status(self, venue, city):
		foursquare_venues_by_latlong = self.search_by_name_city(venue,city)

		#Dict comprehension of Foursquare IDs to check for matching entries in Database
		foursq_ids_in_results = {i['id'] : i for i in foursquare_venues_by_latlong}
		
		
		#Connect to database & check for venues that are in user-reported DB
		sqlsession = connect()
		query = sqlsession.query(Status).filter(Status.foursquare_id.in_(foursq_ids_in_results.keys()))
		status_query = query.all()

		ids_statuses 	= {i.foursquare_id : i.status for i in status_query}
		expiration_info	= {i.foursquare_id : i.expiration_status for i in status_query}
		report_time		= {i.foursquare_id : i.time for i in status_query}
		delta_time		= {i.foursquare_id : int(((datetime.utcnow() - i.time).total_seconds())/3600) for i in status_query}

		# Adding information from user database into foursquare venue object
		for four_id in foursq_ids_in_results.keys():
			if four_id in ids_statuses.keys():
				foursq_ids_in_results[four_id]['user_rating'] = ids_statuses[four_id]
				foursq_ids_in_results[four_id]['expiration']  = expiration_info[four_id]
				foursq_ids_in_results[four_id]['report_time'] = report_time[four_id]
				foursq_ids_in_results[four_id]['delta_time']  = delta_time[four_id]               
			else:
				foursq_ids_in_results[four_id]['user_rating'] 	= -1
				foursq_ids_in_results[four_id]['expiration'] 	= "No Report"
				foursq_ids_in_results[four_id]['report_time'] 	= "No Report"
				foursq_ids_in_results[four_id]['delta_time'] 	= "No Report"

		return foursq_ids_in_results.values()

	def likely_venues(self, venuename, venuecity):
		likely_places = self.client.venues.search(params={'query': venuename,
													'near': venuecity,
													'verified': True,
													'intent': 'checkin',
													})
		likely_venues = likely_places['venues']

		return likely_venues

	def test_user_input(self, venuecity):
		test_search = self.likely_venues('test', venuecity)
		return test_search


	def venues_with_user_status(self, location, venue_type):
		foursquare_venues_by_latlong = self.foursquare_search_by_category(location, venue_type)

		#Dict comprehension of Foursquare IDs to check for matching entries in Database
		foursq_ids_in_results = {i['id'] : i for i in foursquare_venues_by_latlong}
		
		
		#Connect to database & check for venues that are in user-reported DB
		sqlsession = connect()
		query = sqlsession.query(Status).filter(Status.foursquare_id.in_(foursq_ids_in_results.keys()))
		status_query = query.all()

		ids_statuses 	= {i.foursquare_id : i.status for i in status_query}
		expiration_info	= {i.foursquare_id : i.expiration_status for i in status_query}
		report_time		= {i.foursquare_id : i.time for i in status_query}
		delta_time		= {i.foursquare_id : int(((datetime.utcnow() - i.time).total_seconds())/3600) for i in status_query}


		# Adding information from user database into foursquare venue object
		for four_id in foursq_ids_in_results.keys():
			if four_id in ids_statuses.keys():
				foursq_ids_in_results[four_id]['user_rating'] = ids_statuses[four_id]
				foursq_ids_in_results[four_id]['expiration']  = expiration_info[four_id]
				foursq_ids_in_results[four_id]['report_time'] = report_time[four_id]
				foursq_ids_in_results[four_id]['delta_time']  = delta_time[four_id]               
			else:
				foursq_ids_in_results[four_id]['user_rating'] 	= -1
				foursq_ids_in_results[four_id]['expiration'] 	= "No Report"
				foursq_ids_in_results[four_id]['report_time'] 	= "No Report"
				foursq_ids_in_results[four_id]['delta_time'] 	= "No Report"

		return foursq_ids_in_results.values()


	def foursquare_search_by_category(self, latlng, category):

	# Create a list of venue categories to exclude from results (stripclubs)

		blacklist = ['4bf58dd8d48988d1d6941735']

	# Create a dictionary that will be used to search 4sq DB of venues

		results_dictionary =	{'ll': latlng,
								'verified' : True,
								'intent': 'checkin', 
								'radius': '1000',
								'limit': '15'}
		
		# Check to see if there is a specified category - if so add to search
		# dictionary

		if category != False:
			results_dictionary['categoryId'] = category  

		places_by_category = self.client.venues.search(params=results_dictionary)

		# Drilling down to "venues" within the 4q objects that are returned
		# to remove excess information and simplify later code

		venues = places_by_category['venues']
		return venues
		# Creating a list of venues that meet the specified search criteria

		categorized_list_of_venues = []
		for i in range(len(venues)):
			for j in range(len(venues[i]['categories'])):
				if venues[i]['categories'][j]['id'] not in blacklist:
					categorized_list_of_venues.append(venues[i])
	   
		return categorized_list_of_venues


	def query_for_averages_db(self, latlng, category):
		
		params_dictionary =		{'ll': latlng,
								'verified' : True,
								'intent': 'checkin', 
								'radius': '5000',
								'limit': '100',
								'categoryId': category}

		venues = self.client.venues.search(params=params_dictionary)
		venues = venues['venues']
		return venues













