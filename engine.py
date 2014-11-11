from flask import Flask, render_template, request
import os
from instagram import client
import requests
# from GOOGGOOG import user_venue_search
from foursquare_engine import foursquare_search_by_category

app = Flask(__name__)
app.secret_key= 'katekuchinproject'


GOOGLE_MAPS_EMBED_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

CONFIG = {

    'client_id': 'b8fc6f7c1c4d4d438b797bca091f80a4',
    'client_secret': '8207a32e412b4cc2b25c96bdf79c7188',
    'redirect_uri': 'http://localhost:5000/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

@app.route("/", methods = ['POST', 'GET'])
def half_full_home():   
    return render_template("index.html")

# @app.route("/location", methods=['POST', 'GET'])
# def user_location():
#     return user_venue_search()

@app.route("/location", methods = ['POST'])
def user_lat_long():
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?sensor=false&key=AIzaSyDjesZT-7Vc5qErTJjS2tDIvxLQdYBxOEY&address=" +\
    request.form['user_location'])
    user_latitude = r.json()['results'][0]['geometry']['location']['lat']
    user_longitude = r.json()['results'][0]['geometry']['location']['lng']
    user_longitude = str(user_longitude)
    user_latitude = str(user_latitude)
    
    venue_type = False
    location = user_latitude + ',' + user_longitude
    if request.form['venue-type'] == 'restaurant':
        venue_type = '4d4b7105d754a06374d81259'
    elif request.form['venue-type'] == 'bar':
        venue_type = '4d4b7105d754a06376d81259'
    elif request.form['venue-type'] == 'cafe':
        venue_type = '4bf58dd8d48988d1e0931735'






    return render_template ('results.html', user_longitude=user_longitude, 
                            user_latitude=user_latitude, 
                            results = foursquare_search_by_category(location, venue_type))


@app.route('/venuepics')
def picture_finder():
    pass


@app.route("/instagram")
def instagram_connect():
        	url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        	return '<a href="%s">Connect with Instagram</a>' % url






@app.route('/oauth_callback')
def on_callback(): 
    code = request.args.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        api = client.InstagramAPI(access_token=access_token)
        print api
        request.session['access_token'] = access_token
        print ("access token="+access_token)
    except Exception as e:
        print(e)
    return render_template("results.html")








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

@app.route('/media_search')
def media_finder():
	access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
	content = "<h2>Location Search</h2>"

	api = client.InstagramAPI(access_token=access_token)
        
	media_search = api.media_search(lat="40.7050789",lng="-73.93364403",distance=100)

        print type(media_search)
        print media_search
        print dir(media_search)


	photos = []
	for media in media_search:
		photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
	content += ''.join(photos)
    
        return content




    #'lat': 40.70507898542075, 'lng': -73.93364403923762

    # location_search = api.location_search()
  	       
    # return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)





if __name__ == "__main__":
    app.run(debug = True)