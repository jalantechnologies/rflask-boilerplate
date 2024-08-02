run-lint:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run mypy --config-file mypy.ini .

run-vulture:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run vulture

run-engine:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run python --version \
	&& pipenv run gunicorn server:app --bind 0.0.0.0:8080 --log-level info

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
