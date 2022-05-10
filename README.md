## Warning: Python 3.8 is used in lambdas

## Use
Run the following at root to install all the required dependencies:
```pipenv install```

Remember we should install any further dependencies with pipenv:
```pipenv install <dependency_name>```

## Testing
To run tests with Python unittests, go to the root of the project and run:
```python3 -m unittest tests/*.py```

## Linting
You can run it at the root of the project with:
```pipenv run pylint .```

## Building project for lamdas
Use this one-liner in the root of the proyect, this will create a _build with all your code:
```pipenv run pip install -r <(pipenv lock -r) --target _build/```
If you compress that file into a zip, it is possible to upload it to lambdas:
```cd _build/ && zip -r ../_build.zip ./* && cd ..```
