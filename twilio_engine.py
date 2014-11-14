import os
from foursquare_engine import update_db_from_twilio
from twilio.rest import TwilioRestClient
from flask import Flask, request
import twilio.twiml

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# # create an authenticated client that can make requests to Twilio for your
# # account.
# app = Flask(__name__)
# app.config.update(
#     DEBUG=True,
#     SECRET_KEY='katestwiliothing',
#     SERVER_NAME='localhost:80',
# )

# @app.route("/twilio", methods=['GET', 'POST'])
# def half_full_report():
# 	# from_number = request.values.get('From')

# 	body = request.values.get('Body')
# 	r
# 	body = body.split(":")
# 	venue_name = body[0].lower()
# 	city = body[1].lower()
# 	busy_status = body[2].lower()

# 	venues = update_db_from_twilio(venue_name, city, busy_status)

# 	try:
# 		if "half full" in busy_status:

# 			message = 	"""Thanks for letting  us know that %r at %r is a Safe Zone. 
# 			If you meant one of the below locations instead, simply reply to this
# 			text with the corresponding number.\n
# 			1: %r, %r: \n2: %r, %r: \n3: %r, %r: \n4: %r, %r:\n""" % (venues[0]['name'], 
# 				venues[0]['location']['formattedAddress'],
# 				venues[1]['name'], venues[1]['location']['formattedAddress'],
# 				venues[2]['name'], venues[2]['location']['formattedAddress'],
# 				venues[3]['name'], venues[3]['location']['formattedAddress'])
# 		elif "slammed" in busy_status:

# 			message = 	"""Thanks for letting  us know that %r at %r is THE WORST. 
# 			If you meant one of the below locations instead, simply reply to this
# 			text with the corresponding number.\n
# 			1: %r, %r: \n2: %r, %r: \n3: %r, %r: \n4: %r, %r:\n""" % (venues[0]['name'], 
# 				venues[0]['location']['formattedAddress'],
# 				venues[1]['name'], venues[1]['location']['formattedAddress'],
# 				venues[2]['name'], venues[2]['location']['formattedAddress'],
# 				venues[3]['name'], venues[3]['location']['formattedAddress'])
# 		else:

# 			message = """we didn't get that! you said %s in %s was %s, please
# 						respond with 'venue name: the city its in: and either SLAMMED
# 						or HALF FULL.' (ex) 'Blue Bottle: San Francisco, CA: SLAMMED' 
# 						""" % (venue_name, city, busy_status)
	
# 	except TypeError:
# 		message = "no message received"
	

# 	resp=twilio.twiml.Response()

# 	resp.message(message)
# 	return str(resp)




# if __name__ == '__main__':
#     app.run(debug=True)
