from flask import jsonify
from db.Mongo import mongo
from operator import itemgetter

def recommend_restaurant(user_id, business_id):
  number_of_recommended_business = 10
  user_id_list = set()
  business_id_list = set()
  business_user_mapping = {}
  output_list = []

  user_id_list.add(user_id)

  # get details of the particular user_id to find his friendlist
  fooduser = list(mongo.db['fooduser'].find({ 'user_id' : user_id }, { "_id" : 0, 'user_id' : 1, 'friends' : { '$slice' : 20 }}))
 
  if len(fooduser) > 0:

    # fetch the count of terms used by all the friends of the partucular user
    for friend_id in fooduser[0]['friends']:
      friendterms = list(mongo.db['recom1'].find({ 'user_id' : friend_id, 'business_id': { '$ne' : business_id }, '$and': [{ 'terms' : {"$not":{"$size":1}}}, { 'terms' : {"$not":{"$size":2}}}] }))
      user_id_list.add(friend_id)
      friend_terms_count = 0

      # iterate all the review terms for each friend
      for friend_business_terms in friendterms:
        friend_terms_count = 0
        business_id_list.add(friend_business_terms['business_id'])
        friend_terms_count = len(friend_business_terms['terms'])

        # check for business_id key. If present append list else add the tuple (friend_id, friend_terms_count)
        if friend_business_terms['business_id'] in business_user_mapping:
          business_user_mapping[friend_business_terms['business_id']].append((friend_id, friend_terms_count))
        else:
          business_user_mapping[friend_business_terms['business_id']] = [(friend_id, friend_terms_count)]

    business_avg_mapping = {}
    for business_key, values in business_user_mapping.items():
      sum = 0
      for user_item_count in values:
        sum += user_item_count[1]
      business_avg_mapping[business_key] = sum/len(values)
    
    # fetch top recommended restaurants
    business_avg_mapping = sorted(business_avg_mapping.items(), key=itemgetter(1), reverse=True)[:number_of_recommended_business]

    bus_list_temp = [x[0] for x in business_avg_mapping]
    # get business names
    businessnames = list(mongo.db['foodbusiness'].find({ 'business_id' : { '$in': bus_list_temp } }, { "_id" : 0, 'business_id' : 1, 'name' : 1}))
    # get friend names
    friendnames = list(mongo.db['fooduser'].find({ 'user_id' : { '$in': fooduser[0]['friends'] } }, { "_id" : 0, 'user_id' : 1, 'name' : 1}))

    friendlist_dict = {}
    for friend in friendnames:
      friendlist_dict[friend['user_id']] = friend['name']

    for businessiter in businessnames:
      user_list_final = [x[0] for x in business_user_mapping[businessiter['business_id']]]
      user_name_list = []
      for val in  user_list_final:
        user_name_list.append(friendlist_dict[val])
      output_list.append([businessiter['name'], user_name_list])
    return output_list
  else:
    print("No food user!")
    return {}
