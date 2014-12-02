from user_report_model import Status, Session as SQLsession, connect
from datetime import datetime

class UpdateDatabase(object):
	"""docstring for UpdateDatabase"""
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
	