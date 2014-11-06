import foursquare


FOURSQUARE_CLIENT_ID='RZBEONUJFRJ31GYUW3B4Q0JFULK5P3MJEDUSRWHGT5AWYAXG'
FOURSQUARE_CLIENT_SECRET='SUDCP5HHNJ0WNATZFC5WDHWQOHC5GGTXTEKXA1DDUROS4D5R'
# Construct the client object
client = foursquare.Foursquare(client_id='FOURSQUARE_CLIENT_ID', client_secret='FOURSQUARE_CLIENT_SECRET')


print client

print dir(client.venues)
# def foursquare_coffee_search():
# 	coffee_shops=client.venues.search(params={'query': 'coffee', 'll': '37.7781253,-122.41508440000001'})
# 	venues = coffee_shops['venues']
# 	coffee_shop_list = []
# 	for i in venues:
# 		coffee_shop_list.append(i['name'])

# 	return coffee_shop_list

# print foursquare_coffee_search()