from SolrClient import SolrClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#Imported by easy_install vaderSentiment
#Obtained from https://github.com/cjhutto/vaderSentiment
import json
import iso8601
from pymongo import MongoClient

json_file_name = "D:\\Dropbox\\dv\\cusine_names\\indian.json"
json_file_out = "D:\\Dropbox\\dv\\cusine_names\\output_dates.json"
solr = SolrClient('http://localhost:8983/solr')

#Mongodb connection Parameters
client = MongoClient('mongodb://localhost:27017/')
db = client['yelp_dv']
food_business = db.food_business

# Open Output file
f = open(json_file_out, 'w')

analyzer = SentimentIntensityAnalyzer()

with open(json_file_name) as json_data:
    #Load Json File
    file_jsons = json.load(json_data)
    for item in file_jsons:
        #Extract Food Item name 
        food_name = item['foodItem'].lower()
        data = '"'+food_name+'"'
        text_data=  '_text_:%s' %data
        #Query the Solr Index
        for res in  solr.paging_query('review_core',{'q':text_data},rows=10000):
        #Get all values of Review Record
            if res.get_results_count() > 0:
                print(food_name,res.get_results_count())
                
                json_doc = json.loads(res.get_json())
                output = json_doc['response']['docs']
                for review_recd in output:
                    review_text = review_recd['text'][0]
                    business_id = review_recd['business_id'][0]
                    review_id = review_recd['review_id'][0]
                    stars = review_recd['stars'][0]
                    timestamp_str = review_recd['date'][0]
                    useful = review_recd['useful'][0]
                    funny = review_recd['funny'][0]
                    try:
                        all_sentences = [sentence for sentence in review_text.lower()
                                         .split('.') if food_name in sentence]
                        if len(all_sentences) == 0:
                            all_sentences = [review_text]
                            
                        max_polarity = -2
                        sentence_review = ""
                        for sentence in all_sentences:
                            vs = analyzer.polarity_scores(sentence)
                            polarity_Score = vs['compound']
                            if polarity_Score > max_polarity:
                                max_polarity = polarity_Score
                            sentence_review = sentence_review + sentence
                            
                        #Get Business Name from business ID
                        business_name=food_business.find_one({"business_id":business_id })['name']
                        
                
                        #print(polarity_Score,max_polarity)   
                        data = {}
                        data['item'] = food_name
                        data['polarity'] = max_polarity
                        data['business_id'] = business_id
                        data['review_id'] = review_id
                        data['stars'] = stars
                        data['date']  = iso8601.parse_date(timestamp_str).strftime('%Y-%m-%d')
                        data['useful'] = useful
                        data['is_review'] = 1
                        data['is_tip'] = 0
                        data['name'] = business_name
                        data['review_sentence'] = all_sentences[0]
                        
                        json_data_out = json.dumps(data)
                        f.write(json_data_out+'\n')
                                
                    except Exception as e:
                        print(e)
                        pass
            
    f.close()



    
    


