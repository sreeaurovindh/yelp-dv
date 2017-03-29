# Yelp Backend for API's (Flask)

###Steps to configure:  
* 1. Install and setup __python3__, __virtualenv__ and __mongodb__ as prerequisite.  
* 2. Create a __test__ collection in mongodb for the yelp backend service to test for db connection. (one time)  
* 2. __virtualenv__ can be installed using `pip install virtualenv` (one time)  
* 2. Clone the repo  
* 3. Goto yelp/yelp-flask  
* 4. Run `virtualenv env` (one time)  
* 5. Run `source env/bin/activate`  
* 5. Run `pip install flask`  
* 6. Start the service using `python app.py`  


###API's Used  
__Base URL:__  
http://localhost:5000/  

__Get all collection names in yelp:__  
http://localhost:5000/collections  

__Get all data from the given collection:__  
http://localhost:5000/collection/<coll>  
http://localhost:5000/collection/dummy  

__Get limited data from the given collection:__  
http://localhost:5000/collection/<coll>/limit/<limit>  
http://localhost:5000/collection/dummy/limit/50  



Info:
Refer [Introduction to MongoDB using Pymongo](http://altons.github.io/python/2013/01/21/gentle-introduction-to-mongodb-using-pymongo/) for using mongo calls in PyMongo.