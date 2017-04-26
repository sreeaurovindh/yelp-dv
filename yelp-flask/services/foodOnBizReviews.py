from db.Mongo import mongo
from flask import jsonify


def getTargetBizChart(bizId):
    print(bizId)
    targetBizData = mongo.db.eval("targetBizChart('"+bizId+"')")
    return jsonify(targetBizData)

def getNeighboringBizChart(bizId,radius):
    print(bizId,radius)
    neighborhoodBizData = mongo.db.eval("neighborhood_props('"+bizId+"', '"+radius+"')")
    return jsonify(neighborhoodBizData['_batch'])

def getFoodItems(bizId, radius, startDate1, endDate2):
    print(bizId, radius, startDate1, endDate2)
    bubbleChartData = mongo.db.eval("foodItemsChart('"+bizId+"', '"+radius+"', '"+startDate1+"', '"+endDate2+"')")
    return jsonify(bubbleChartData)