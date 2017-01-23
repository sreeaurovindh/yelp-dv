# Function reads all json files
import json
import csv

review_file = 'D:\\Dropbox\\dv\\yelp_dataset_challenge_academic_dataset\\yelp_academic_dataset_review.json'

# Single line of review file looks like this

#{'type': 'review', 'stars': 4, 'review_id': 'Ya85v4eqdd6k9Od8HbQjyA', 'business_id': '5UmKMjUEUNdYWqANhGckJw', 'text': 'Mr Hoagie is an institution. Walking in, it does seem like a throwback to 30 years ago, old fashioned menu board', 'date': '2012-08-01', 'user_id': 'PUFPaY9KxDAcGqfsorJp3Q', 'votes': {'funny': 0, 'useful': 0, 'cool': 0}}


output_file = open('D:\\Dropbox\\dv\\yelp_cleaned\\review.csv','wt',encoding='utf-8')

i = 0
with open(review_file) as fp:
   writer = csv.writer(output_file, lineterminator='\n')
   writer.writerow(("id","type_str","stars","review_id","business_id","text","date_str","user_id","votes_funny","votes_useful","votes_cool"))
   for line in fp:
      resp = json.loads(line)
      type_str = resp['type']
      stars = resp['stars']
      review_id = resp['review_id']
      business_id = resp['business_id']
      text = resp['text'].replace(","," ").replace('\n',' ').replace('  ',' ').replace("'", "\\\'").replace('"', "'")

      date_str = resp['date']
      user_id = resp['user_id']
      votes_funny = resp['votes']['funny']
      votes_useful = resp['votes']['useful']
      votes_cool = resp['votes']['cool']
      writer = csv.writer(output_file, lineterminator='\n')
      writer.writerow((i,type_str,stars,review_id,business_id,text,date_str,user_id,votes_funny,votes_useful,votes_cool))
      i += 1
   output_file.close()
      