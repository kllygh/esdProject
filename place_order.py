from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

import stripe

app = Flask(__name__)
CORS(app)


order_URL = environ.get('order_URL') or "http://localhost:5001/order"
box_URL = environ.get('box_URL') or "http://localhost:5000/box"
payment_URL = environ.get(
    "payment_URL") or "http://localhost:6002/payment"


@app.route("/place_order", methods=['POST'])
def place_order():
    # NOTE: FROM UI -> send customer id, customer number, boxID, quantity
    if request.is_json:
        try:
            order = request.get_json()
            print("Received a mystery box order (JSON):", order)

            result = processPlaceOrder(order)
            print("\n------------------------------------")
            print("\nresult:", result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processPlaceOrder(order):
    # 2. Send the order info

    # NOTE: Order sent from UI must contain customer_number, customer_id, restaurant_id, boxID, quantity, total_bill (calculated), transaction_no, payment_method, currency

    # Get order info
    boxID = int(order["boxID"])
    quantity = int(order["quantity"])
    customer_number = int(order["customer_number"])
    customer_id = int(order["customer_id"])
    restaurant_id = int(order["restaurant_id"])
    total_bill = order["total_bill"]  # not sure

    # ASK not sure if needed: how to get payment method
    # payment_method = order["payment_method"] or None
    transaction_no = order["transaction_no"] or None
    currency = order["currency"] or None

    # Set unit amount, which is in cents
    cents = int(total_bill * 100)

    print(boxID, quantity, customer_number, customer_id, restaurant_id,
          total_bill, transaction_no, currency)

    # 3. Check if sufficient inventory

    print('\n------Invoking box microservice-----')
    inv_URL = f"{box_URL}/inventory/{boxID}/{quantity}"
    inventory_result = invoke_http(inv_URL, method="GET")
    print("inventory_result:", inventory_result, '\n')

    curr_inventory = inventory_result["data"]["inventory"]

    # 4. if insufficient inventory, send to error
    code_inventory = inventory_result["code"]
    message_inventory = json.dumps(inventory_result)
    rabbit_msg = inventory_result["message"]

    amqp_setup.check_setup()

    if code_inventory not in range(200, 300):
        # publish to error
        return publish_error(message_inventory, inventory_result,
                             code_inventory, rabbit_msg)

    # if order success
    else:
        publish_activity(message_inventory, rabbit_msg)

    print("\nInventory sufficient activity published to RabbitMQ Exchange.\n")

    # 4. Since sufficient inventory, send to Order to record
    print('\n------Invoking Order microservice-------')
    new_order_URL = f"{order_URL}/new"
    order_result = invoke_http(new_order_URL, method="POST", json=order)
    print("order_result:", order_result)

    code_order = order_result["code"]
    message_order = json.dumps(order_result)
    rabbit_msg = order_result["message"]
    order_id = order_result["data"]["order_id"]

    if code_order not in range(200, 300):
        return publish_error(message_order, order_result, code_order, rabbit_msg)
    else:
        publish_activity(message_order, rabbit_msg)

    print("\nOrder activity sent to RabbitMQ Exchange Activity Log")

    # 5. Conduct Payment
    print("\n------Invoking Payment microservice-------")

    # NOTE: Create payment info object to send to Payment
    payment = {
        "boxID": boxID,
        "amount": cents,
        "currency": currency
    }
    # NOTE
    intent_URL = payment_URL + "/create-payment-intent"
    intent_result = invoke_http(intent_URL, method="POST", json=payment)
    print("payment_result:", intent_result)

    client_secret = intent_result["clientSecret"]
    # client_secret = payment_result.json()["client_secret"]

    code_payment = intent_result["code"]
    message_payment = json.dumps(intent_result)
    rabbit_msg = intent_result["message"]

    if code_payment not in range(200, 300):
        return publish_error(message_payment, intent_result,
                             code_payment, rabbit_msg)
    else:
        publish_activity(message_payment, rabbit_msg)

    print("\nPayment activity sent to RabbitMQ Exchange Activity Log")

    charge_id = retrieve_chargeID(intent_result)

    updated_order = update_order(charge_id, order_id, "PAID")
    message_updated = json.dumps(updated_order)

    if updated_order["code"] not in range(200, 300):
        return publish_error(message_updated, updated_order,
                             updated_order["code"], updated_order["message"])
    else:
        publish_activity(message_updated, updated_order["message"])

    # 6. Update inventory in Box
    updated_box = update_inventory(curr_inventory, quantity, boxID)
    code_updatedbox = updated_box["code"]
    message_updatedbox = json.dumps(updated_box)
    rabbit_msg = updated_box["message"]
    if updated_box["code"] not in range(200, 300):
        return publish_error(message_updatedbox, updated_box, code_updatedbox, rabbit_msg)
    else:
        publish_activity(message_updatedbox, rabbit_msg)

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result
        }
    }


def update_inventory(curr_inventory, quantity, boxID):
    new_inventory = int(curr_inventory) - int(quantity)
    update_box_details = {
        "inventory": new_inventory
    }
    update_box_URL = f"{box_URL}/{boxID}"
    updated_box = invoke_http(
        update_box_URL, method="PUT", json=update_box_details)
    return updated_box


def update_order(charge_id, order_id, status):
    update_details = {
        "charge_id": charge_id,
        "order_id": order_id,
        "status": status
    }
    update_URL = f"{order_URL}/update/{order_id}"
    updated_order = invoke_http(update_URL, method="PUT", json=update_details)
    return updated_order


def retrieve_chargeID(payment_result):
    # NOTE: Retrieve charge ID

    # step 1: retrieve session ID from returned object
    session_id = payment_result["sessionId"]
    session = stripe.checkout.Session.retrieve(session_id)

    # step 2: create PaymentIntent object
    payment_intent = stripe.PaymentIntent.retrieve(
        session.payment_intent, expand=['latest_charge.id'])

    # step 3: get charge id from prev session
    charge_id = payment_intent.latest_charge.id
    return charge_id


def publish_error(message, order_result, code, rabbit_msg):
    # error MS
    print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error",
                                     body=message, properties=pika.BasicProperties(delivery_mode=2))

    print("\n {} ({:d}) published to the RabbitMQ Exchange:".format(
        rabbit_msg, code), order_result)

    # 7. Return error
    return {
        "code": 500,
        "data": {"order_result": order_result},
        "message": rabbit_msg
        # "There is insufficient inventory ."
        # "Order creation failure sent for error handling."
    }


def publish_activity(message, rabbit_msg):
    print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')
    print(rabbit_msg)
    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchangename, routing_key="order.info", body=message)


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
