from code.schemas.customer import Customer
import datetime
import json
import os

class TestDataGenerator:
    customer: Customer = None
    ids: list = []
    brandId: int = 0
    TEST_FOLDER = "../../output_tests"
    scriptDir = ""
    def __init__(self, brandId: int, ids: list, customer: Customer):
        self.ids = ids
        self.customer = customer
        self.brandId = brandId
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))

    def generate_testing_data(self):
        return self.__get_test_list()
        # self.__create_testing_json()
        # self.__copy_file_to_postman_tests(self.__get_dest_file())

    # def __create_testing_json(self):
    #     dest_dir = self.__get_dest_dir()
    #     self.__create_dir_if_doesnt_exist(dest_dir)
    #     self.__write_file(self.__get_dest_file())

    # def __copy_file_to_postman_tests(self, dest_file):
    #     os.system(f"cp {dest_file} ~/Documents/VivantaPostmanTests")

    def __get_dest_dir(self):
        dest_file = self.__get_dest_file()
        return os.path.dirname(dest_file)

    def __create_dir_if_doesnt_exist(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    def __write_file(self, dest_file):
        test_lists = self.__get_test_list()
        self.__write_test_list_to_file(test_lists, dest_file)

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

    def __write_test_list_to_file(self, test_list, dest_file):
        with open(dest_file, 'w+') as f:
            print('dest_file', dest_file)
            json.dump(test_list, f)

    def __get_parameters_json(self):
        with open(os.path.join(self.scriptDir, "../../parameters.json"), "r") as file:
            return json.load(file)

    def __get_today_date_ymd(self):
        return datetime.date.today().strftime("%Y-%m-%d")

    def __get_brands_dictionary(self):
        with open(os.path.join(self.scriptDir,"../../brands.json"), "r") as file:
            return json.load(file)

    def __get_dest_file(self):
        brand_name = self.__get_brand_name()
        customer_id = self.customer.getCustomerId()
        file_name = f"{brand_name}_{customer_id}_{self.__get_today_date_ymd()}_testing.json"
        currentFile = os.path.dirname(os.path.abspath(__file__))
        testFolder = os.path.join(self.TEST_FOLDER, file_name)
        return  os.path.join(currentFile, testFolder)

    def __get_brand_name(self):
        brands_dictionary = self.__get_brands_dictionary()
        return brands_dictionary[self.brandId]
