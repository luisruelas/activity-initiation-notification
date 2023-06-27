from code.lambda_function import lambda_handler
import sys

if len(sys.argv) >= 5:
    customerId = sys.argv[1]
    customerKey = sys.argv[2]
    brandId = sys.argv[3]
    ids = sys.argv[4].split(",")
    print(f"Customer ID: {customerId}")
    print(f"Customer Key: {customerKey}")
else:
    print("Customer ID and Customer Key not provided.")

EVENT = {
    'customerId': customerId,
    'customerKey': customerKey,
    'brandId': brandId,
    'ids': ids,
}
print('EVENT', EVENT)
print(lambda_handler(EVENT, 2))
