import foursquare
import os

FOURSQUARE_CLIENT_ID=os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET=os.environ.get('FOURSQUARE_CLIENT_SECRET')
# construct the client object

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
food_id = '4d4b7105d754a06374d81259'




latlong = '37.7781253,-122.41508440000001'



def foursquare_search_by_category(category):
	places_by_category = client.venues.search(params={'ll': latlong, 
											'intent': 'browse', 
											'radius': '50000', 
											'categoryId': category,
											'limit': '100'})


	venues = places_by_category['venues']

	category_list = []
	for i in venues:
		category_list.append({(i['name']):(i['hereNow']['count'])})


	return category_list 



	# venues = places_by_category['venues']
	# print venues[1]
	# bar_list = []
	# for i in venues:
	# 	bar_list.append(i['name'])

	# return bar_list

print "BARS:" + str(foursquare_search_by_category(nightlife_id))
print "COFFEE:" + str(foursquare_search_by_category(coffee_id))
print "FOOD:" + str(foursquare_search_by_category(food_id))

raiders4ever









