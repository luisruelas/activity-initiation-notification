from code.schemas.customer import Customer
import datetime
import json
import os

class TestDataGenerator:
    customer: Customer = None
    ids: list = []
    brandId: int = 0
    scriptDir = ""
    def __init__(self, brandId: int, ids: list, customer: Customer):
        self.ids = ids
        self.customer = customer
        self.brandId = brandId
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))

    def generate_testing_data(self) -> list:
        self.testing_data = self.__get_test_list()
        return self.testing_data

    def write_testing_data(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.testing_data))

    def __get_test_list(self):
        test_list = []
        for user_id in self.ids:
            for parameter in self.__get_parameters_json():
                test_dict = {
                    "userId": user_id,
                    "parameter": parameter,
                    "brandId": self.brandId,
                    "date": self.__get_today_date_ymd(),
                    "x-test-customer": self.customer.getCustomerId(),
                    "x-test-api-key": self.customer.getCustomerKey(),
                }
                test_list.append(test_dict)
        return test_list

    def __get_parameters_json(self):
        with open("code/parameters.json") as file:
            return json.load(file)

    def __get_today_date_ymd(self):
        return datetime.date.today().strftime("%Y-%m-%d")
