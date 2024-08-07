run-lint:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run mypy --config-file mypy.ini .

run-format:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run autoflake . -i \
	&& pipenv run isort . \
	&& pipenv run black .

run-vulture:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run vulture

run-engine:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run python --version \
	&& pipenv run gunicorn -c gunicorn_config.py server:app

run-test:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run pytest tests

run-engine-winx86:
	echo "This command is specifically for windows platform \
	sincas gunicorn is not well supported by windows os"
	cd src/apps/backend \
	&& pipenv install --dev && pipenv install \
	&& pipenv run waitress-serve --listen 127.0.0.1:8080 server:app

run-script:
	cd src/apps/backend && \
	pipenv install --dev && \
	pipenv run python scripts/$(file).py
