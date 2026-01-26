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
  -H 'X-Client-Secret:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvZSIsImV4cGlyZSI6IjIwMjUtMDEtMjRUMTQ6Mjg6MDMuMDM2NzI0KzAwOjAwIn0.GTphQVoUy6eBX14hx2UPXv6-4u4tbrgUEWLEHXGLFho'
```


curl -X 'POST' \
  'http://0.0.0.0:8000/api/token/check?username=joe&password=123' \
  -H 'accept: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -H 'client_secret:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvZSIsImV4cGlyZSI6IjIwMjUtMDEtMjRUMTQ6Mjg6MDMuMDM2NzI0KzAwOjAwIn0.GTphQVoUy6eBX14hx2UPXv6-4u4tbrgUEWLEHXGLFho'
```


curl -X 'POST' 'http://0.0.0.0:8000/v1/?username=joe&password=123'
# Get username and password from query parameters
# username = request.query_params.get('username')
# password = request.query_params.get('password')

```