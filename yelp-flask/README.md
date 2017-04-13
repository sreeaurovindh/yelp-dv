# Yelp Backend for API's (Flask)

### Steps to configure:  
* Install and setup __python3__, __virtualenv__ and __mongodb__ as prerequisite.  
* In mongodb, create an __yelp__ database and __test__ collection for the yelp backend service to test for db connection. (one time)  
* __virtualenv__ can be installed using `pip install virtualenv` (one time)  
* Clone the repo  
* Goto yelp/yelp-flask  
* Run `virtualenv env` (one time)  
* Run `source env/bin/activate`. (Type `deactivate` for come out of the virtual envirionment)  
* Run `pip install flask`  
* Run `pip install Flask-PyMongo`
* Run `pip install -U flask-cors`
* Start the service using `python app.py`  


### API's Used  
__Base URL:__  
http://localhost:5000/  

__Get all collection names in yelp:__  
http://localhost:5000/collections  

__Get all data from the given collection:__  
http://localhost:5000/collection/<coll\>  
http://localhost:5000/collection/dummy  

__Get limited data from the given collection:__  
http://localhost:5000/collection/<coll\>/limit/\<limit\>  
http://localhost:5000/collection/dummy/limit/50  



__Info:__
Refer [Introduction to MongoDB using Pymongo](http://altons.github.io/python/2013/01/21/gentle-introduction-to-mongodb-using-pymongo/) for using mongo calls in PyMongo.
