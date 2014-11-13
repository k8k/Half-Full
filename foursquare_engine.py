import foursquare
import os


FOURSQUARE_CLIENT_ID=os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET=os.environ.get('FOURSQUARE_CLIENT_SECRET')

# Construct the client object
client = foursquare.Foursquare(client_id=FOURSQUARE_CLIENT_ID, client_secret=FOURSQUARE_CLIENT_SECRET)

def foursquare_search_by_category(latlng, category):

    # Create a list of venue categories to exclude from results

    blacklist=  ['4bf58dd8d48988d125941735', '52e81612bcbc57f1066b79ed', 
                '4bf58dd8d48988d124941735']


    # Create a dictionary that will be used to search 4sq DB of venues

    results_dictionary =    {'ll': latlng,
                            'verified' : True,
                            'intent': 'checkin', 
                            'radius': '100',
                            'limit': '15'}
    
    # Check to see if there is a specified category - if so add to search
    # dictionary

    if category != False:
        results_dictionary['categoryId'] = category  

    places_by_category = client.venues.search(params=results_dictionary)

    # Drilling down to "venues" within the 4q objects that are returned
    # to remove excess information and simplify later code

    venues = places_by_category['venues']
    
    # Creating a list of venues that meet the specified search criteria

    category_list = []
    for i in range(len(venues)):
        for j in range(len(venues[i]['categories'])):
            if venues[i]['categories'][j]['id'] not in blacklist:
                category_list.append(venues[i])

   
    return category_list


def update_db_from_twilio(venue_name, city, busy_status):
    likely_places = client.venues.search(params=    {'query': venue_name,
                                                    'near': city,
                                                    'verified': True,
                                                    'intent': 'checkin',
                                                    })
    likely_venues = likely_places['venues']

    # print "IS THIS A GOOD ANSWER ?? %r, %r " % (likely_venues[0]['name'], likely_venues[0]['location']['formattedAddress'])
    # print " if not, text the following numbers for which venue is correct: \n"
    # print "1: %r, %r:" % (likely_venues[1]['name'], likely_venues[1]['location']['formattedAddress'])
    # print "2: %r, %r:" % (likely_venues[2]['name'], likely_venues[2]['location']['formattedAddress'])
    # print "3: %r, %r:" % (likely_venues[3]['name'], likely_venues[3]['location']['formattedAddress'])
    # print "4: %r, %r:" % (likely_venues[4]['name'], likely_venues[4]['location']['formattedAddress'])
    # print "5: %r, %r:" % (likely_venues[5]['name'], likely_venues[5]['location']['formattedAddress'])
    return likely_venues
#
# print update_db_from_twilio('Starbucks', 'Berkeley, CA', 'SLAMMED')



# Current 4sq venue category IDs. For testing - will update to a script
# that dynamically pulls from the 4sq DB.

# potential coffee spots
coffee_id = '4bf58dd8d48988d1e0931735'
cafe_id = '4bf58dd8d48988d16d941735'
bakery_id = '4bf58dd8d48988d16a941735'
bagel_shop_id = '4bf58dd8d48988d179941735'

# bars
nightlife_id = '4d4b7105d754a06376d81259'

# remove from results
stripclub_id = '4bf58dd8d48988d1d6941735'

# restaurants
restaurant = '4d4b7105d754a06374d81259'



