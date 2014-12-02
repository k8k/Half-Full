from instagram import client as instagram_client
import constants as c


class InstagramSearch(object):
        """docstring for InstagramSearch"""
        def __init__(self):
                super(InstagramSearch, self).__init__()
                self.access_token       = c.INSTAGRAM_CONFIG['access_token']
                

        def recent_media_search(self,foursquare_id):
                api = instagram_client.InstagramAPI(access_token=self.access_token)
                
                # Getting Instagram ID objects from Foursquare ID
                instagram_id_info = api.location_search(foursquare_v2_id=foursquare_id)
                try:
                        instagram_id = int(instagram_id_info[0].id)
                
                except IndexError:
                        media_search = "No Media"
                        return media_search
                
                # Searching for all media tagged at location, based on Instagram ID
                media_search = api.location_recent_media(location_id=int(instagram_id))
                
                # Stripping unnecessary info out of media_search list       
                media_search = media_search[0]
                if len(media_search) > 0:
                        return media_search
                else:
                        media_search = "No Media"
                        return media_search

        # def venue_name(self, foursquare_id):
        #         api = instagram_client.InstagramAPI(access_token=self.access_token)
                
        #         # Getting Instagram ID objects from Foursquare ID
        #         instagram_id_info = api.location_search(foursquare_v2_id=foursquare_id)
        #         return instagram_id_info[0].name
               



