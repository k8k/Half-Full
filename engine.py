from flask import Flask, render_template, request, session as flasksession, redirect
from twilio_model import update_db_from_twilio
from instagram_engine import InstagramSearch
import twilio.twiml
from twilio.rest import TwilioRestClient
from user_report_model import Status, Session as SQLsession, connect
from datetime import datetime
from user_reports_engine import expire_statuses
from geocoder import Geocoder
from specificsearch import SearchForVenue
import constants as c
from venue import Venue, VenueType




app = Flask(__name__)
app.secret_key= 'katescoolproject'



@app.route("/", methods = ['POST', 'GET'])
def half_full_home():
    """Home page. Basic search box with venue category options"""

    return render_template("index.html")

@app.route('/test')
def test_page():

    venue_search = SearchForVenue().search_by_name_city('bar 355', 'oakland')
    return render_template("test.html",
                            foursquare_venues_by_latlong=venue_search)
    

    expire_statuses()





@app.route("/search", methods = ['POST'])
def return_matching_venues():
    """Take user location and venue type, check for existing reports in
    database. If user report is in database that is 'Fresh,' then override
    foursquare check-in information """
    
    
    #Get information from form and query Foursquare's API for matching venues
    location = Geocoder(request.form.get('user_location', '37.80,122.27')).fetch()
    venue_type = VenueType[request.form.get('venue-type', 'bar')].value
    foursquare_venues_by_latlong = SearchForVenue().venues_with_user_status(location, venue_type)

    return render_template ('results.html',  
                    foursquare_venues_by_latlong    =foursquare_venues_by_latlong)


@app.route('/venueinfo/<id>', methods=['POST', 'GET'])
def venue_more_information(id):
    """Return detailed information about selected venue"""

    return render_template ('listing.html',
                            photos      = InstagramSearch().recent_media_search(id),
                            info        = Venue(id).info(),
                            instainfo   = InstagramSearch().venue_name(id))


@app.route("/searchforvenue/", methods=['POST'])
def specific_venue_search():

    venue_search = SearchForVenue().search_by_name_city(request.form['search_venue'], request.form['search_city'])
    
    return render_template ('results.html',
                            foursquare_venues_by_latlong=venue_search,
                            )





@app.route("/twilio", methods=['GET', 'POST'])
def half_full_report():
    
    # setting up session counter to allow for tracking conversations
    counter = flasksession.get('counter', 0)
    counter += 1
    flasksession['counter'] = counter

    # Test to make sure counter is behaving as expected
    print counter



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
                message.body = "{0}".format(c.HELP_MESSAGE)
                flasksession.clear()
            return str(response)


        # calling function from foursquare_engine that will query the foursquare
        # API using the parameters defined in the user's incoming test message
        venues = update_db_from_twilio(venue_name, city, busy_status)
        print venues

        if 'half' in busy_status:
            status_code=0
        elif 'slammed' in busy_status:
            status_code=1
        else:
            with response.message() as message:
                message.body = "{0}".format(c.HELP_MESSAGE)
                flasksession.clear()
            return str(response)



        flasksession['status_code']=status_code
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
        flasksession['first_id'] = s.id

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

        # Store this list to the flasksession so if user texts back we can access
        # the information and update the database as needed

        flasksession['ALTERNATE_OPTIONS'] = ALTERNATE_OPTIONS
        print "flasksession %r" % ALTERNATE_OPTIONS
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
                                                    c.ALTERNATE_INTRO, ALTERNATE_STRING)
                # print response
                # print message.body
                return unicode(response).encode("utf-8")


            elif 'half' in busy_status:
                with response.message() as message:
                    message.body = "{0}\n{1}\n{2}".format(safe_confirmation_message,
                                                    c.ALTERNATE_INTRO, ALTERNATE_STRING)

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
                message.body = "{0}".format(c.HELP_MESSAGE)

            flasksession.clear()
        
        print 'RESPONSE%r' % response
        return 'hello'
        return unicode(response).encode("utf-8")

    def corrected_report():
        
        ALTERNATE_OPTIONS = flasksession.get('ALTERNATE_OPTIONS', 0)
        status_code = flasksession.get('status_code', 0)
        
        print "STATUS CODE IN flaskSESSION %r" % status_code
        print type(status_code)


        first_id = flasksession.get('first_id', 0)
            
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
            flasksession.clear()
        
        else:
            try:
                body = int(BODY)
                with response.message as message:
                    message.body = "Sorry! %r is not a valid option. Please pick 1, 2, or 3." % body
            except ValueError:
                new_user_report()
                flasksession.clear()
            


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
            return unicode(response).encode('utf-8')








if __name__ == "__main__":
    app.run(debug = True)