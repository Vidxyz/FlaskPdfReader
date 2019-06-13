import os
from flask import Flask
from flask import request
import PyPDF2 as pdf_extracter
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## Accepts a PDF file as post request. PDF file is then processed, and all words are extracted
## 5 most common words are determined for the inbound file
## A database entry is then made that contains at the minimum (FileName, TimeOfUpload, FiveMostCommonWords)
@app.route('/upload-file', methods=['GET', 'POST'])
def process_file():
	if request.method == 'GET':
		return 'Invalid Request Method. Expected POST request!\n'
	else:
		# Do processing here
		# Overview of steps
		# 1. Initialize database - if database schema already exists, then re-use it
		# 2. Save pdf file to temp storage 
		# 3. Process contents of PDF file. Assumption here is that it is only textual data
		#    3.1 - Solution can be extended to further pdf formats with images, would require 
		#		   more powerful processing libraries
		# 4. Go through each word extracted, and repeatedly compute the most commonly occuring words
		# 5. Store results in database
		#    5.1 - Assumption here is made that an inbound file with already existing filename in DB is overwritten
		# 6. Delete temporary file from storage
		# 7. Return success response

		pdf_file = request.files['pdf_file']
		print('PDF file received with filename ' + secure_filename(pdf_file.filename))
		pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf_file.filename))
		print('PDF save path is ' + pdf_path)
		pdf_file.save(pdf_path)
		
		pdf_obj = open(pdf_path, 'rb')
		pdf_reader = pdf_extracter.PdfFileReader(pdf_obj)

		# Make sure to catch exceptions over here
		if pdf_reader.isEncrypted:
			pdf_reader.decrypt('')

		print('Number of pages = ' + str(pdf_reader.numPages) + '\n')

		for i in range(pdf_reader.numPages):
			page_object = pdf_reader.getPage(i)
			lines_of_text = page_object.extractText()
			print(lines_of_text)
			

		# Must delete PDF file after processing contents
		os.remove(pdf_path)
		return 'Hello, World!\n' 



## Makes database call tgo query information previously inserted via process_file()
## Returns at the very least, the name of file, time of upload and the 5 most common words for 
## all previously uploaded PDF's
@app.route('/get-common-words')
def get_common_words():
	if request.method == 'GET':
		return 'Hello, World!\n'
   	else: 
		return 'Hello, World!\n'