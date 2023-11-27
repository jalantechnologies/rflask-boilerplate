run-lint:
	cd src/apps/backend && pipenv install && pipenv run mypy --config-file mypy.ini .

run-vulture:
	cd src/apps/backend && pipenv install && pipenv run vulture

run-engine:
	cd src/apps/backend && pipenv install --dev && pipenv install
	cd src/apps/backend && pipenv run gunicorn server:app --bind 0.0.0.0:8080 --workers=4 --log-level info --reload

run-test:
	cd src/apps/backend && pipenv install && pipenv run pytest tests

run-engine-winx86:
	echo "This command is specifically for windows platform \
	sincas gunicorn is not well supported by windows os"
	cd src/apps/backend && pipenv install --dev && pipenv install
	cd src/apps/backend && pipenv run waitress-serve --listen 0.0.0.0:8080 server:app
