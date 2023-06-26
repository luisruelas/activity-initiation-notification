class Customer:
    def __init__(self, customerId, customerKey):
        self.customerId = customerId
        self.customerKey = customerKey

    def getCustomerId(self):
        return self.customerId
    
    def getCustomerKey(self):
        return self.customerKey
