from flask import Flask, render_template
import os
# from instagram import client, subscriptions

from googlemaps import user_venue_search


app = Flask(__name__)
app.secret_key= 'katekuchinproject'


GOOGLE_MAPS_EMBED_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

# CONFIG = {

#     'client_id': 'b8fc6f7c1c4d4d438b797bca091f80a4',
#     'client_secret': '8207a32e412b4cc2b25c96bdf79c7188',
#     'redirect_uri': 'http://localhost:5000/oauth_callback'
# }

# unauthenticated_api = client.InstagramAPI(**CONFIG)

@app.route("/")
def half_full_home():   
    return render_template("index.html")

@app.route("/location", methods=['POST', 'GET'])
def user_location():
    return user_venue_search()
    



    # return render_template("results.html", GOOGLE_MAPS_EMBED_KEY=GOOGLE_MAPS_EMBED_KEY,
                            # user_location=user_location)



# @app.route("/instagram")
# def instagram_connect():
#         	url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
#         	return '<a href="%s">Connect with Instagram</a>' % url




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
#     # except Exception as e:
#     #     print(e)   

# @app.route('/media_search')
# def media_finder():
# 	access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
# 	content = "<h2>Location Search</h2>"

# 	api = client.InstagramAPI(access_token=access_token)
        
# 	media_search = api.media_search(lat="40.731032",lng="-73.985619",distance=1000)

# 	photos = []
# 	for media in media_search:
# 		photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
# 	content += ''.join(photos)
#   	return content       
#     # return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)





if __name__ == "__main__":
    app.run(debug = True)