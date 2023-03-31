# from dotenv import load_dotenv
import os
import stripe
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='place_order', static_url_path='',template_folder='place_order')
CORS(app)

# load_dotenv()

stripe_secret_key = os.environ.get(
    "STRIPE_SECRET_KEY") or "sk_test_51M25gLJNS4gB3cUWOEkkGPcmXZCjJ0V0TsGbmq0dBZnsIvn97Mu7smxnLuopWOpa0bAhceZZdNtwC9TOBkfZRkP300O1mg1T0h"
#sk_test_51Mmaq9Kcs6la72jh0v2KAFQGvOWzqEVksC3hLHdDwf7UfuTRLxS62UVBJFxdZfnvGHcWLVmSuHLypH5kyHWGaQuy00wKtjTYqW

stripe_publish_key = os.environ.get(
    "STRIPE_PUBLISHABLE_KEY") or "pk_test_51M25gLJNS4gB3cUWC9UQDBWnQfcivrY2TdhUL0PGSTh5Gsu27E1WfJreVOxN2rCIy63Bt0qDGDD7ulYshCGmUcju00SnS84DEU"
# pk_test_51Mmaq9Kcs6la72jh1ZMbbP5wP4yd0wbYZ43d1aDu09CDagPhLEet12Mcho1Nm2gApRmaPt8CCHrrFpWNsKb3h6De00PYaYjnbP
stripe_keys = {
    "secret_key": stripe_secret_key,
    "publishable_key": stripe_publish_key,
}
stripe.api_key = stripe_keys["secret_key"]

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

# @app.route('/place_order')
# def place_order():
#     return render_template('place_orer.html')

@app.route('/create-payment-intent', methods=["POST"])
def create_payment_intent():
    # get payment details
    # data = request.get_json()
    
    # amount = data["amount"]
    # currency = data["currency"]
    # token = data["token"]
    # description = data["description"]

    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='sgd',
            automatic_payment_methods={"enabled": True},
        )
        # return client secret to Place an Order (to confirm payment)
        # return jsonify({"client_secret": intent.client_secret})
        return jsonify({'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify({"error": str(e)}), 403



# @app.route("/confirm-payment", methods=["POST"])
# def confirm_payment():
#     data = request.get_json()

#     try:
#         # Retrieve payment intent
#         intent = stripe.PaymentIntent.retrieve(data["payment_intent_id"])

#         # confirm payment intent with the provided payment method and payment details
#         # NOTE If payment fails, the PaymentIntent will transition to the requires_payment_method status. If payment succeeds, the PaymentIntent will transition to the succeeded status

#         # NOTE TO UI PEOPLE:  payment_method_id is expected to be included in the POST request data that is sent to the Flask route, either in an HTML form input field or in a JSON payload.
#         intent.confirm(
#             payment_method=data["payment_method_id"], metadata=data["metadata"])

#         # return success response to Place an Order
#         return jsonify({"message": "Payment Intent success", "code": 201, }, 201)

#     except Exception as e:
#         return jsonify({"message": "Payment failed to create Payment Intent", "error": str(e)}), 400


# if __name__ == '__main__':
#     print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
#     app.run(host='0.0.0.0', port=6002, debug=True)
if __name__=='__main__':
    app.run(port=4242)
