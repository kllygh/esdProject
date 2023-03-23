'''
Things to remember to do:
-- Link this MS to login
-- Link this MS to rabbitMQ for activity logs
-- check line 101 to see if the return code is correct
-- Do we need to do an error handling MS here?

'''
#################### Import libraries ###############################################################################
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

#################### Microservices URL #############################################################################

location_URL = "http://localhost:5200/location"
box_URL = "http://localhost:5000/box/open"
rest_URL = "http://localhost:5300/restaurant"

#################### Call on Near By Complex MS ####################################################################

@app.route("/near_by", methods=['POST'])
def near_by():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            #customer_location: refers to the location that the customer gave {'cust_location': '30 Sembawang Dr, Singapore 757713'}
            customer_location = request.get_json()
            customer_location = json.dumps(customer_location)
            print("\nReceived Customer's location in JSON:", customer_location)

            # do the actual work
            result = processNearByLocation(json.dumps(customer_location))
            print(result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "nearby.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

#################### Main bulk of Near By Complex MS #################################################################

def processNearByLocation(customer_location):
    ###### 2. Ask Mystery Box MS for array of rest_id that posted today ##############################################
    
    print('\n-----Invoking Mystery Box microservice-----')
    box_result = invoke_http(box_URL)
    print(box_result)
    # response_dict = json.loads(box_result)
    boxes_list = box_result['data']['boxes']
    print('\n-----test-----')
    # create an empty list to store the restaurant IDs
    restaurant_ids = []
    for box in boxes_list:
        restaurant_ids.append(box['restaurant_id'])
    print('restaurant_ids:',restaurant_ids)
    print('\n-----End of Mystery Box microservice-----')

    ###### 3. Ask Restaurant MS for lat, lng based on restaurant_id array ###########################################
    
    print('\n-----Invoking Restaurant microservice-----')
    # restaurant_locations: Returns the list of dictionary of the restaurant information ~ restaurant that posted
    msg = {
        "restaurant_ids": restaurant_ids
        }
    restaurant_locations = invoke_http(rest_URL, method="POST", json=msg)
    print('restaurant_locations:',restaurant_locations)
    print('\n-----End of Restaurant microservice-----')

    ###### 4. Ask Location MS for top 20 nearest recommendation based on restaurant_location array #################
    print('\n-----Invoking Location microservice-----')
    nearby_locations = invoke_http(location_URL, method="POST", json={"starting_location":customer_location,"restaurant_location":restaurant_locations})
    print('order_result:',nearby_locations)
    print('\n-----End of Location microservice-----')

    #check if this return way is correct
    return {
        'code': '200',
        'data': nearby_locations
        }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
