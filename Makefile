run:
	python3 auth_project/manage.py runserver

format:
	uv run ruff format .
	uv run ruff check --fix .

req:
	uv export --no-hashes --format requirements-txt --output-file ./requirements.txt