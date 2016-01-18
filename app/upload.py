import os
import json
import xlrd
from app import parse
from app import notify
from app import validate
import os.path
from xlrd import open_workbook
from flask import Flask, request, redirect, url_for,render_template, flash, session
from werkzeug import secure_filename
from app import app, connection
from .connection import db
import logging

# import pymongo
# from pymongo import MongoClient

# customerConnection = MongoClient('localhost:27017')
# db_ba = customerConnection['business_advisor']
# customerDB = db_ba['Customer_'+session['userId']]
#UPLOAD_FOLDER = os.path.expanduser("~/Desktop/gitBA/business_advisor/app/test")
#The file formats that are acceptable for upload
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

#check that the uploaded file is in the right format in our case .xls or .xlsx.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


###########
#We then mapped the URL / to the function home(). Now, when someone visits this URL, the function home() will execute. 

	
# Python function finds a web template living in the templates/ folder.
#A web template will look in the static/ folder for any images, CSS, or JavaScript files it needs as it renders to HTML
#Rendered HTML is sent back to uploadtemp.py
#routes.py sends the HTML back to the browser	


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		# logging.basicConfig(format='%(asctime)s %(message)s')
		# logging.warning('is when the check file has to start.')
		if file and allowed_file(file.filename):
			
			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the check file is done.')
			
			filename = secure_filename(file.filename)
					
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is the cleaning of data has to start.')
			validate.validation(filename)
			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the cleaning of data is done.')
			
			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the parsing process has to start (transform to JSON).')
			json_filename = parse.parse_file(filename)
			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the parsing process (transform to JSON) is done.')
			
			print(session['userId'])
			
			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the data storage process has to start.')
			
			collectionName = "Customer_"+session['userId']
			customerDB = connection.get_collection(collectionName)
			transactionsDB=customerDB['Transactions']
			print(transactionsDB)
			input_file = open(json_filename)
			for line in input_file:
				transactionsDB.insert(json.loads(line))
			flash('Successfully uploaded %s' % filename)

			logging.basicConfig(format='%(asctime)s %(message)s')
			logging.warning('is when the data storage process is done.')
			return redirect(url_for('upload_file'))
		else:
			flash('Invalid file %s' % file.filename)
			return redirect(url_for('upload_file'))
	else:
		files = notify.get_files(app.config['UPLOAD_FOLDER'])
		return render_template('upload.html', files=files)
		return redirect(url_for('upload_file'))
						
if __name__ == '__main__':
 	app.debug = True
	app.run()
