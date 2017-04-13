from flask import jsonify
from db.Mongo import mongo

#Gets the top 5 most common attributes between the target business_id and
#  other business_ids that are within the defined radius
def get_common_attributes(business_id, radius):

    maxItems = 5

    targetBusinessAttributes = mongo.db.eval("attrOfTargetBiz('"+business_id+"')")['_batch']
    targetBusinessAttributes.sort(key=lambda x: x['count'], reverse=True)

    neighboringAttributes = mongo.db.eval("attrOfNeighborBiz('"+business_id+"', '"+radius+"')")['_batch']
    neighboringAttributes.sort(key=lambda x: x['count'], reverse=True)

    targetAttr = [o['_id'] for o in targetBusinessAttributes]
    neighborAttr = [o['_id'] for o in neighboringAttributes]

    intersect = set(targetAttr) & set(neighborAttr)

    #commonAttributes = [obj['_id'] for obj in neighboringAttributes if obj['_id'] in targetBusinessAttributes['_id']]

    prllPlotData = []

    itemCount = 0

    for attr in intersect:
        dataPoint = {}
        for item in targetBusinessAttributes:
            if(attr == item['_id']):
                dataPoint['target'] = item['polarity']
        for item in neighboringAttributes:
            if(attr == item['_id']):
                dataPoint['neighbor'] = item['polarity']
                itemCount += 1        
        dataPoint['item'] = attr

        prllPlotData.append(dataPoint)
        if itemCount >= maxItems :
            break    

    responseString = "" + str(prllPlotData)
    # responseString += "::" + (neighboringAttributes[0]['_id'])
    # responseString += "::" + (str(neighboringAttributes) + " ::::::::::" + str(targetBusinessAttributes))

    return jsonify({'targetBusiness' : business_id, 'radius': radius,'data': responseString})