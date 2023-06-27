import json
from code.helpers.test_data_generator import TestDataGenerator
from code.schemas.customer import Customer
import os
import subprocess

ENVIRONMENT_FILE_PATH = "files/environments/collection.json"
COLLECTION_FILE = "files/collections/VivantaAPI1.1.postman_collection.json"
def lambda_handler(event, context): # pylint: disable=unused-argument
    customer = Customer(event['customerId'], event['customerKey'])
    tests_data_generator = TestDataGenerator(event['brandId'], event['ids'], customer)
    tests_data_generator.generate_testing_data()
    tests_data_generator.write_testing_data(ENVIRONMENT_FILE_PATH)
    # Construct the Newman command
    command = f"newman run {COLLECTION_FILE} -e {ENVIRONMENT_FILE_PATH}"

    # Execute the command using subprocess
    subprocess.run(command, shell=True)

    return {
        'statusCode': 200,
        'body': 'testData'
    }
