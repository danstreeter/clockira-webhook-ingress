PIPENV := $(shell command -v pipenv 2> /dev/null)

ifndef PIPENV
    $(error "Pipenv is not installed! See README.md")
endif


.PHONY: init test dev run-like-prod lint requirements pipeline-dev

export PIPENV_IGNORE_VIRTUALENVS=1
export PYTHONPATH=./src

init:
	pipenv install --dev

test:
	pipenv run pytest tests

test-coverage:
	@echo Delete all old test files
	rm -f .coverage
	rm -rf ./test-reports/htmlcov
	mkdir -p test-reports/htmlcov
	@echo "Running tests"
	pipenv run coverage run -m pytest
	# # coverage report

	@echo "Creating HTML coverage report"
	pipenv run coverage html

dev:
	FLASK_APP=main \
	FLASK_ENV=development \
	pipenv run flask run --host=0.0.0.0 --port=8998

run-like-prod:
	pipenv run gunicorn --workers=2 --threads=4 --worker-class=gthread --log-file=- main:create_app

lint:
	pipenv run pylint ./src

requirements:
	pipenv lock -r > requirements.txt

pipeline-dev:
	@echo Running What A Pipeline Would Run
	@echo Delete all old test files
	rm -f .coverage
	rm -rf ./test-reports
	mkdir -p test-reports/{flake8,htmlcov,pylint}

	@echo Running Flake8
	pipenv run flake8 ./src --exit-zero --format=html --htmldir=test-reports/flake8/

	@echo "Running pylint"
	pipenv run pylint --output-format=json ./src > test-reports/pylint/pylint.json || exit 0
	pipenv run pylint-json2html -o test-reports/pylint/pylint.html test-reports/pylint/pylint.json

	@echo "Running tests"
	PYTHONPATH=./src pipenv run coverage run -m pytest
	# # coverage report

	@echo "Creating HTML coverage report"
	pipenv run coverage html

rabbit-start:
	docker-compose -f docker-compose.yml up -d rabbitmq

rabbit-stop:
	docker-compose -f docker-compose.yml stop rabbitmq