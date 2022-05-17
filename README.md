# Vivanta Python Lambda Template
## Warning: Python 3.8 is used in lambdas

## Setup
Run the following at root to install all the required dependencies:

```pipenv install```

Remember we should install any further dependencies with pipenv:

```pipenv install <dependency_name>```

Also, you should add the pre-commit script to your local repo:

``` cp pre-commit-sample .git/hooks/pre-commit```

This will run unit testing and linting before each commit, ensuring all of your commits comply with our coding standards

## Testing
To run tests with Python unittests, go to the root of the project and run:

```python3 -m unittest tests/*.py```

## Linting
You can run it at the root of the project with:

```pipenv run pylint .```

## Building project for lamdas
Use this one-liner in the root of the proyect, this will create a _build with all the dependencies:

```pipenv run pip install -r <(pipenv lock -r) --target _build/```

Don't forget to add your code in (ideally, this folder name is the same as your AWS Lambda's):

```mkdir -p _build/lambda_name && cp lambda_function.py _build/lambda_name```


If you compress that file into a zip, it is possible to upload it to lambdas:

```cd _build/ && zip -r ../_build.zip ./* && cd ..```
