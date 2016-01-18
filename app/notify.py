import os
import os.path
from flask import Flask


#where we find the uploaded files(use double slash to avoid the IOError22: invalid filename)
# path =  'C:\\Users\\POLY\\Google Drive\\Desktop\\UPC\\BIP\\project\\temp\\test\\*.'
#path =  'C:\\Users\\POLY\\Google Drive\\Desktop\\UPC\\BIP\\project\\temp\\test'
path = "C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test"
#this method will get all the files uploaded fron the temporary folder and display them on the browser
def get_files(path):
	files = os.listdir(path)
	files_list = [i for i in files if i.endswith(('.xlsx', '.xls'))]
	return files_list
#other implementation
# def get_files(path):
# 	value = [fn for fn in os.listdir(path) if fn.endswith(('.xlsx', '.xls'))]
# 	print value
# 	return value

