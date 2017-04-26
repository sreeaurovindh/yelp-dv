from flask import Blueprint
from flask import jsonify
from flask import request
from db.Mongo import mongo
from services import recommendService as recommend
from services import commonAttributes
from services import businessService as business
from services import foodOnBizReviews

mongo_api = Blueprint('mongo_api', __name__)

@mongo_api.route("/collections")
def get_data():
  try:
    collections = mongo.db.collection_names()
    return jsonify({'collections' : collections})
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

@mongo_api.route("/collection/<coll>", methods=['GET'])
@mongo_api.route("/collection/<coll>/limit/<limit>", methods=['GET'])
def get_data_from_collection(coll, limit=""):
  try:
    if not limit:
      output = list(mongo.db[coll].find({}, {"_id": 0}))
    else:
      output = list(mongo.db[coll].find({}, {"_id": 0}).limit(int(limit)))
    return jsonify({'data' : output})
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

@mongo_api.route("/recommendrestaurants/businessid/<businessid>/userid/<userid>", methods=['GET'])
def recommend_restaurants(businessid, userid):
  try:
    res = recommend.recommend_restaurant(userid, businessid)
    return jsonify({'data' : res})
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

#Gets the top 5 most common attributes between the target business_id and
#  other business_ids that are within the defined radius
@mongo_api.route("/attributes/<business_id>/radius/<radius>", methods=['GET'])
def get_common_attributes(business_id, radius):
  try:
    return commonAttributes.get_restaurant_attributes(business_id, radius)
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

#Gets the data for stacked bar chart(Sree) - Target Biz chart data
@mongo_api.route("/foodqualityvariation/<business_id>", methods=['GET'])
def get_target_food_quality(business_id):
  try:
    return foodOnBizReviews.getTargetBizChart(business_id)
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

#Gets the data for stacked bar chart(Sree) - Neighboring Biz chart data
@mongo_api.route("/foodqualityvariation/<business_id>/radius/<radius>", methods=['GET'])
def get_neighboring_food_quality(business_id, radius):
  try:
    return foodOnBizReviews.getNeighboringBizChart(business_id, radius)
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

#Gets the food item data for bubble chart(Sree) - food items within start/end dates
@mongo_api.route("/foodItems/<business_id>/radius/<radius>/start_year/<start_year>/end_year/<end_year>", methods=['GET'])
def get_food_items(business_id, radius, start_year, end_year):
  try:
    return foodOnBizReviews.getFoodItems(business_id, radius, start_year, end_year)
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

@mongo_api.route("/business/locationtype/<locationtype>/location/<location>/<cuisine>", methods=['GET'])
def get_restaurant_details(locationtype, location, cuisine):
  try:
    res = business.get_business_details_by_location(locationtype, location, cuisine)
    return jsonify({'data' : res})
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

@mongo_api.route("/userlistbybusinessid/<business_id>", methods=['GET'])
def user_list_by_businessid(business_id):
  try:
    res = business.user_list_by_businessid(business_id)
    return jsonify({'data' : res})
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})

# -------dummy database calls--------- #
@mongo_api.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})
# -------dummy database calls--------- #

if __name__ == '__main__':
    app.run(debug=True)