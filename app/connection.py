import pymongo
from pymongo import MongoClient
#from flask import Flask
#app = Flask(__name__)
""" Connect to MongoDB """
client = MongoClient('localhost:27017')
print (client)
db = client['business_advisor']
customers = db['test-customers']

#if __name__ == '__main__':
#	app.debug = True
#	app.run()