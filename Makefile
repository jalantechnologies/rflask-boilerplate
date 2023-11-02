run-lint:
	cd src/apps/backend && pipenv run mypy --config-file mypy.ini .

run-vulture:
	cd src/apps/backend && pipenv run vulture

