run:
	python3 auth_project/manage.py runserver

db:
	python3 auth_project/manage.py makemigrations
	python3 auth_project/manage.py migrate

format:
	uv run ruff format .
	uv run ruff check --fix .

req:
	uv export --no-hashes --format requirements-txt --output-file ./requirements.txt

test:
	pytest auth_project/