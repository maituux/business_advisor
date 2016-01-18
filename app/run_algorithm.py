from flask import request, session, redirect, url_for, render_template, flash
from werkzeug import secure_filename
from app import app, connection, apriori, advice
#import logging

@app.route('/startAnalysis', methods=['GET', 'POST'])
def start_analysis():
	error=None
	if request.method == 'POST':
		if request.form.get('transactionFile'):
			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the apriori algorithm will be called.')

			if (session['userSector'] == "Bakery"): 
				filename="goods.csv"
			if (session['userSector'] == "Pharmacy"):
				filename="pharmacy.csv"

			apriori.mainAlgorithm(filename)
			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the apriori algorithm ends.')
			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the advices generation will be called.')
			advice.generate_advice()
			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the advices generation ends.')


			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the advices generation will be getted.')
			collectionName = 'Customer_'+session['userId']
			customerDB = connection.get_collection(collectionName)
			advicesDB=customerDB['Advices']
			advices = advicesDB.distinct('sentence')
		
			
			# logging.basicConfig(format='%(asctime)s %(message)s')
			# logging.warning('is when the advices  will be displayed.')
			if (session['userSector'] == "Bakery"): 
				return render_template('analysis.html', advices=advices)
			if (session['userSector'] == "Pharmacy"):
				return render_template('analysis2.html', advices=advices)
			
	

		else:
			error = 'No file selected' 
			return render_template('startAnalysis.html', error=error)
		#transaction = request.get('transactionFile'allow_multiple=True)
		#for t in transaction:
			
		#return 	redirect(url_for('analysis'))
	else:
		return render_template('startAnalysis.html')		

	#     
	#     analysisFile = 'apriori_data.csv'
	# 	flash('Successfully %s' % analysisFile)
	# 	return redirect(url_for('analysis'))
	# else:
	# 	flash('Failed to analyse %s' % analysisFile)
	# 	return redirect(url_for('startAnalysis'))	