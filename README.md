### Example of a django rest framework project

educational

Пример учебного проекта, REST API

По заданию реализация авторизации не должна быть основана на встроенной возможности фреймворка, а организована своя.
Для аутентификации использую выдачу JWT-токенов.

1. API имеют ограничение доступа. 

Каждый пользователь может быть одной из ролей: admin, manager, basic, guest (последний - не требует авторизации, но имеет меньше всего доступа).

Реализация доступа с помощью декоратора над каждым из методов.

пример

`@require_auth_role(UserRole.BASIC)`

Либо у UserRole можно указать не BASIC, а любой из остальных.
У Админа - права на всё.

2. Есть url регистрации по уникальному юзернейму и паролю
3. Авторизация через юзернейм и пароль - равна запросу на выдачу jwt токена, который действует ограниченное время, и по которому есть доступ к другим url.
4. Каждый пользователь может "удалить" свой профиль - запись остается в базе, но -> is_active = False. После этого доступ к url по токену прекращается и новый "логин" не осуществляется.


<img width="1619" height="843" alt="image" src="https://github.com/user-attachments/assets/ab45ebeb-7d29-434e-a189-ba20b3bc6ff5" />

<img width="1619" height="920" alt="image" src="https://github.com/user-attachments/assets/d66854ab-2860-4191-8de0-f8c455d5e769" />



## Notes
```
uv venv
source .venv/bin/activate
VIRTUAL_ENV=.venv/
uv pip install ruff
uv pip list

uv add django djangorestframework

django-admin startproject myproject
python manage.py startapp api

Не называть app именем app! # for myself

делать runserver из внутренней папки


INSTALLED_APPS = [
    # ... default django apps ...
    'rest_framework',  # Add Django Rest Framework
    'api',             # Add your app
]

python manage.py makemigrations
python manage.py migrate

python manage.py migrate api zero # reverse
``


```
example of a request 

curl -X 'GET' \
  'http://0.0.0.0:8000/api/books-author/' \
  -H 'accept: application/json' \
  -d '' -H 'Authorization:bearer xxx' 

curl -X 'POST' \
  'http://0.0.0.0:8000/api/books-author/' \
  -H 'accept: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -d '
  {
  "author": {
    "name": "string"
  },
  "title": "string",
  "publish_date": "2026-01-30"
}'
  
  
  
  '{
  "author": "joe",
  "title": "123",
  "publish_date": "2026-01-30"
  
}'

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
  -H 'X-Client-Secret:xxx' \
  -d '{
  "username": "joe",
  "password": "123"
}'



curl -X 'POST' \
  'http://127.0.0.1:8000/api/edit-role' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '' -H 'Authorization:bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvZSIsImV4cGlyZSI6IjIwMjYtMDEtMzBUMTM6NDI6NDcuNDA5Njk4KzAwOjAwIiwicm9sZSI6ImFkbWluIn0.XWL-iV5jUq5Or7_jy2kI2NrN7oLv5G33ay7UvheBcDU' \
  -d '{
  "role_id": 5,
  "id": 1
}'


curl -X 'POST' \
  'http://127.0.0.1:8000/api/edit-role' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -d '{
  "role_id": 5,
  "id": 1
}'


curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/profile/1/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '' -H 'Authorization:bearer xxx' \
  -d '{
  "role_id": 5,
  "id": 1
}'

```
