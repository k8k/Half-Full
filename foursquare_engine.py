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
                            'intent': 'browse', 
                            'radius': '1000',
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

    categorized_list_of_venues = []
    for i in range(len(venues)):
        for j in range(len(venues[i]['categories'])):
            if venues[i]['categories'][j]['id'] not in blacklist:
                categorized_list_of_venues.append(venues[i])

    # print "THIS IS CATEGORY LIST %r" % categorized_list_of_venues
   
    return categorized_list_of_venues


def update_db_from_twilio(venue_name, city, busy_status):
    likely_places = client.venues.search(params=    {'query': venue_name,
                                                    'near': city,
                                                    'verified': True,
                                                    'intent': 'checkin',
                                                    })
    likely_venues = likely_places['venues']

   
    return likely_venues
#
# print update_db_from_twilio('Starbucks', 'Berkeley, CA', 'SLAMMED')


def specific_search(venue_name, venue_city):
    search_result = client.venues.search(params=    {'query': venue_name,
                                                    'near': venue_city,
                                                    'verified': True,
                                                    'intent': 'match',
                                                    })
    return search_result['venues'][0]['id']
    #Foursquare ID of closest match for venue given search: venue name & city

print specific_search('bar 355', 'oakland')

def venue_hours(venue_id):

    if 'hours' in client.venues(venue_id)['venue']:
        opening_hours=client.venues(venue_id)['venue']['hours'] 
    else:
        opening_hours = None

    return opening_hours

def venue_info(venue_id):
    full_venue_info = client.venues(venue_id)

    return full_venue_info





# venues()
# venues.add()
# venues.categories()
# venues.explore()
# venues.search()
# venues.trending()
# venues.events()
# venues.herenow()
# venues.listed()
# venues.menu()
# venues.photos()
# venues.similar()
# venues.tips()
# venues.edit()
# venues.flag()
# venues.edit()
# venues.proposeedit()
# venues.setrole()




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



