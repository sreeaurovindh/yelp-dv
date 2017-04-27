from flask import Flask
from db.Mongo import mongo
from services.MongoAPI import mongo_api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# config details for mongodb
app.config['MONGO_DBNAME'] = 'yelp'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/yelp'

mongo.init_app(app)

# check connection
with app.app_context():
  dummy_object = mongo.db.test.find_one()
  if(dummy_object):
    print ("Database connected")
  else:
    print ("Connection Error")

# base route
@app.route('/')
def check():
  return "It Works!"

# register all blueprints
app.register_blueprint(mongo_api, url_prefix='/getdata')

if __name__ == '__main__':
    app.run(debug=True)