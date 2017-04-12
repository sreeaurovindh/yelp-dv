from flask import Blueprint
from flask import jsonify
from flask import request
from db.Mongo import mongo
from services import recommendService as recommend
from services import commonAttributes
from services import businessService as business

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
    return commonAttributes.get_common_attributes(business_id, radius)
  except Exception as err:
    return jsonify({'error' : "Something went wrong! "+ str(err)})
    
@mongo_api.route("/business/locationtype/<locationtype>/location/<location>", methods=['GET'])
def get_restaurant_details(locationtype, location):
  try:
    res = business.get_business_details_by_location(locationtype, location)
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