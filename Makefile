.PHONY: format lint test install help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies (dev + production)"
	@echo "  make format     - Auto-format code with black and isort"
	@echo "  make lint       - Run linters (flake8, black check, isort check, pylint)"
	@echo "  make test       - Run Django tests"
	@echo "  make migrate    - Run Django migrations"
	@echo "  make run        - Run Django development server"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

format:
	@echo "Running black..."
	black hw_checker/
	@echo "Running isort..."
	isort --profile black hw_checker/
	@echo "✓ Code formatting complete!"

lint:
	@echo "Running flake8..."
	flake8 hw_checker/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 hw_checker/ --count --max-complexity=10 --max-line-length=127 --statistics
	@echo "Running black (check mode)..."
	black --check hw_checker/
	@echo "Running isort (check mode)..."
	isort --check-only --profile black hw_checker/
	@echo "Running pylint..."
	pylint hw_checker/assignments/ --disable=C0114,C0115,C0116,R0903 --max-line-length=127
	@echo "✓ All linters passed!"

test:
	cd hw_checker && python manage.py test --verbosity=2

migrate:
	cd hw_checker && python manage.py migrate

run:
	cd hw_checker && python manage.py runserver

