from flask import Flask, render_template, request, session as flasksession, redirect, url_for
from twilio_model import update_db_from_twilio
import twilio_model
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
from database_update import UpdateDatabase




app = Flask(__name__)
app.secret_key= 'katescoolproject'



@app.route("/", methods = ['POST', 'GET'])
def half_full_home():
    """Home page. Basic search box with venue category options"""

    return render_template("index.html")

@app.route('/test')
def test_page():

    # expire_statuses()
    venue_search = SearchForVenue().search_by_name_city('bar 355', 'oakland')
    return render_template("test.html",
                            foursquare_venues_by_latlong=venue_search)
    



@app.route("/search", methods = ['POST', 'GET'])
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


@app.route("/searchforvenue", methods=['POST', 'GET'])
def specific_venue_search():

    venue   = request.form.get('search_venue')
    city    = request.form.get('search_city')

    venue_search = SearchForVenue().search_by_name_city(venue,city)
    
    return render_template ('results.html',
                            foursquare_venues_by_latlong=venue_search,
                            )


@app.route("/about")
def about_page():
    return render_template ('about.html')

@app.route("/updatedatabasesafe", methods=['POST'])
def get_safe_report():

    venue_name      = request.form['venue-name-safe']
    foursquare_id   = request.form['foursquare-id-safe']
    venue_status    = '0'


    
    UpdateDatabase().add_new_rating(venue_name, foursquare_id ,venue_status)

    return redirect('/venueinfo/%s'%foursquare_id)

@app.route("/updatedatabaseslammed", methods=['POST'])
def get_slammed_report():

    venue_name      = request.form['venue-name-slammed']
    foursquare_id   = request.form['foursquare-id-slammed']
    venue_status    = '1'
    
    UpdateDatabase().add_new_rating(venue_name, foursquare_id ,venue_status)

    return redirect('/venueinfo/%s'%foursquare_id)


@app.route("/twilio", methods=['GET', 'POST'])
def twilio_user_report():

    
    return twilio_model.Twilio().conversation_counter(request.values.get('Body'),twilio.twiml.Response()) 


if __name__ == "__main__":
    app.run(debug = True)