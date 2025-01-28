run-lint:
	cd src/apps/backend \
		&& pipenv run mypy --config-file mypy.ini .

run-format:
	cd src/apps/backend \
		&& pipenv run autoflake . -i \
		&& pipenv run isort . \
		&& pipenv run black .

run-vulture:
	cd src/apps/backend \
		&& pipenv run vulture

run-engine:
	cd src/apps/backend \
		&& pipenv run python --version \
		&& pipenv run gunicorn -c gunicorn_config.py --reload server:app

run-test:
	PYTHONPATH=src/apps/backend pipenv run pytest tests

run-engine-winx86:
	echo "This command is specifically for Windows platform \
	since gunicorn is not well supported by Windows OS"
	cd src/apps/backend \
		&& pipenv run waitress-serve --listen 127.0.0.1:8080 server:app

run-script:
	cd src/apps/backend && \
		PYTHONPATH=./ pipenv run python scripts/$(file).py

