import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from python_lambda_template.code import lambda_function

class TestLambdaResponse(unittest.TestCase):
    def test_lambda_ok_response(self):
        self.assertEqual(lambda_function.lambda_handler(1, 2)['statusCode'], 200)