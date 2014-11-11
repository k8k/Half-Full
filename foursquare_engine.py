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

    def location_search(list_of_shit):
        access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
        api = instagram_client.InstagramAPI(access_token=access_token)
        
        ### Get foursquare ids to link up to instagram pics
        id_list = []
        for k in list_of_shit:
            id_list.append(k['id'])

        print id_list
        test_search = api.location_search(foursquare_v2_id=id_list[0])
        # print test_search
        # print dir(test_search)
        # print type(test_search)
      
        print dir(test_search[0])
        print "TYPE %r" % type(test_search[0])
        print "\n\n\n\n\n DIRRRR \n %r" % dir(test_search[0].id)
        print type(test_search[0].id)

        mapped_foursquare_ids = []
        for n in range(len(id_list)):
            mapped_foursquare_ids.append(api.location_search(foursquare_v2_id=id_list[n]))

        # print "MAPPED IDS %r" % mapped_foursquare_ids
        
        instagram_ids = []    
        for i in range(len(mapped_foursquare_ids)):
            instagram_ids.append(int(mapped_foursquare_ids[i][0].id))

        # print "INSTAGRAM IDs %r" % instagram_ids

        # print type(instagram_ids[0])
        # print api.location_recent_media(location_id=113278)

        # print dir(api.location_recent_media(location_id=113278))
        
        media_search = []
        for item in instagram_ids:
            media_search.append(api.location_recent_media(location_id=int(item)))

        # print media_search
        print media_search[0][0]
        print media_search[0][0][0].get_standard_resolution_url()
        # print media_search[1]
        # photos = []
        # content = ''
        # for media in media_search:
        #     photos.append('<img src="%s"/>' % media_search[0][0][0].get_standard_resolution_url())
        # content += ''.join(photos)

        # print content

        # # print photos_list
        # print type(photos_list)
        # print type(photos_list[0])
        # actual_photos = []
        # content = ''
        # for media in photos_list:
        #     actual_photos.append('<img src="%s">' % media.get_standard_resolution_url())
        #     content += ''.join(actual_photos)
        # return content 


        # photos = []
        # for ii in instagram_photos_by_location:
        #     photos.append(api.location)


        # photos = []
        # for m in range(len(id_list)):
        #     photos.append(api.location_search(m))
        # print photos
        # return photos

    print location_search(category_list)
# photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
#     content += ''.join(photos)
    
    

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



