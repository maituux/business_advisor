import os
import xlrd
import os.path
from xlrd import open_workbook, cellname,empty_cell
#path = "C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test"
path = os.path.expanduser("~/Desktop/business/app/test")
filename = ''
# wb = open_workbook('C:\\Users\\POLY\\Google Drive\\Desktop\\UPC\\BIP\\project\\temp\\test\\signin.xlsx')
# for sheet in wb.sheets():
# 	print 'Sheet:',sheet.name
# 	print'+++++++++++++++++++++++'
# 	print sheet.nrows
# 	print sheet.ncols
# 	print empty_cell.value
# 	print'+++++++++++++++++++++++'
	# for row in range(s.nrows):
		# values = []
		# for col in range(s.ncols):
			# values.append(s.cell(row,col).value)
		# print ','.join(values)
	
	# for row_index in range(sheet.nrows):
	# 	for col_index in range(sheet.ncols):
	# 		print cellname(row_index,col_index),'-',
	# 		print sheet.cell(row_index,col_index).value	
			#print sheet.cell_type(1,col_index),sheet.cell_value(1,col_index)
def validation(filename):
	book = open_workbook(os.path.join(path,filename))
	sheet_name = book.sheet_names()[0] #getting the sheetname of the  first sheet
	sheet = book.sheet_by_name(sheet_name)
	for r in range(0,sheet.nrows): #create a list with all row numbers that contain data and loop through it
		for c in range(0, sheet.ncols): #create a list with all column numbers that contain data and loop through i
			if sheet.cell_type(r, c) == xlrd.XL_CELL_EMPTY:
				sheet._cell_values[r][c] = 'NULL'
# for r in range(0,sheet.nrows):
#     data_column_1 = sheet.cell(r,1).value
#     print data_column_1