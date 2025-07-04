module.exports = {
  'src/apps/backend/**/*.py': [
    'pipenv run autoflake -i',
    'pipenv run isort',
    'pipenv run black',
  ],
  'tests/**/*.py': [
    'pipenv run autoflake -i',
    'pipenv run isort',
    'pipenv run black',
  ],
  '*.{js,ts,tsx}': ['prettier --write --ignore-path .prettierignore'],
};
