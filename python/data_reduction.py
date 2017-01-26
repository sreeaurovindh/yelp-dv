from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import datetime
import ast
import json
client = MongoClient('localhost',27017)
db = client.yelp_dv




#output_businesses = db_business.find({"categories":{"$in":["Restaurants","Afghan"]}},{"business_id":1,"_id":0})
data = ["Restaurants","Afghan","African","American (New)","American (Traditional)","Arabian","Argentine","Armenian","Asian Fusion","Australian","Austrian","Bangladeshi","Barbeque","Basque","Belgian","Brasseries","Brazilian","Breakfast & Brunch","British","Buffets","Burgers","Burmese","Cafes","Cafeteria","Cajun/Creole","Cambodian","Caribbean","Catalan","Cheesesteaks","Chicken Shop","Chicken Wings","Chinese","Comfort Food","Creperies","Cuban","Czech","Delis","Diners","Dinner Theater","Ethiopian","Fast Food","Filipino","Fish & Chips","Fondue","Food Court","Food Stands","French","Gastropubs","German","Gluten-Free","Greek","Guamanian","Halal","Hawaiian","Himalayan/Nepalese","Honduran","Hong Kong Style Cafe","Hot Dogs","Hot Pot","Hungarian","Iberian","Indian","Indonesian","Irish","Italian","Japanese","Kebab","Korean","Kosher","Laotian","Latin American","Live/Raw Food","Malaysian","Mediterranean","Mexican","Middle Eastern","Modern European","Mongolian","Moroccan","New Mexican Cuisine","Nicaraguan","Noodles","Pakistani","Pan Asian","Persian/Iranian","Peruvian","Pizza","Polish","Pop-Up Restaurants","Portuguese","Poutineries","Russian","Salad","Sandwiches","Scandinavian","Scottish","Seafood","Singaporean","Slovakian","Soul Food","Soup","Southern","Spanish","Sri Lankan","Steakhouses","Supper Clubs","Sushi Bars","Syrian","Taiwanese","Tapas Bars","Tapas/Small Plates","Tex-Mex","Thai","Turkish","Ukrainian","Uzbek","Vegan","Vegetarian","Vietnamese","Waffles","Wraps"]

def select_restaurants(data):
    query_business = db.business.find({"categories":{"$in":data}},{"business_id":1,"_id":0})
    output = []
    count = 0
    for record in query_business:
        count = count + 1
        output.append(record['business_id'])
    return output

def write_selected_business(data):
    query_business_data = db.business.find({"categories":{"$in":data}},{'_id':0})
    file_business = open("D:\\Dropbox\\dv\\cleaned_data\\food_business.json","wt",encoding='utf-8')
    for business_rcd in query_business_data:
        json.dump(business_rcd,file_business)
        file_business.write('\n')
    file_business.close()

def write_selected_reviews(output):
    output_reviews = db.review.find({"business_id":{"$in":output}},{'_id':0}) 
    file_review = open("D:\\Dropbox\\dv\\cleaned_data\\food_reviews.json","wt",encoding='utf-8')
    for review_rcd in output_reviews:
        json.dump(review_rcd,file_review)
        file_review.write('\n')
        file_review.flush()
    file_review.close()
        
def write_selected_checkin(output):
    output_checkin = db.checkin.find({"business_id":{"$in":output}},{'_id':0}) 
    file_checkin = open("D:\\Dropbox\\dv\\cleaned_data\\food_checkin.json","wt",encoding='utf-8')
    for checkin_rcd in output_checkin:
        json.dump(checkin_rcd,file_checkin)
        file_checkin.write('\n')
        file_checkin.flush()
    file_checkin.close()

def write_selected_tip(output):
    output_tip = db.tip.find({"business_id":{"$in":output}},{'_id':0}) 
    file_tip = open("D:\\Dropbox\\dv\\cleaned_data\\food_tip.json","wt",encoding='utf-8')
    for tip_rcd in output_tip:
        json.dump(tip_rcd,file_tip)
        file_tip.write('\n')
        file_tip.flush()
    file_tip.close()


    
output = select_restaurants(data)
write_selected_tip(output)
#write_selected_business(data)
