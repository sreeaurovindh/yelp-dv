from db.Mongo import mongo

def get_business_details_by_location(location_type, location):
  query = {}
  business_limit = 100
  if location_type == "state":
    print("state")
    query['state'] = location.upper()
    business_limit = 300
  elif location_type == "city":
    print("city")
    query['city'] = location
    business_limit = 200
  elif location_type == "zipcode":
    print("zipcode")
    query['postal_code'] = location
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