from db.Mongo import mongo
from operator import itemgetter

def get_business_details_by_location(location_type, location, cuisine):
  query = {}
  business_limit = 100
  if location_type == "state":
    query['state'] = location.upper()
    business_limit = 300
  elif location_type == "city":
    query['city'] = location
    if cuisine != "none":
      query['categories'] = cuisine
    business_limit = 200
  else:
    return {}

  business_list = list(mongo.db['foodbusiness']
  .find(query, { "_id" : 0, 'business_id' : 1, 'name' : 1, 'address' :1, 'latitude' : 1, 'longitude': 1, 'stars':1})
  .sort('stars', -1)
  .limit(business_limit))
  
  for business in business_list:
    business['location'] = {'lat': business['latitude'], 'lng': business['longitude']}
    business.pop('latitude', None)
    business.pop('longitude', None)

  return business_list


def user_list_by_businessid(business_id):
  query = { 'business_id' : business_id }
  review_limit = 100
  number_of_users = 10
  user_mapping = {}

  review_list = list(mongo.db['foodreviews']
  .find( query, { "_id" : 0, 'user_id' : 1})
  .limit(review_limit))

  for review in review_list:
    if review['user_id'] in user_mapping:
      user_mapping[review['user_id']] += 1
    else:
      user_mapping[review['user_id']] = 1

  user_mapping = sorted(user_mapping.items(), key=itemgetter(1), reverse=True)[:number_of_users]
  user_mapping = [x[0] for x in user_mapping]

  user_list = list(mongo.db['fooduser'].find( { 'user_id' : {'$in': user_mapping}}, { "_id" : 0, 'user_id' : 1, 'name' : 1}))

  return user_list