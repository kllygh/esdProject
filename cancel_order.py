from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
# from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_setup
import notification

app = Flask(__name__)
CORS(app)

orderURL = "http://localhost:5001/order"
boxURL = "http://localhost:5000/box"

##is refund going to be triggered onclick, or need to have flask route?
##need to add code to receive OrderID

############# code added here #########################################################
@app.route('/cancel_order/<OrderID>', methods=['POST'])

def CancelOrder(OrderID):
    #get order details
    order = invoke_http(orderURL + '/' + OrderID) #type = dict
    ############# code added here #########################################################
    #or is it:
    #OrderID = order['data']['OrderID']
    code = order["code"]
    message = json.dumps(order)
    if code not in range(200, 300):
        routing_key = 'retrieveDetails.error'
        ############# code added here #########################################################
        #updateActivityandError(OrderID, message, order, routing_key) OR
        updateActivityandError(code, message, order, routing_key)
        return {
            "code": 500,
            "data": {"cancel_order_result": order},
            "message": "Cancel order failure sent for error handling."
        }
    routing_key = 'retrieveDetails.info'
    updateActivityandError(code, message, order, routing_key)

    #update inventory
    orderDetails = order["data"]
    quantity = orderDetails["quantity"]
    boxID = orderDetails["boxID"]
    box = invoke_http(boxURL + '/' + boxID)
    code = box["code"]
    message = json.dumps(box)
    if code not in range(200, 300):
        routing_key = 'retrieveBox.error'
        updateActivityandError(code, message, box, routing_key)
        return {
            "code": 500,
            "data": {"cancel_order_result": box},
            "message": "Cancel order failure sent for error handling."
        }
    routing_key = 'retrieveBox.info'
    updateActivityandError(code, message, box, routing_key)

    quantity += box["data"]["quantity"] #new quantity to update
    quantity_json = jsonify(
            {"quantity": quantity}
        )
    box = invoke_http(boxURL + '/' + boxID, method='PUT', json=quantity_json)
    code = box["code"]
    message = json.dumps(box) 
    if code not in range(200, 300):
        routing_key = 'updateInventory.error'
        updateActivityandError(code, message, box, routing_key)
        return {
            "code": 500,
            "data": {"cancel_order_result": box},
            "message": "Cancel order failure sent for error handling."
        }
    routing_key = 'updateInventory.info' 
    updateActivityandError(code, message, box, routing_key)

    
    #start refunding
    global phoneNo
    global amount
    chargeID = orderDetails["charge_id"]
    amount = orderDetails["total_bill"] #is string
    phoneNo = orderDetails[""] #need to add when jolene update order MS
    startRefund(chargeID, amount)

############# code added here #########################################################
#update order

def update_order_status(refund_status, OrderID):
    if refund_status == 'Success':
        order_update = jsonify({"status": "Refunded"})
        order = invoke_http(orderURL + '/' + OrderID, method='PUT', json=order_update)
        code = order["code"]
        message = json.dumps(order)
        if code not in range(200, 300):
            return {
                "code": 500,
                "data": {"cancel_order_result": order},
                "message": "Error updating order status."
            }
        # Update activity status
        routing_key = 'updateOrder.info'
        updateActivityandError(code, message, order, routing_key)
        return {
            "code": 200,
            "data": {"cancel_order_result": order},
            "message": "Order status updated to Refunded."
        }
    else:
        return {
            "code": 500,
            "data": {"cancel_order_result": None},
            "message": "Error processing refund."
        }


##step6-7
def startRefund(chargeID, Amt):
    amqp_setup.check_setup()

    msg = f"""
    {
        "refund_details": [{chargeID}, {float(Amt)}]
    }
    """ #stringify JSON
    # Send a message with reply-to header under properties
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename,
                        routing_key='refund.reply',
                        properties=pika.BasicProperties(reply_to='Refund_Reply'),
                        body=msg) ##body need to include chargeID and amount, send as "{'refund_details': [chargeID, Amt]}"

    ## are we supposed to add this into a function?
    amqp_setup.channel.basic_consume(queue='Refund_Reply',
                        on_message_callback=on_response,
                        auto_ack=True)

    amqp_setup.channel.start_consuming()
    # Listen for the response message on the reply-to queue


def on_response(channel, method, properties, body):
    print("Response from Refund MS received")
    notification.refundCompleted(phoneNo, amount, body.decode()) #amount here is a string
    amqp_setup.connection.close()

def updateActivityandError(code, message, order_result, rKey):
    amqp_setup.check_setup()

    if code not in range(200, 300):
        print('\n\n-----Publishing the error message with routing_key=' + rKey + '-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=rKey, 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))      
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), order_result)

    else:
        print('\n\n-----Publishing the info message with routing_key=' + rKey + '-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=rKey, 
            body=message)
    
    print("\nOrder published to RabbitMQ Exchange.\n")