#from app import app
import sys
sys.path.append('/Users/utilisateur/Desktop/business/')
from flask import session
from app import app, connection
from app.connection import db, advice_templates
import logging

def generate_advice():

	templateDB= db['advice_templates']

	#collectionName = 'Customer_568e84f322c8e50c448e07a7'
	collectionName = 'Customer_'+session['userId']
	#print (collectionName)
	
	#download the customer collection
	customerDB = connection.get_collection(collectionName)
	#print (customerDB)
	
	#access to the customer rules collection where the rules will be stored
	rulesDB=customerDB['Rules']
	advicesDB=customerDB['Advices']
	#print(advicesDB)

	logging.basicConfig(format='%(asctime)s %(message)s')
	logging.warning('is when the analyse of the pattern will be executed.')

	rulesLocation = rulesDB.find({'confidence':{ "$gt": 0.95 }})
	#rulesLocation = rulesDB.find({'confidence': 1})
	rulesPromotional = rulesDB.find({'confidence':{ "$lt": 0.95 }})

	logging.basicConfig(format='%(asctime)s %(message)s')
	logging.warning('is when the analyse of the pattern is done.')

	logging.basicConfig(format='%(asctime)s %(message)s')
	logging.warning('is when the extraction of the templates will be executed.')

	
	adviceLocation = advice_templates.find({'name':'placement'})
	for a in adviceLocation:
		adviceTxt1= a.get("txt")

	advicePromotional = advice_templates.find({'name':'promotional'})
	for a in advicePromotional:
		adviceTxt2= a.get("txt")


	for rule in rulesLocation:
		logging.basicConfig(format='%(asctime)s %(message)s')
		logging.warning('is when the generation of the advice will start.')
		productTxt = 'The products '+str(rule.get("explained product"))+ ' and '+ str(rule.get("explaining product"))+' are frequently bought together.'
		#resAdvice = create_placement_advice(productTxt)
		resAdvice = productTxt+ '\n'+ adviceTxt1+ '\n\n\n'
		logging.basicConfig(format='%(asctime)s %(message)s')
		logging.warning('is when the advice is generated.')
		logging.basicConfig(format='%(asctime)s %(message)s')
		logging.warning('is when the advice will be stored.')
		newAdvice = {'sentence': resAdvice, 'type': 'placement'}
		logging.basicConfig(format='%(asctime)s %(message)s')
		logging.warning('is when the advice is stored.')
		advicesDB.insert(newAdvice)
		#print(resAdvice)

	for rule in rulesPromotional:
		productTxt = 'The products '+str(rule.get("explained product"))+ ' and '+ str(rule.get("explaining product"))+' are frequently bought together.'
		resAdvice = productTxt+ '\n'+ adviceTxt2+ '\n\n\n'
		# resAdvice = create_promotional_advice(productTxt)
		newAdvice = {'sentence': resAdvice, 'type': 'promotional'}
		advicesDB.insert(newAdvice)
		print(resAdvice)

	logging.basicConfig(format='%(asctime)s %(message)s')
	logging.warning('is when the advices have been generated and stored.')

# def get_placement_advice():
# 	adviceLocation = advice_templates.find({'name':'placement'})
# 	for a in adviceLocation:
# 	 	adviceTxt2= a.get("txt")
# 	 return adviceTxt2

# def get_promotional_advice():
# 	advicePromotional = advice_templates.find({'name':'promotional'})
# 	for a in advicePromotional:
# 		adviceTxt1= a.get("txt")
# 	return adviceTxt1

# def create_placement_advice(txt1):
# 	txt2 = get_placement_advice()
# 	resAdvice = txt1+ '\n'+ txt2+ '\n\n\n'
# 	return resAdvice

# def create_promotional_advice(txt1):
# 	txt2 = get_promotional_advice()
# 	resAdvice = txt1+ '\n'+ txt2+ '\n\n\n'
# 	return resAdvice
	
if __name__ == '__main__':
	generate_advice()