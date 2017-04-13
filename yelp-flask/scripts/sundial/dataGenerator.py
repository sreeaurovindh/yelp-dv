from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import jsonify

client = MongoClient('mongodb://localhost:27017/')
mongo = client['yelp']

def getData():

  collection = []
  colors = ['#E3170A', '#A9E5BB', '#FCF6B1', '#F7B32B', '#2D1E2F', '#3C1642', '#086375', '#1DD3B0', '#AFFC41', '#320D6D', '#B2FF9E', 
  '#FFBFB7', '#FFD447', '#700353', '#4C1C00', '#003049', '#D62828', '#F77F00', '#FCBF49', '#EAE2B7', '#09BC8A', '#008DD5']
  i = 0


  business_list = list(mongo.foodbusiness.aggregate(
	[
    {
			'$unwind': {
			    'path' : "$categories"
			}
		},
		{
			'$group': {
			    '_id': {
			        'state': '$state',
			        'city': '$city',
			    },
			    'categories': { '$addToSet': '$categories' } 
			}
		},
		{
			'$group': {
			    '_id': {
			        'state': '$_id.state'
			    },
			    'cities': { '$addToSet': { 'city': '$_id.city', 'category':'$categories' } }
			}
		},
	]
  ))

  print(business_list)

  for business in business_list:
    state = { 'name' : business['_id']['state'], 'color':colors[clamp(i)], 'children' : [] }
    collection.append(state)
    for cities in business['cities']:
      city = { 'name' : cities['city'], 'color':colors[clamp(i)], 'children' : [] }
      state['children'].append(city)
      for categories in cities['category']:
        category = { 'name' : categories , 'color':colors[clamp(i)] }
        city['children'].append(category)

  #print(collection)


def clamp(x): 
  x += 1
  return max(0, min(x, 21))

getData()
print('\n\n')