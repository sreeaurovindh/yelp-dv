from SolrClient import SolrClient
from textblob import TextBlob
import json

json_file_name = "D:\\Dropbox\\dv\\cusine_names\\indian.json"
json_file_out = "D:\\Dropbox\\dv\\cusine_names\\output.json"
solr = SolrClient('http://localhost:8983/solr')

# Open Output file
f = open(json_file_out, 'w')


with open(json_file_name) as json_data:
    #Load Json File
    file_jsons = json.load(json_data)
    for item in file_jsons:
        #Extract Food Item name 
        food_name = item['foodItem'].lower()
        data = '"'+food_name+'"'
        text_data=  '_text_:%s' %data
        #Consider paging query
        #Query the Solr Index
        res = solr.query('review_core',{
            'q':text_data
        })          
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
                date = review_recd['date'][0]
                useful = review_recd['useful'][0]
                funny = review_recd['funny'][0]
                try:
                    all_sentences = [sentence for sentence in review_text.lower()
                                     .split('.') if food_name in sentence]
                    polarity_sum = 0
                    for sentence in all_sentences:
                        blob = TextBlob(sentence)
                        #for sentence in blob.sentences:
                        polarity_Score = sentence.sentiment.polarity
                        polarity_sum  = polarity_sum + polarity_Score
                        
                    data = {}
                    data['item'] = food_name
                    data['polarity_avg'] = polarity_sum / len(all_sentences)
                    data['business_id'] = business_id
                    data['review_id'] = review_id
                    data['stars'] = stars
                    data['date'] = date
                    data['useful'] = useful
                    data['is_review'] = 1
                    data['is_tip'] = 0
                    
                    json_data_out = json.dumps(data)
                    f.write(json_data_out+'\n')
                            
                except:
                    pass
            
    f.close()



    
    


