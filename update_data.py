from predictive_db_model import Status, Venue, Checkin, Session as SQLsession, connect
from baseline_foursquare_data import QueryFoursquare
from datetime import datetime


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







