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
