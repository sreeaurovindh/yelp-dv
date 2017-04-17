from flask import jsonify
from db.Mongo import mongo

# Finds the business name for corresponding business Ids
def get_business_names(nearby_restaurant_id_list):
    restaurant_names = []

    for biz_id in nearby_restaurant_id_list:
        restaurant = mongo.db['food_business'].find_one({ 'business_id' : biz_id })
        restaurant_names.append(restaurant['name'])

    return restaurant_names

#returns the list of all nearby restaurants within radius, capped by limit
def find_nearby_restaurants_id(business_id, radius, limit):
    location_query_pipeline = [
    {'$match': {'business_id': 'Sq596PqWNj7J0s-YAQmrQA'}},
    {'$project':{'_id':0,'loc':'$loc.coordinates'}}
    ]

    target_restaurant_location =  mongo.db['food_business'].aggregate(location_query_pipeline)
    target_coords = list(target_restaurant_location)[0]['loc']

    #radius/3959 will be search radius in radians
    neighbor_query_pipeline = [
        {'$match': {'loc': {'$geoWithin': {'$centerSphere' : [target_coords, float(radius)/3959 ]}}}},
        {'$limit': limit},
        {'$group': {'_id':1, 'businesses': {'$push' : '$business_id'}}}
        ]
    
    nearby_restaurant_id_mongo = mongo.db['food_business'].aggregate(neighbor_query_pipeline)
    return list(nearby_restaurant_id_mongo)[0]['businesses']

#Gets the top N most common attributes between the target business_id and
#  other business_ids that are within the defined radius
def get_restaurant_attributes(business_id, radius):
    nearby_restaurant_limit = 20
    items_required = 5
    
    nearby_restaurant_id_list = find_nearby_restaurants_id(business_id, radius, nearby_restaurant_limit)

    restaurant_names = get_business_names(nearby_restaurant_id_list)

    top_attr_polarity_list = []
    top_attr_list = []

    for i, biz_id in enumerate(nearby_restaurant_id_list):
        top_results = get_restaurant_top_attributes(biz_id)
        top_attr_polarity_list.append(top_results)
        top_attr_list.append([])
        top_attr_list[i] = set([o['_id'] for o in top_results])

    intersection = list(set.intersection(*top_attr_list))
    
    if len(intersection) >= items_required:
        intersection = intersection[:items_required]
    else:
        uniqueAttr = top_attr_list[0] - set(intersection)
        intersection = set(intersection) | set(list(uniqueAttr)[:items_required - len(intersection)])

    output_list = []

    for i, name in enumerate(restaurant_names):
        restaurant_dict = {}
        restaurant_dict['__Restaurant'] = name
        polarity_sum = 0
        for foodItem in intersection:
            for element in top_attr_polarity_list[i]:
                if element['_id'] == foodItem:
                    restaurant_dict[foodItem.title()] = element['polarity']
                    polarity_sum += element['polarity']
            if foodItem.title() not in restaurant_dict:
                restaurant_dict[foodItem.title()] = 0

        restaurant_dict['__Average'] = polarity_sum/items_required

        output_list.append(restaurant_dict)  

    return jsonify(output_list)

#Fetches the 50 most mentioned attributes from a restaurant
def get_restaurant_top_attributes(business_id):
    top_attr_query_pipeline = [
    {'$match': {'business_id': business_id}},
    {'$project': {'polarity': "$polarity", 'item': {'$toLower':"$item"},	'value': "$value"}},
    {'$group': {'_id': "$item", 'polarity': {'$avg': "$polarity"}, 'count' : {'$sum' : 1}}},
	{'$sort': {'count' : -1}},
	{'$limit' : 50}
    ]

    top_attr_mongo = mongo.db['data'].aggregate(top_attr_query_pipeline)
    return list(top_attr_mongo)