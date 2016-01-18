import csv
import os
from os import path
import sys
sys.path.append('/Users/utilisateur/Desktop/business/')
#sys.path.append("C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test")
from app import app
from app.connection import db
import logging

def prepare_data(customerDB):
	# logging.basicConfig(format='%(asctime)s %(message)s')
	# logging.warning('is when the input data for the apriori algorithm will be extracted.')
	transactions = customerDB['Transactions']
	transactionsId = transactions.distinct('Transaction number')
	print transactionsId
	#print transactionsId
	# logging.basicConfig(format='%(asctime)s %(message)s')
	# logging.warning('is when the input data for the apriori algorithm are extracted.')

	# logging.basicConfig(format='%(asctime)s %(message)s')
	# logging.warning('is when the input data will be transformed.')

	
	with open('apriori_data.csv', 'wb') as csvfile:
		for i in transactionsId:
			if i==u'': 
				continue
			if isinstance(i, int):
				x= i
			else:
				x = int(i)

			products=transactions.find({"Transaction number": x})
			writer = csv.writer(csvfile, delimiter=',')
			row=[x]
			print "@@@@@@@@@@@@@@@@@@@@@@"
			for product in products:
				getProductId= int(product.get("Product ID"))
				if isinstance(getProductId, int):
					productId= getProductId
				else:
					productId = int(getProductId)
				
				row.insert(len(row), productId)
			#print(row)
			writer.writerow(row)
	# logging.basicConfig(format='%(asctime)s %(message)s')
	# logging.warning('is when the input data has been transformed.')
	csvfile.close()
	print ('data ready')

