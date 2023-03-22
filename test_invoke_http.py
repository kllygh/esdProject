#################### Import test_invoke_http.py ##################################################
from invokes import invoke_http


#################### NearyBy Complex MS Testing ##################################################

#invoke ... microservice to ...
results = invoke_http("http://localhost:5000/book",method="GET")

#invoke ... microservice to ...
isbn = '9213213213213'
book_details = {"availability":5,"price":213.00,"title":"ESD"}
create_results = invoke_http(
    "http://localhost:5000/book/" + isbn, method ="POST",
    json = book_details
)

#################### Place an Order Complex MS Testing #############################################

# have not yet added @jolene, klarice if needed!


#################### Cancel an Order Complex MS Testing #############################################

# have not yet added @jx, amanda if needed!


#################### Printing out results created ##################################################

print(type(results))
print()
print(results)

print()
print(create_results)