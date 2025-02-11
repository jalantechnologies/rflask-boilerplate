module.exports = {
  //'*?(x)': () => 'npm run fmt',
  '*.{js,ts,tsx}': ['prettier --write --ignore-path .prettierignore'],
  '*.py': [
    'sh -c pipenv run autoflake -i',
    'pipenv run isort',
    'pipenv run black',
  ],
};
