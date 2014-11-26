class VenueType(object):
	"""docstring for VenueType"""
	def __init__(self):
		super(VenueType, self).__init__()
		self.venues = {'restaurant': '4d4b7105d754a06374d81259',
						'bar': '4d4b7105d754a06376d81259',
						'cafe': '4bf58dd8d48988d1e0931735',
						}
	def get(self, typevenue):
		return self.venues.get(typevenue)

