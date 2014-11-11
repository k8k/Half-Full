import foursquare
import os
from instagram import client as instagram_client

# FOURSQUARE_CLIENT_ID=os.environ.get('FOURSQUARE_CLIENT_ID')
# FOURSQUARE_CLIENT_SECRET=os.environ.get('FOURSQUARE_CLIENT_SECRET')
# construct the client object

FOURSQUARE_CLIENT_ID='RZBEONUJFRJ31GYUW3B4Q0JFULK5P3MJEDUSRWHGT5AWYAXG'
FOURSQUARE_CLIENT_SECRET='SUDCP5HHNJ0WNATZFC5WDHWQOHC5GGTXTEKXA1DDUROS4D5R'


client = foursquare.Foursquare(client_id=FOURSQUARE_CLIENT_ID, client_secret=FOURSQUARE_CLIENT_SECRET)



#####MAY NEED TO CHANGE THESE -- KEYS CHANGE, can't figure out where they keep them
#####in an accessible format.


## potential coffee spots
coffee_id = '4bf58dd8d48988d1e0931735'
cafe_id = '4bf58dd8d48988d16d941735'
bakery_id = '4bf58dd8d48988d16a941735'
bagel_shop_id = '4bf58dd8d48988d179941735'

## bars
nightlife_id = '4d4b7105d754a06376d81259'
## remove from results
stripclub_id = '4bf58dd8d48988d1d6941735'

## restaurants
restaurant = '4d4b7105d754a06374d81259'




# latlong = '37.7781253,-122.41508440000001'



def foursquare_search_by_category(latlng, category):
    access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
    api = instagram_client.InstagramAPI(access_token=access_token)

    blacklist = ['4bf58dd8d48988d125941735', '52e81612bcbc57f1066b79ed', 
                 '4bf58dd8d48988d1f4931735', '4bf58dd8d48988d124941735']

    ##blacklist = Tech Startup, Outdoor Sculpture, Race Track, Office
    
    results_dictionary = {'ll': latlng,
            'verified' : True,
            'intent': 'browse', 
            'radius': '2000',
            'limit': '2'}

            ## changed limit to 2 to increase testing speed

    if category != False:
        results_dictionary['categoryId'] = category  

    places_by_category = client.venues.search(params=results_dictionary)

    venues = places_by_category['venues']
    # print "LAT LONG %r" % latlng
    # print "VENUES %r" % venues

    category_list = []

    for i in range(len(venues)):
        # print venues[i] 
        for j in range(len(venues[i]['categories'])):
            if venues[i]['categories'][j]['id'] not in blacklist:
                category_list.append(venues[i])

    # print "CATEGORY LIST %r" % category_list
    
    id_list = []
    for k in category_list:
        id_list.append(k['id'])

    print "ID LIST %r" % id_list

    mapped_foursquare_ids = []
    for n in range(len(id_list)):
        mapped_foursquare_ids.append(api.location_search(foursquare_v2_id=id_list[n]))

    print "MAPPED IDS %r" % mapped_foursquare_ids

    instagram_ids = []    
    for i in range(len(mapped_foursquare_ids)):
        instagram_ids.append(int(mapped_foursquare_ids[i][0].id))

    print "INSTAGRAM IDs %r" % instagram_ids
   
    return category_list

# def instagram_pics(list_of_venues):
#     for i in (list_of_venues):
#         print i['id']



# print instagram_pics(foursquare_search_by_category)




    # venues = places_by_category['venues']
    # print venues[1]
    # bar_list = []
    # for i in venues:
    #   bar_list.append(i['name'])

    # return bar_list

# print "BARS:" + str(foursquare_search_by_category(nightlife_id))
# print "COFFEE:" + str(foursquare_search_by_category(coffee_id))
# print "FOOD:" + str(foursquare_search_by_category(food_id))






