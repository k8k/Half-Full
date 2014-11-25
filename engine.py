from flask import Flask, render_template, request, session
import os
from instagram import client
import requests
from foursquare_engine import foursquare_search_by_category, update_db_from_twilio, venue_hours
import instagram_engine
import twilio.twiml
from twilio.rest import TwilioRestClient
from user_report_model import Status, Session as SQLsession, connect
from datetime import datetime
from user_reports_engine import expire_statuses


# from jinja2 import Environment, Undefined

# def custom_in_list(item, list_to_check):
#     if item in list_to_check:
#         return True
#     else:
#         return False

# env = Environment()
# env.filters['custom_in_list'] = custom_in_list
# from twilio_engine import new_user_report, corrected_report




app = Flask(__name__)
app.secret_key= 'katescoolproject'

#Google Maps API Key for Typeahead & Lat Long
GOOGLE_MAPS_EMBED_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

# Instagram Configuration
CONFIG = {

    'client_id': os.environ.get("INSTAGRAM_CLIENT_ID"),
    'client_secret': os.environ.get("INSTAGRAM_CLIENT_SECRET"),
    'redirect_uri': os.environ.get("INSTAGRAM_REDIRECT_URI")
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

# Twilio Keys, pulled in from system environment
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')



@app.route("/", methods = ['POST', 'GET'])
def half_full_home():
    """Home page. Basic search box with venue category options"""
    
    

    # expire_statuses()

    return render_template("index.html")




@app.route("/search", methods = ['POST'])
def user_lat_long():
    """Take user inputted address and convert to lat-long"""

    # Getting Lat/Long coordinates from Address user is searching for
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?sensor=false&key=AIzaSyDjesZT-7Vc5qErTJjS2tDIvxLQdYBxOEY&address=" +\
    request.form['user_location'])
    user_latitude = r.json()['results'][0]['geometry']['location']['lat']
    user_longitude = r.json()['results'][0]['geometry']['location']['lng']
    user_longitude = str(user_longitude)
    user_latitude = str(user_latitude)

    # Defining User Location as a string, to pass to foursquare engine
    location = user_latitude + ',' + user_longitude
    

    # Set venue_type as false, making it optional
    venue_type = False



    # Checking venue-type. Translation Layer - will transfer to a DB
    # to dynamically update after MVP is complete
    if request.form['venue-type'] == 'restaurant':
        venue_type = '4d4b7105d754a06374d81259'
    elif request.form['venue-type'] == 'bar':
        venue_type = '4d4b7105d754a06376d81259'
    elif request.form['venue-type'] == 'cafe':
        venue_type = '4bf58dd8d48988d1e0931735'

    results_check = foursquare_search_by_category(location, venue_type)

    foursq_ids_in_results = []
    for i in results_check:
        foursq_ids_in_results.append(i['id'])

    open_venues = []
    for i in results_check:
        if venue_hours(i['id']) is not None:
            if venue_hours(i['id'])['isOpen']:
                open_venues.append(i)
    



  
    print "THESE PLACES ARE OPEN %r" % open_venues
    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"


    # Write an if statement that will return only venues that are open


    print "RESULTS %r" % results_check

    sqlsession = connect()

    query = sqlsession.query(Status).filter(Status.foursquare_id.in_(foursq_ids_in_results))
    status_query = query.all()
    

    for i in results_check:
        i['user_rating'] = -1
        for k in status_query:
            if i['id'] == k.foursquare_id:
                i['user_rating'] = k.status
                break
            else:
                i['user_rating'] = -1

            

    print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'


    print "STATUS QUERY %r" % status_query
    # print "*~*~*~*~*~*~**~*~\n\n\n\n\n\n\n\n\n %r" % status_query[0].venue_name

    matching_ids =[]
    for i in status_query:
        matching_ids.append(i.foursquare_id.encode())



    return render_template ('results.html',  
                    foursq_ids_in_results   =foursq_ids_in_results,
                    status_query            =status_query,
                    matching_ids            =matching_ids,
                    results_check           =results_check,
                    open_venues             =open_venues,
                    )

@app.route('/venueinfo/<id>')
def venue_more_infomration(id):

    return render_template (hours   =venue_hours(id),
                            photos  =instagram_engine.location_search(id))

@app.route('/venuepics/<id>')
def instagram_picture_finder(id):
    """renders recent instagram photos from a specific venue"""

    return render_template ('listing.html', 
                            photos=instagram_engine.location_search(id))







@app.route("/twilio", methods=['GET', 'POST'])
def half_full_report():
    
    # setting up session counter to allow for tracking conversations
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    # Test to make sure counter is behaving as expected
    print counter

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
        print venues

        if 'half' in busy_status:
            status_code=0
        elif 'slammed' in busy_status:
            status_code=1

        session['status_code']=status_code
        print status_code


        sqlsession = connect()

        s                       = Status()
        s.venue_name            = venues[0]['name']
        s.foursquare_id         = venues[0]['id']
        s.status                = status_code
        s.time                  = datetime.utcnow()
        s.expiration_status     = 'Fresh'



        print "FOURSQUARE ID %r" % s.foursquare_id
        print "STATUS CODE %r" % s.status
        print "DATE TIME%r" % s.time
        
        print type(sqlsession)
        sqlsession.add(s)

        
        sqlsession.commit()
        session['first_id'] = s.id


       
        # TEST to make sure venues are coming out correctly
        # print venues
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
        # print ALTERNATE_OPTIONS

        # Store this list to the session so if user texts back we can access
        # the information and update the database as needed

        session['ALTERNATE_OPTIONS'] = ALTERNATE_OPTIONS
        print "session %r" % ALTERNATE_OPTIONS
        # String that is used in response to user
        ALTERNATE_STRING = ''
        for i in range(1, len(ALTERNATE_OPTIONS)):
            ALTERNATE_STRING = ALTERNATE_STRING + str(ALTERNATE_OPTIONS[i][0]) + ": " + ALTERNATE_OPTIONS[i][1][0] + ", " + ALTERNATE_OPTIONS[i][1][1] + "\n"

        # print "STRING %s" % ALTERNATE_STRING
        # Setting up variables to be used in Response Message. primary_venue_name
        # is the first response from the foursquare API and is the assumed correct
        # match for the search, unless user indicates otherwise.
        primary_venue_name      = (venues[0]['name']).encode()
        primary_venue_address   = (venues[0]['location']['formattedAddress'][0]).encode()
       
        slammed_confirmation_message    = """Thanks for letting us know that %s at %s is THE WORST. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
        safe_confirmation_message       = """Thanks for letting us know that %s at %s is a Safe Zone. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
        # print len(venues)

        # Check to see if more than one venue in response. There will be no
        # alternates offered if query only results in one response.
        if len(venues) > 1:
            if 'slammed' in busy_status:
                with response.message() as message:
                    message.body = "{0}\n{1}\n{2}".format(slammed_confirmation_message,
                                                    ALTERNATE_INTRO, ALTERNATE_STRING)
                # print response
                # print message.body
                return unicode(response).encode("utf-8")


            elif 'half' in busy_status:
                with response.message() as message:
                    message.body = "{0}\n{1}\n{2}".format(safe_confirmation_message,
                                                    ALTERNATE_INTRO, ALTERNATE_STRING)

                return unicode(response).encode("utf-8")


        # For queries that result in a single response. No alternates provided.
        elif len(venues) == 1:
            if 'slammed' in busy_status:
                with response.message() as message:
                    message.body = "{0}".format(slammed_confirmation_message)

                
                                                
            elif 'half' in busy_status:
                with response.message() as message:
                    message.body = "{0}".format(safe_confirmation_message)

                


        else:
            with response.message() as message:
                message.body = "{0}".format(HELP_MESSAGE)

            session.clear()
        
        print 'RESPONSE%r' % response
        return 'hello'
        return unicode(response).encode("utf-8")

    def corrected_report():
        
        ALTERNATE_OPTIONS = session.get('ALTERNATE_OPTIONS', 0)
        status_code = session.get('status_code', 0)
        
        print "STATUS CODE IN SESSION %r" % status_code
        print type(status_code)


        first_id = session.get('first_id', 0)
            
        alternate_enumerated_options = ['1','2','3']

        if BODY in alternate_enumerated_options:
            body = int(BODY)

            response_list = []
            for i in ALTERNATE_OPTIONS:
                response_list.append(i[1])


            updated_response_message = """Got it, you meant %s at %s.""" % (response_list[body][0],
                                                                            response_list[body][1])
                
            sqlsession = connect()

            sqlsession.query(Status).filter_by(id=first_id).delete()

            s                   = Status()
            s.venue_name        = response_list[body][0]
            s.foursquare_id     = response_list[body][2]
            s.status            = status_code
            s.time              = datetime.utcnow()
            s.expiration_status = 'Fresh'

            print "FOURSQUARE ID %r" % s.foursquare_id
            print "STATUS CODE %r" % s.status
            print "DATE TIME%r" % s.time
            
            print type(sqlsession)
            sqlsession.add(s)


            sqlsession.commit()
            with response.message() as message:
                        message.body = "{0}".format(updated_response_message)
            session.clear()
        
        else:
            try:
                body = int(BODY)
                with response.message as message:
                    message.body = "Sorry! %r is not a valid option. Please pick 1, 2, or 3." % body
            except ValueError:
                new_user_report()
                session.clear()
            


        return unicode(response).encode("utf-8")




    if counter == 1:
        return new_user_report()
    if counter == 2:
        return corrected_report()
    if counter == 3:
        return corrected_report()
    if counter > 3:
        with response.message as message:
            message.body = "Huh, not quite sure what you mean. If you're trying to report a venue, please respond with 'Venue Name: City: Slammed/Half Full'."""
 














        # Split message body on colons to parse out informatio to add to the
        # Hot Tip Database

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


    #         updated_response_message = """Got it, you meant %s.""" % response_list[body][0]

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













# @app.route('/oauth_callback')
# def on_callback(): 
#     code = request.args.get("code")
#     if not code:
#         return 'Missing code'
#     try:
#         access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
#         if not access_token:
#             return 'Could not get access token'
#         api = client.InstagramAPI(access_token=access_token)
#         print api
#         request.session['access_token'] = access_token
#         print ("access token="+access_token)
#     except Exception as e:
#         print(e)
#     return render_template("results.html")








# @app.route('/location_search')
# def location_search(): 
#     access_token = "34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
#     content = "<h2>Location Search</h2>"
#     # if not access_token:
#     #     return 'Missing Access Token'
#     # try:
#     api = client.InstagramAPI(access_token=access_token)
#     location_search = api.location_search(lat="47.615608",lng="-122.339350",distance=1000)
#     locations = []
#     # for location in location_search:
#     #     locations.append('<li>%s  <a href="https://www.google.com/maps/preview/@%s,%s,19z">Map</a>  </li>' % (location.name,location.point.latitude,location.point.longitude))
    


#     for location in location_search:
#     	locations.append('<li> %s' % location.name)

#     content += ''.join(locations)
#     return content
    # except Exception as e:
    #     print(e)   

# @app.route('/media_search')
# def media_finder():
# 	access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
# 	content = "<h2>Location Search</h2>"

# 	api = client.InstagramAPI(access_token=access_token)
        
# 	media_search = api.media_search(lat="40.7050789",lng="-73.93364403",distance=100)

#         print type(media_search)
#         print media_search
#         print dir(media_search)


# 	photos = []
# 	for media in media_search:
# 		photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
# 	content += ''.join(photos)
    

#         print content
#         return content




    #'lat': 40.70507898542075, 'lng': -73.93364403923762

    # location_search = api.location_search()
  	       
    # return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)





if __name__ == "__main__":
    app.run(debug = True)