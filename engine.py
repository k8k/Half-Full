from flask import Flask, render_template, request
import os
from instagram import client
import requests
from foursquare_engine import foursquare_search_by_category, update_db_from_twilio
import instagram_engine
import twilio.twiml
from twilio.rest import TwilioRestClient



app = Flask(__name__)
app.secret_key= os.environ.get("APP_SECRET_KEY")

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



    return render_template ('results.html', user_longitude=user_longitude, 
                            user_latitude=user_latitude, 
                            results = foursquare_search_by_category(location, venue_type), 
                            )


@app.route('/venuepics/<id>')
def instagram_picture_finder(id):
    """renders recent instagram photos from a specific venue"""

    return render_template ('listing.html', 
                            photos=instagram_engine.location_search(id))



@app.route("/twilio", methods=['GET', 'POST'])
def half_full_report():

    # message = "Starbucks: San Francisco: Slammed"
    # from_number = request.values.get('From')

    body = request.values.get('Body')
    from_number = request.values.get('From')
    print "FROM %r" % from_number
    print body
    
    print body
    body = body.split(": ")
    venue_name = body[0].lower()
    city = body[1].lower()
    busy_status = body[2].lower()
    print venue_name
    print city
    print busy_status

    venues = update_db_from_twilio(venue_name, city, busy_status)



    print "thanks for that report about %r at  %r" % (venues[0]['name'], venues[0]['location']['formattedAddress'][0])
    
    # print type(venues)

    # venue_dictionary = {}
    # for i in range(len(venues)):
    #     venue_dictionary[(venues[i]['location']['formattedAddress'][0])] = venues[i]['name']

    # venue_list = []
    # for i in range(len(venues)):
    #     venue_list.append({venues[i]['location']['formattedAddress'][0]: venues[i]['name']})

    # print venue_list

    if "half full" in busy_status:

        message = """Thanks for letting  us know that %s at %s is a Safe Zone. If you meant one of the below locations instead, simply reply to this text with the corresponding number.\n1: %s, %s \n2: %s, %s \n3: %s, %s \n4: %s, %s\n
        """ % (venues[0]['name'], venues[0]['location']['formattedAddress'][0],
            venues[1]['name'], venues[1]['location']['formattedAddress'][0],
            venues[2]['name'], venues[2]['location']['formattedAddress'][0],
            venues[3]['name'], venues[3]['location']['formattedAddress'][0],
            venues[4]['name'], venues[4]['location']['formattedAddress'][0])

    elif "slammed" in busy_status:

        message = """Thanks for letting  us know that %s at %s is a THE WORST. If you meant one of the below locations instead, simply reply to this text with the corresponding number.\n1: %s, %s \n2: %s, %s \n3: %s, %s \n4: %s, %s\n
        """ % (venues[0]['name'], venues[0]['location']['formattedAddress'][0],
            venues[1]['name'], venues[1]['location']['formattedAddress'][0],
            venues[2]['name'], venues[2]['location']['formattedAddress'][0],
            venues[3]['name'], venues[3]['location']['formattedAddress'][0],
            venues[4]['name'], venues[4]['location']['formattedAddress'][0])

    
    else:
        message = """we didn't get that! you said %s in %s was %s, please
                    respond with 'venue name: the city its in: and either SLAMMED
                    or HALF FULL.' (ex) 'Blue Bottle: San Francisco, CA: SLAMMED' 
                    """ % (venue_name, city, busy_status)




    resp=twilio.twiml.Response()

    resp.message(message)
    return str(resp)










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