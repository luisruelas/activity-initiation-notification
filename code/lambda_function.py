from code.helpers.test_data_generator import TestDataGenerator
from code.schemas.customer import Customer
import json

def lambda_handler(event, context): # pylint: disable=unused-argument
    customer = Customer(event['customerId'], event['customerKey'])
    testData = TestDataGenerator(event['brandId'], event['ids'], customer).generate_testing_data()
    return {
        'statusCode': 200,
        'body': testData
    }
