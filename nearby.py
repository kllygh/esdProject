'''
Things to remember to do:
-- Link this MS to login (change the user ID in the database based on the firebase)
-- Change the user Id to link with firebase
-- Create a docker file for your current microservice
'''
#################### Import libraries ###############################################################################
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import json

import pika
import json
import amqp_setup

app = Flask(__name__)
CORS(app)

#################### Microservices URL #############################################################################

location_URL = "http://localhost:5200/location"
box_URL = "http://127.0.0.1:5000/box"
rest_URL = "http://localhost:5300/restaurant"

#################### Call on Near By Complex MS ####################################################################

@app.route("/near_by", methods=['POST'])
def near_by():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            #customer_location: refers to the location that the customer gave {'cust_location': '30 Sembawang Dr, Singapore 757713'}
            customer_location = request.get_json()
            print("\nReceived an request in JSON:", customer_location)

            # do the actual work
            customer_location = customer_location["cust_location"]
            result = processNearByLocation(customer_location)
            code = result["code"]
            message = json.dumps(result)

            ######################## Send to AMQP ##########################################
            if code not in range(200, 300):
                routing_key = 'retrieveDetails.error'
                updateActivityandError(code, message, result, routing_key)
                return {
                    "code": 500,
                    "data": result,
                    "message": "Nearby Microservice failure sent for error handling."
                }
            routing_key = 'retrieveDetails.info'
            updateActivityandError(code, message, result, routing_key)
            ####################### End of AMQP ##########################################

            return jsonify(message), result["code"]

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
    print("this is the box result",box_result)
    # response_dict = json.loads(box_result)
    boxes_list = box_result['data']['boxes']
    print("this is the box list",boxes_list)
    
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
    return nearby_locations

#################### AMQP activity log and error handling ############################################################
def updateActivityandError(code, message, result, rKey):
    amqp_setup.check_setup()

    if code not in range(200, 300):
        print('\n\n-----Publishing the error message with routing_key=' + rKey + '-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=rKey, 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))      
        print("\nStatus ({:d}) published to the RabbitMQ Exchange:".format(
            code), result)

    else:
        print('\n\n-----Publishing the info message with routing_key=' + rKey + '-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=rKey, 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    
    print("\nPublished to RabbitMQ Exchange.\n")

#################### Execute this program if it is run as a main script (not by 'import') ############################
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " for placing an order...")
    app.run(host="0.0.0.0", port=5400, debug=True)
