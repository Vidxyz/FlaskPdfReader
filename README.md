# FlaskPdfReader

Simple Flask App that reads a PDF and summarizes contents

## Steps to run

### Clone the repository
```
git clone https://github.com/Vidxyz/FlaskPdfReader.git
cd FlaskPdfReader
```

### Create a virtualenv and activate it:
Note, this project uses python 2.7 and SQLite 

```
virtualenv venv
. venv/bin/activate
```

### Install FlaskPdfReader:
```
pip install -e .
pip install -r requirements.txt
````

### Run
```
export FLASK_APP=flaskpdfreader
export FLASK_ENV=development
flask run
```

### Initialize DB
Open a new terminal instance
```
flask init-db
```

You should see the following

`Initialized the database.`

### Use
Open `http://localhost:5000/` in your browser

You should see the following

`Hello, World!`

### POST request
```
curl -X POST -F 'pdf_file=@current_folder/test_document.pdf' http://localhost:5000/upload-file
```

### GET request
```
curl -X GET http://localhost:5000/get-common-words
```

Test
pip install '.[test]'
pytest
Run with coverage report:

coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
