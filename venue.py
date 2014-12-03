import constants as c
import foursquare
from enum import Enum


class Venue(object):
    """docstring for Venue"""
    def __init__(self, venue_id):
        super(Venue, self).__init__()
        self.venue_id = venue_id
        self.client   = foursquare.Foursquare(client_id=c.FOURSQUARE_CLIENT_ID, client_secret=c.FOURSQUARE_CLIENT_SECRET)


    def info(self):
        full_venue_info = self.client.venues(self.venue_id)
        return full_venue_info

    def hours(self):
        if 'hours' in self.client.venues(self.venue_id)['venue']:
            opening_hours=self.client.venues(self.venue_id)['venue']['hours'] 
        else:
            opening_hours = ''

        return opening_hours


class VenueType(Enum):
    restaurant  = '4d4b7105d754a06374d81259'
    bar         = '4d4b7105d754a06376d81259'
    cafe        = '4bf58dd8d48988d1e0931735'

    # potential coffee shops
    coffee      = '4bf58dd8d48988d1e0931735'
    bakery      = '4bf58dd8d48988d16a941735'
    bagel_shop  = '4bf58dd8d48988d179941735'

    # bars
    nightlife   = '4d4b7105d754a06376d81259'

    # remove from results
    stripclub   = '4bf58dd8d48988d1d6941735'




print Venue('40a55d80f964a52020f31ee3').info()