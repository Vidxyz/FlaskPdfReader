import os, operator, collections, sys, re
import PyPDF2 as pdf_extracter
from werkzeug.utils import secure_filename
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskpdfreader.db import get_db

bp = Blueprint('pdf_reader', __name__)

SQL_PDF_INSERT = 'INSERT INTO PDF(filename) VALUES (?) '
SQL_PDFSTATS_INSERT = 'INSERT INTO PDFSTATS(pdf_id, rank, word) VALUES (?, ?, ?) '
SQL_FETCH_LAST_ROWID = 'SELECT last_insert_rowid()'
SQL_PDFSTATS_VIEW   = 'SELECT p.id, p.filename, p.created, s.rank, s.word from PDF p, PDFSTATS s WHERE p.id = s.pdf_id'



word_black_list = [',', '.', '!', '?', '"', ':', ';']



# Todo: Unit tests
def sanitize_stats(stats):

	cleaned_stats = []
	word_list_acc = []

	if(len(stats) == 0):
		return cleaned_stats

	cur_index = stats[0][0]
	
	for i in range(len(stats)):
		if stats[i][0] != cur_index:
			cur_index = stats[i][0];
			# Index has changed. We have to update stats
			cleaned_stats.append([stats[i-1][1], stats[i-1][2], word_list_acc])
			word_list_acc = []

		word_list_acc.append((stats[i][4], stats[i][3]))


	# Append last set of stats
	cleaned_stats.append([stats[len(stats) - 1][1], stats[len(stats) - 1][2], word_list_acc])
	return cleaned_stats


# Todo: Unit tests
def make_json(stats):
	json_list = []

	if(len(stats) == 0):
		return json_list

	for each in stats:
		stat_dict = {}
		stat_dict['filename'] = each[0]
		stat_dict['timestamp'] = each[1]
		most_common_list = []
		
		for entry in each[2]:
			word_pair = {}
			word_pair['word'] = entry[0]
			word_pair['count'] = entry[1]
			most_common_list.append(word_pair)

		stat_dict['most_common_words'] = most_common_list
		json_list.append(stat_dict)

	return json_list

## Accepts a PDF file as post request. PDF file is then processed, and all words are extracted
## 5 most common words are determined for the inbound file
## A database entry is then made that contains at the minimum (FileName, TimeOfUpload, FiveMostCommonWords)
from flask import current_app as app
@bp.route('/upload-file', methods=['GET', 'POST'])
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
		pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf_file.filename))
		
		app.logger.info('PDF file received with filename ' + secure_filename(pdf_file.filename))
		app.logger.info('PDF save path is ' + pdf_path)
		pdf_file.save(pdf_path)
		
		pdf_obj = open(pdf_path, 'rb')
		pdf_reader = pdf_extracter.PdfFileReader(pdf_obj)

		# Make sure to catch exceptions over here
		if pdf_reader.isEncrypted:
			pdf_reader.decrypt('')

		app.logger.info('Number of pages = ' + str(pdf_reader.numPages))


		# Do calculation of common words here
		frequency_list = []
		complete_lines_of_text = ''
		
		for i in range(pdf_reader.numPages):
			page_object = pdf_reader.getPage(i)
			lines_of_text = page_object.extractText().lower()
			complete_lines_of_text = complete_lines_of_text + lines_of_text


		# Separate all the text into words
		words_of_text = re.findall(r"[\w']+|[.,!?;]", complete_lines_of_text)
		words = collections.Counter(words_of_text)

		for word in list(words):
			if word in word_black_list:
				del words[word]

		frequency_list = list(words.most_common(5))
		app.logger.info('Frequency List')
		app.logger.info(frequency_list)


		error = None
		if not pdf_file:
			error = 'Error: PDF File required\n'

		if len(words_of_text) == 0:
			error = 'Error: PDF File empty!\n'



		if error is not None:
			os.remove(pdf_path)
			return error;

		else:
			db = get_db()
			# Insert into PDF table
			db.execute(SQL_PDF_INSERT, (secure_filename(pdf_file.filename), ))
			current_id = db.execute(SQL_FETCH_LAST_ROWID).fetchall()[0][0]
			# Insert into PDFSTATS table
			for pair in frequency_list:
				db.execute(SQL_PDFSTATS_INSERT, (current_id, pair[1], pair[0]))

			# db.execute()
			db.commit()

		# Must delete PDF file after processing contents
		os.remove(pdf_path)
		return 'PDF Save successful!!\n' 


## Makes database call tgo query information previously inserted via process_file()
## Returns at the very least, the name of file, time of upload and the 5 most common words for 
## all previously uploaded PDF's
@bp.route('/get-common-words')
def get_common_words():
	if request.method == 'GET':
		
		db = get_db()

		stats = db.execute(SQL_PDFSTATS_VIEW).fetchall()

		for entry in stats:
			print entry

		cleaned_stats = sanitize_stats(stats)		
		json_stats = make_json(cleaned_stats)

		return jsonify(json_stats)

   	else: 
		return 'Invalid Request Method. Expected GET request!\n'