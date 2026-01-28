Example of a django rest framework project
educational

```
uv venv
source .venv/bin/activate
VIRTUAL_ENV=.venv/
uv pip install ruff
uv pip list

uv add django djangorestframework

django-admin startproject myproject
python manage.py startapp api

Не называть app именем app!

делать runserver из внутренней папки


INSTALLED_APPS = [
    # ... default django apps ...
    'rest_framework',  # Add Django Rest Framework
    'api',             # Add your app
]

python manage.py makemigrations
python manage.py migrate
```

```
example of a request 

curl -X 'GET' \
  'http://0.0.0.0:8000/api/books-author/' \
  -H 'accept: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -H 'X-Client-Secret:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvZSIsImV4cGlyZSI6IjIwMjYtMDEtMjhUMDY6NTk6MzQuMTUyNzM1KzAwOjAwIiwicm9sZSI6ImJhc2ljIn0.VIBOe74-rq56_aflBrTWnC4sJufcTAE0iTAG1ofNAT8'


curl -X 'POST' \
  'http://0.0.0.0:8000/api/token/check?username=joe&password=123' \
  -H 'accept: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -H 'X-Client-Secret:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvZSIsImV4cGlyZSI6IjIwMjYtMDEtMjdUMTU6MzA6MzMuNjQxODk0KzAwOjAwIn0.LZKUJAXvbJBmV6lwxDCRjLLsc8nZea9Aa5Xxylmyfkg'

curl -X 'POST' \
  'http://127.0.0.1:8000/api/token/gen' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: 86ChJcJ8ywmz6fKsWNhUFQNssTok7P5Y' \
  -d '{
  "username": "joe",
  "password": "123"
}'

curl -X 'POST' 'http://0.0.0.0:8000/v1/?username=joe&password=123'
# Get username and password from query parameters
# username = request.query_params.get('username')
# password = request.query_params.get('password')

get username and password from body in view
username = request.data.get("username")
password = request.data.get("password")



curl -X 'POST' \
  'http://127.0.0.1:8000/api/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: 86ChJcJ8ywmz6fKsWNhUFQNssTok7P5Y' \
  -d '{
  "username": "joe",
  "password": "123"
}'

```