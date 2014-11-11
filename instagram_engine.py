from instagram import client as instagram_client



def location_search(instagram_ids):
        

        access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
        api = instagram_client.InstagramAPI(access_token=access_token)
        
        ### Get foursquare ids to link up to instagram pics
        # id_list = []
        # for k in list_of_foursquare_ids:
        #     id_list.append(k['id'])

        # print id_list

        # test_search = api.location_search(foursquare_v2_id=id_list[0])
        # # print test_search
        # # print dir(test_search)
        # # print type(test_search)
      
        # print dir(test_search[0])
        # print "TYPE %r" % type(test_search[0])
        # print "\n\n\n\n\n DIRRRR \n %r" % dir(test_search[0].id)
        # print type(test_search[0].id)

        # mapped_foursquare_ids = []
        # for n in range(len(id_list)):
        #     mapped_foursquare_ids.append(api.location_search(foursquare_v2_id=id_list[n]))

        # print "MAPPED IDS %r" % mapped_foursquare_ids
        
        # instagram_ids = []    
        # for i in range(len(mapped_foursquare_ids)):
        #     instagram_ids.append(int(mapped_foursquare_ids[i][0].id))

        print "INSTAGRAM IDs %r" % instagram_ids

        # print type(instagram_ids[0])
        # print api.location_recent_media(location_id=113278)

        # print dir(api.location_recent_media(location_id=113278))
        
        media_search = []
        for item in instagram_ids:
            media_search.append(api.location_recent_media(location_id=int(item)))

        # print media_search
        print media_search[0][0]
        return '<img src="%s"/>' % media_search[0][0][0].get_standard_resolution_url()
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

print location_search([182, 1572])
# photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
#     content += ''.join(photos)
    