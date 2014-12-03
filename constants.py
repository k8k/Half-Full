import os
from instagram import client as instaclient



#Google Maps API Key for Typeahead & Lat Long
GOOGLE_MAPS_EMBED_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

# Instagram Configuration
INSTAGRAM_CONFIG = {

    'client_id': os.environ.get("INSTAGRAM_CLIENT_ID"),
    'client_secret': os.environ.get("INSTAGRAM_CLIENT_SECRET"),
    'access_token': os.environ.get("INSTAGRAM_ACCESS_TOKEN")
}

unauthenticated_api = instaclient.InstagramAPI(**INSTAGRAM_CONFIG)


# Foursquare Keys
FOURSQUARE_CLIENT_ID=os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET=os.environ.get('FOURSQUARE_CLIENT_SECRET')


# Twilio Keys, pulled in from system environment
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')




#TWILIO MESSAGES
HELP_MESSAGE    ="We didn't get that! please respond with 'City, Venue Name, SLAMMED / HALF FULL.\n(ex) 'San Francisco Blue Bottle SLAMMED'. "
ALTERNATE_INTRO = """If you meant one of the places below instead, just reply to this text with the corresponding number."""
