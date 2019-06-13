# FlaskPdfReader

Simple Flask App that reads a PDF and summarizes contents

## Steps to run

# clone the repository
```
git clone https://github.com/Vidxyz/FlaskPdfReader.git
cd FlaskPdfReader
```

Create a virtualenv and activate it:
Note, this project uses python=2.7

```
virtualenv venv
. venv/bin/activate
```

Install FlaskPdfReader:
`pip install -e .`
`pip install -r requirements.txt`

Run
```
export FLASK_APP=flaskpdfreader
export FLASK_ENV=development
flask run
```

Open http://127.0.0.1:5000 in a browser.

Test
pip install '.[test]'
pytest
Run with coverage report:

coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
