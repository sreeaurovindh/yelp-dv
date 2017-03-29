from flask import Blueprint
from flask import jsonify
from flask import request
from db.Mongo import mongo

mongo_api = Blueprint('mongo_api', __name__)

@mongo_api.route("/collections")
def getData():
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


# -------dummy database calls--------- #
@mongo_api.route('/star', methods=['GET'])
def get_all_stars():
  star = mongo.db.stars
  output = []
  for s in star.find():
    output.append({'name' : s['name'], 'distance' : s['distance']})
  return jsonify({'result' : output})

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