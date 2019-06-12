from flask import Flask

app = Flask(__name__)

## Accepts a PDF file as post request. PDF file is then processed, and all words are extracted
## 5 most common words are determined for the inbound file
## A database entry is then made that contains at the minimum (FileName, TimeOfUpload, FiveMostCommonWords)
@app.route('/upload-file', methods=['GET', 'POST'])
def process_file():
	if(request.method == 'GET'):
    	return 'Hello, World!'
    else:
    	# Do processing here
    	return 'Hello, World!'



## Makes database call tgo query information previously inserted via process_file()
## Returns at the very least, the name of file, time of upload and the 5 most common words for 
## all previously uploaded PDF's
@app.route('/get-common-words')
def process_file():
	if(request.method == 'GET'):
    	return 'Hello, World!'
    else:
    	# Do processing here
    	return 'Hello, World!'