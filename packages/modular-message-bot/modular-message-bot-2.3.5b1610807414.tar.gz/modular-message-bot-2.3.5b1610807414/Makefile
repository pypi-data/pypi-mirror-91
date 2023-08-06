install:
	pip install -r requirements.txt

install-dev: install
	echo "Installing DEV dependencies"
	pip install -e ".[dev]"

install-packages-apt:
	DEBIAN_FRONTEND=noninteractive apt-get update
	DEBIAN_FRONTEND=noninteractive apt-get install -y locales locales-all

lint:
	flake8 modular_message_bot/
	flake8 tests/
	black --check modular_message_bot/
	black --check tests/
	isort --check-only .

format:
	black modular_message_bot/
	black tests/
	isort .

unit:
	python -m pytest tests/unit/ -v

component:
	python -m pytest tests/component/ -v

coverage:
	coverage run -m pytest tests/unit -v
	coverage report --fail-under=100

coverage-report: coverage
	coverage report --fail-under=90
	coverage html -d build/coverage
	coverage xml -o build/coverage.xml

pygount-summary:
	pygount --suffix=py,yml --format=summary .
	pygount --suffix=py,yml --format=summary modular_message_bot/

qa: lint package-validate unit component coverage pygount-summary

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-annotate --no-emit-index-url --output-file requirements.txt setup.py

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-annotate --no-emit-index-url --output-file requirements.txt --upgrade setup.py

package-validate:
	python setup.py check

package:
	mkdir dist || true
	rm -f dist/*
	python setup.py check sdist bdist_wheel

docker:
	docker-compose build --pull

docker-shell:
	docker-compose run --user="`id -u`" --rm modular-message-bot bash
