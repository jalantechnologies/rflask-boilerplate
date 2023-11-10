run-lint:
	cd src/apps/backend && pipenv run mypy --config-file mypy.ini .

run-vulture:
	cd src/apps/backend && pipenv run vulture

run-engine:
	cd src/apps/backend && pipenv install --dev && pipenv install
	cd src/apps/backend && pipenv run gunicorn server:app --bind 0.0.0.0:8080 --workers=4 --log-level info --reload

test:
	cd src/apps/backend && pipenv run pytest tests
