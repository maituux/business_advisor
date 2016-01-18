import pymongo
from pymongo import MongoClient

#app = Flask(__name__)
""" Connect to MongoDB """
client = MongoClient('localhost:27017')
print (client)
db = client['business_advisor']
customers = db['customers']
advice_templates = db['advice_templates']

def get_collection(collection):
    coll = db[collection]
    return coll
#if __name__ == '__main__':
#	app.debug = True
#	app.run()