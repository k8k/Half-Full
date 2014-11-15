import os
from foursquare_engine import update_db_from_twilio
from twilio.rest import TwilioRestClient
import twilio.twiml
from flask import request, session

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')


HELP_MESSAGE    ="We didn't get that! please respond with 'venue name: the city its in: SLAMMED / HALF FULL.\n(ex) 'Blue Bottle: San Francisco, CA: SLAMMED'. "
ALTERNATE_INTRO = """If you meant one of the places below instead, just reply to this text with the corresponding number."""


BODY            = request.values.get('Body')
response        = twilio.twiml.Response()

def new_user_report():
	try:
            body        = BODY.split(": ")
            venue_name  = body[0].lower()
            city        = body[1].lower()
            busy_status = body[2].lower()
        
        # Error handler in case user does not send message in correct format of
        # "venue: city (state code optional): busy status (slammed / half full)"  
	except IndexError:
		with response.message() as message:
			message.body = "{0}".format(HELP_MESSAGE)
			session.clear()
        return str(response)


        # calling function from foursquare_engine that will query the foursquare
    # API using the parameters defined in the user's incoming test message
	venues = update_db_from_twilio(venue_name, city, busy_status)
   
    # TEST to make sure venues are coming out correctly
	print venues
    # UNICODE BUG THAT NEEDS TO BE FIXED LIVES HERE # 


    # List pulled from venues JSON object with Venue Name, Venue Address, 
    # Foursquare ID number. Only pull the first 4 items from the venues list.
    # Item 0 will be the assumed correct venue, unless user corrects.

	ALTERNATE_OPTIONS = []        
	for i in range(len(venues)):
		ALTERNATE_OPTIONS.append(((venues[i]['name']).encode(), venues[i]['location']['formattedAddress'][0], venues[i]['id']))
		if i == 3:
			break


	ALTERNATE_OPTIONS = list(enumerate(ALTERNATE_OPTIONS))

    # Store this list to the session so if user texts back we can access
    # the information and update the database as needed

	session['ALTERNATE_OPTIONS'] = ALTERNATE_OPTIONS

    # String that is used in response to user
	ALTERNATE_STRING = ''
	for i in range(1, len(ALTERNATE_OPTIONS)):
		ALTERNATE_STRING = ALTERNATE_STRING + str(ALTERNATE_OPTIONS[i][0]) + ": " + ALTERNATE_OPTIONS[i][1][0] + ", " + ALTERNATE_OPTIONS[i][1][1] + "\n"

    # Setting up variables to be used in Response Message. primary_venue_name
    # is the first response from the foursquare API and is the assumed correct
    # match for the search, unless user indicates otherwise.
	primary_venue_name      = (venues[0]['name']).encode()
	primary_venue_address   = (venues[0]['location']['formattedAddress'][0]).encode()
   
	slammed_confirmation_message    = """Thanks for letting us know that %s at %s is THE WORST. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
	safe_confirmation_message       = """Thanks for letting us know that %s at %s is a Safe Zone. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)


    # Check to see if more than one venue in response. There will be no
    # alternates offered if query only results in one response.
	if len(venues) > 1:
		if 'slammed' in busy_status:
			with response.message() as message:
				message.body = "{0}\n{1}\n{2}".format(slammed_confirmation_message,
                                                ALTERNATE_INTRO, ALTERNATE_STRING)

        elif 'half' in busy_status:
            with response.message() as message:
                message.body = "{0}\n{1}\n{2}".format(safe_confirmation_message,
                                                ALTERNATE_INTRO, ALTERNATE_STRING)

    # For queries that result in a single response. No alternates provided.
	elif len(venues) == 1:
		if 'slammed' in busy_status:
			with response.message() as message:
				message.body = "{0}".format(slammed_confirmation_message)

			session.clear()
                                            
        elif 'half' in busy_status:
            with response.message() as message:
                message.body = "{0}".format(safe_confirmation_message)

            session.clear()


	else:
		with response.message() as message:
			message.body = "{0}".format(HELP_MESSAGE)

        session.clear()
           

	return unicode(response).encode("utf-8")

def corrected_report():
	
	ALTERNATE_OPTIONS = session.get('ALTERNATE_OPTIONS', 0)
        
	alternate_enumerated_options = ['1','2','3']

	if BODY in alternate_enumerated_options:
	    body = int(BODY)

	    response_list = []
	    for i in ALTERNATE_OPTIONS:
	        response_list.append(i[1])


	    updated_response_message = """Got it, you meant %s.""" % response_list[body][0]

	    with response.message() as message:
	                message.body = "{0}".format(updated_response_message)
	    session.clear()
	
	else:
	    try:
	        body = int(body)
	        with response.message as message:
	            message.body = "Sorry! %r is not a valid option." % body
	    except ValueError:
	        new_user_report()
	        session.clear()
	    


	return unicode(response).encode("utf-8")









 # setting up session counter to allow for tracking conversations
    # counter = session.get('counter', 0)
    # counter += 1
    # session['counter'] = counter

    # # Test to make sure counter is behaving as expected
    # print counter

    # # Global Variables used in response messages

    # HELP_MESSAGE    ="We didn't get that! please respond with 'venue name: the city its in: SLAMMED / HALF FULL.\n(ex) 'Blue Bottle: San Francisco, CA: SLAMMED'. "
    # ALTERNATE_INTRO = """If you meant one of the places below instead, just reply to this text with the corresponding number."""

    
    # # Getting information from incoming text and builing Response object for later

    # body            = request.values.get('Body')
    # response        = twilio.twiml.Response()

    # # Check to see if this is the first message in the conversation. If so, assume
    # # it is a tip about a venue.

    # if counter == 1:
    #     # Split message body on colons to parse out informatio to add to the
    #     # Hot Tip Database

    #     try:
    #         body        = body.split(": ")
    #         venue_name  = body[0].lower()
    #         city        = body[1].lower()
    #         busy_status = body[2].lower()
        
    #     # Error handler in case user does not send message in correct format of
    #     # "venue: city (state code optional): busy status (slammed / half full)"  
    #     except IndexError:
    #         with response.message() as message:
    #             message.body = "{0}".format(HELP_MESSAGE)
    #             session.clear()
    #         return str(response)


    #     # calling function from foursquare_engine that will query the foursquare
    #     # API using the parameters defined in the user's incoming test message
    #     venues = update_db_from_twilio(venue_name, city, busy_status)
       
    #     # TEST to make sure venues are coming out correctly
    #     print venues
    #     # UNICODE BUG THAT NEEDS TO BE FIXED LIVES HERE # 


    #     # List pulled from venues JSON object with Venue Name, Venue Address, 
    #     # Foursquare ID number. Only pull the first 4 items from the venues list.
    #     # Item 0 will be the assumed correct venue, unless user corrects.

    #     ALTERNATE_OPTIONS = []        
    #     for i in range(len(venues)):
    #         ALTERNATE_OPTIONS.append(((venues[i]['name']).encode(), venues[i]['location']['formattedAddress'][0], venues[i]['id']))
    #         if i == 3:
    #             break

    #     ALTERNATE_OPTIONS = list(enumerate(ALTERNATE_OPTIONS))

    #     # Store this list to the session so if user texts back we can access
    #     # the information and update the database as needed

    #     session['ALTERNATE_OPTIONS'] = ALTERNATE_OPTIONS

    #     # String that is used in response to user
    #     ALTERNATE_STRING = ''
    #     for i in range(1, len(ALTERNATE_OPTIONS)):
    #         ALTERNATE_STRING = ALTERNATE_STRING + str(ALTERNATE_OPTIONS[i][0]) + ": " + ALTERNATE_OPTIONS[i][1][0] + ", " + ALTERNATE_OPTIONS[i][1][1] + "\n"

    #     # Setting up variables to be used in Response Message. primary_venue_name
    #     # is the first response from the foursquare API and is the assumed correct
    #     # match for the search, unless user indicates otherwise.
    #     primary_venue_name      = (venues[0]['name']).encode()
    #     primary_venue_address   = (venues[0]['location']['formattedAddress'][0]).encode()
       
    #     slammed_confirmation_message    = """Thanks for letting us know that %s at %s is THE WORST. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
    #     safe_confirmation_message       = """Thanks for letting us know that %s at %s is a Safe Zone. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)


    #     # Check to see if more than one venue in response. There will be no
    #     # alternates offered if query only results in one response.
    #     if len(venues) > 1:
    #         if 'slammed' in busy_status:
    #             with response.message() as message:
    #                 message.body = "{0}\n{1}\n{2}".format(slammed_confirmation_message,
    #                                                 ALTERNATE_INTRO, ALTERNATE_STRING)

    #         elif 'half' in busy_status:
    #             with response.message() as message:
    #                 message.body = "{0}\n{1}\n{2}".format(safe_confirmation_message,
    #                                                 ALTERNATE_INTRO, ALTERNATE_STRING)

    #     # For queries that result in a single response. No alternates provided.
    #     elif len(venues) == 1:
    #         if 'slammed' in busy_status:
    #             with response.message() as message:
    #                 message.body = "{0}".format(slammed_confirmation_message)

    #             session.clear()
                                                
    #         elif 'half' in busy_status:
    #             with response.message() as message:
    #                 message.body = "{0}".format(safe_confirmation_message)

    #             session.clear()


    #     else:
    #         with response.message() as message:
    #             message.body = "{0}".format(HELP_MESSAGE)

    #         session.clear()
            


    #     return unicode(response).encode("utf-8")

    # # If primary venue is not correct, user can reply to the text with 1 - 5,
    # # and those numbers correspond with the 5 
    # elif counter == 2:

    #     ALTERNATE_OPTIONS = session.get('ALTERNATE_OPTIONS', 0)
        
    #     alternate_enumerated_options = ['1','2','3']

    #     if body in alternate_enumerated_options:
    #         body = int(body)

    #         response_list = []
    #         for i in ALTERNATE_OPTIONS:
    #             response_list.append(i[1])


    #         updated_response_message 	= """Got it, you meant %s at %s.""" % (
    #         							response_list[body][0], response_list[body][1])

    #         with response.message() as message:
    #                     message.body = "{0}".format(updated_response_message)


    #         session.clear()

    #     else:
    #         try:
    #             body = int(body)
    #             with response.message as message:
    #                 message.body = "Sorry! %r is not a valid option." % body
    #         except ValueError:
    #             pass



    #     return unicode(response).encode("utf-8")


    # else:
    #     print counter
    #     # counter = 0
    #     session.clear()
    #     print "NEW %r" % counter
    #     return "WTF %r" % counter















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
