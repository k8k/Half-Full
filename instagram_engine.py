from instagram import client as instagram_client
import urllib


def location_search(foursquare_id):
        access_token="34946503.b8fc6f7.27686630c22b44eaad7754776d061fb7"
        api = instagram_client.InstagramAPI(access_token=access_token)
        
        
        # Getting Instagram ID objects from Foursquare ID
        instagram_id_info = api.location_search(foursquare_v2_id=foursquare_id)
        instagram_id = int(instagram_id_info[0].id)
        
        # Searching for all media tagged at location, based on Instagram ID
        media_search = api.location_recent_media(location_id=int(instagram_id))
        
        # Stripping unnecessary info out of media_search list       
        media_search = media_search[0]
        

        return media_search



        # photos = []
        # for media in media_search:
        #         photos.append(media.get_standard_resolution_url())

        # print photos
        # return photos




        # return urllib.unquote(content).decode('utf8')
        

    