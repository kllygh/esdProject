from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
# from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_setup

app = Flask(__name__)
CORS(app)

orderURL = "http://localhost:5001/order"
boxURL = "http://localhost:5000/box"

############# code added here #########################################################
@app.route('/cancel_order/<OrderID>', methods=['POST'])
def CancelOrder(OrderID):
    try:
        global orderID 
        orderID = int(OrderID)
        try:
            #get order details
            print('\n-----1. Getting order details from Order MS-----')
            order = invoke_http(orderURL + '/' + str(orderID)) #type = dict
            print(order)
            code = order["code"]
            message = json.dumps(order)
            if code not in range(200, 300):
                routing_key = 'retrieveDetails.error'
                updateActivityandError(code, message, order, routing_key)
                return {
                    "code": 500,
                    "data": {"cancel_order_result": order['data'], "status": "Failed"},
                    "message": "Unable to find Order."
                }, 500
            routing_key = 'retrieveDetails.info'
            updateActivityandError(code, message, order, routing_key)

            print('\n\n--------2. Sending to ProcessCancelOrder--------')
            result = ProcessCancelOrder(order['data'])
            print('\nresult: ', result)
            print('\n\n--------7. End ProcessCancelOrder--------')

            try:
                print('\n\n--------8. Send to update_order_status--------')
                status = refundDetails['status']
                result = update_order_status(status)
                print('\n\n----------9. End update_order_status----------')
                return jsonify(result), result["code"]
            except:
                result = {
                        "code": 500,
                        "data": {
                                "status": "Failed"
                            },
                        "message": "Order refundID unable to be updated."
                    }
                return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "cancel_order.py internal error: " + ex_str
            }), 500
    
    # if reached here, not an int.
    except:
        print('\n\n--------Error not Int--------')
        return jsonify({
            "code": 400,
            "message": "Not an integer"
        }), 400

def ProcessCancelOrder(orderDetails):
    #update inventory
    print('\n\n--------3. Start Update Inventory--------')
    quantity = orderDetails["quantity"]
    boxID = str(orderDetails["boxID"])
    box = invoke_http(boxURL + '/' + boxID)
    # code = box["code"]
    # message = json.dumps(box)
    # if code not in range(200, 300):
    #     routing_key = 'retrieveBox.error'
    #     updateActivityandError(code, message, box, routing_key)
    #     return {
    #         "code": 500,
    #         "data": {"cancel_order_result": box, "status": "Failed"},
            
    #     }
    # routing_key = 'retrieveBox.info'
    # updateActivityandError(code, message, box, routing_key)

    quantity += box["data"]["quantity"] #new quantity to update
    quantity_json = {"quantity": quantity}
    box = invoke_http(boxURL + '/' + boxID, method='PUT', json=quantity_json)
    code = box["code"]
    message = json.dumps(box) 
    if code not in range(200, 300):
        routing_key = 'updateInventory.error'
        updateActivityandError(code, message, box, routing_key)
        return {
            "code": 500,
            "data": {"cancel_order_result": box, "status": "Failed"},
            "message": "Unable to update inventory."
        }
    routing_key = 'updateInventory.info' 
    updateActivityandError(code, message, box, routing_key)
    print('\n\n--------4. End update Inventory--------')

    #start refunding
    global phoneNo
    global amount
    chargeID = orderDetails["charge_id"]
    amount = str(orderDetails["total_bill"]) #is string
    phoneNo = '+65' + str(orderDetails["customer_number"])
    print('\n\n--------5. Send to refund.py--------')
    startRefund(chargeID, amount)
    print('\n\n--------6. Exit refund.py--------')
    if refundDetails['status'] == 'succeeded':
        return {
            "code": 200,
            "data": {
                "status": "Success"
            },
            "message": "Order successfully refunded."
        }
    return {
            "code": 500,
            "data": {
                "status": "Failed"
            },
            "message": "Order unable to be refunded. Please try again."
        }

def update_order_status(refund_status):
    #update order
    if refund_status == 'succeeded':
        print('\n\n--------Start Update Order--------')
        refID = refundDetails['refund_id']
        order_update = {"status": "REFUNDED", "refund_id": refID}
        order = invoke_http(orderURL + '/update/' + str(orderID), method='PUT', json=order_update)
        print('\n\n--------End Update Order--------')
        print(order)
        code = order["code"]
        message = json.dumps(order)
        if code not in range(200, 300):
            routing_key = 'updateOrder.error'
            updateActivityandError(code, message, order, routing_key)
            return {
                "code": 500,
                "data": {"status": "Failed"},
                "message": "Order refund unsuccessful."
            }
        routing_key = 'updateOrder.info'
        updateActivityandError(code, message, order, routing_key)
        return {
            "code": 200,
            "data": {
                "cancel_order_result": order['data'],
                "status": "Success"
            },
            "message": "Order successfully refunded."
        }
    else:
        return {
            "code": 500,
            "data": {"cancel_order_result": None},
            "message": "Error processing refund."
        }

##step6-7
def startRefund(chargeID, Amt):
    print('\n\n--------Start Refund--------')
    amqp_setup.check_setup()
    amount = float(Amt)
    msg = f"""
    {{
        "refund_details": ["{chargeID}", {amount:.2f}]
    }}
    """ #stringify JSON

    callback_queue = 'Refund_Reply'
    # Send a message with reply-to header under properties
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename,
                        routing_key='refund.refund',
                        properties=pika.BasicProperties(reply_to='refund.reply', delivery_mode = 2),
                        body=msg) ##body need to include chargeID and amount, send as "{'refund_details': [chargeID, Amt]}"

    amqp_setup.channel.basic_consume(queue=callback_queue,
                        on_message_callback=on_response,
                        auto_ack=True)
    amqp_setup.channel.start_consuming()
    # Listen for the response message on the reply-to queue
    print('\n\n--------End Refund--------')

def on_response(channel, method, properties, body):
    print("Response from Refund MS received")
    global refundDetails
    refundDetails = json.loads(body)
    if refundDetails['status'] == 'succeeded':
        amqp_setup.check_setup()
        refID = refundDetails['refund_id']
        msg = json.dumps({
            "notif_details": [phoneNo, amount, refID]
        })
        print('\n\n----------Send Notification----------')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='refund.notify', 
            body=msg, properties=pika.BasicProperties(delivery_mode = 2))
        print('\n\n----------Notification Sent----------')
    amqp_setup.channel.close()

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
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    
    print("\nOrder published to RabbitMQ Exchange.\n")

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " for cancelling an order...")
    app.run(host="0.0.0.0", port=5500, debug=True)