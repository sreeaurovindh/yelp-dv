from flask import jsonify
from db.Mongo import mongo

#Gets the top 5 most common attributes between the target business_id and
#  other business_ids that are within the defined radius
def get_common_attributes(business_id, radius):
    return jsonify({'targetBusiness' : business_id, 'radius': radius})