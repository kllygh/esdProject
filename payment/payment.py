from dotenv import load_dotenv
import os
import stripe
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# load env variables
load_dotenv()

# get them
stripe_secret_key = "sk_test_51Mmaq9Kcs6la72jh0v2KAFQGvOWzqEVksC3hLHdDwf7UfuTRLxS62UVBJFxdZfnvGHcWLVmSuHLypH5kyHWGaQuy00wKtjTYqW"
#  os.environ.get(
#     "STRIPE_SECRET_KEY") or
stripe_publish_key = "pk_test_51Mmaq9Kcs6la72jh1ZMbbP5wP4yd0wbYZ43d1aDu09CDagPhLEet12Mcho1Nm2gApRmaPt8CCHrrFpWNsKb3h6De00PYaYjnbP"
# os.environ.get(
#     "STRIPE_PUBLISHABLE_KEY") or

# NOTE The secret key is used for server-to-server interactions with the Stripe API, while the publishable key is used for client-side interactions, specifically for tokenizing card information with Stripe.js.

stripe_keys = {
    "secret_key": stripe_secret_key,
    "publishable_key": stripe_publish_key,
}

stripe.api_key = "sk_test_51Mmaq9Kcs6la72jh0v2KAFQGvOWzqEVksC3hLHdDwf7UfuTRLxS62UVBJFxdZfnvGHcWLVmSuHLypH5kyHWGaQuy00wKtjTYqW"


# @app.route("/")
# def index():
#     return render_template("./index.html")


# @app.route("/config")
# def get_publishable_key():
#     stripe_config = {"publicKey": stripe_keys["publishable_key"]}
#     return jsonify(stripe_config)


@app.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    # needs to render the payment page
    domain_url = "http://localhost:5001/"  # define domain url
    stripe.api_key = stripe_keys["secret_key"]   # send stripe secret key
    # used the secret key to create a unique Checkout Session ID
    data = request.get_json()
    currency = data["currency"]
    unit_amount = data["unit_amount"]
    boxID = data["boxID"]
    quantity = data["quantity"]

    try:
        # Create new Checkout Session for the order
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success",
            # success_url=domain_url +
            # "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": unit_amount,
                        "product_data": {
                            "name": boxID
                        }
                    },
                    "quantity": quantity,
                }
            ]
        )
        return jsonify(
            {
                "sessionId": checkout_session["id"],
                "message": "Payment successful",
                "code": 200

            }
        )   # send id back
    except Exception as e:
        error = str(e)
        message = "Payment has failed to go through"
        return jsonify(
            {
                "code": 403,
                "message": message,
                "error": error
            }
        ), 403
        # return jsonify(error=str(e)), 403


# webhook endpoint
# @app.route("/webhook", methods=["POST"])
# def stripe_webhook():
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get("Stripe-Signature")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, stripe_keys["endpoint_secret"]
#         )

#     except ValueError as e:
#         # Invalid payload
#         return "Invalid payload", 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return "Invalid signature", 400

#     # Handle the checkout.session.completed event
#     if event["type"] == "checkout.session.completed":
#         print("Payment was successful.")
#         # TODO: run some custom code here

#     return "Success", 200


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancel")
def cancelled():
    return render_template("cancel.html")

# To do after UI
# Add each of your products to a database.
# NOTE TO UI PEOPLE:Then, when you dynamically create the product page, store the product database ID and price in data attributes within the purchase button.

# NOTE TO UI PEOPLE: Update the JavaScript event listener to grab the product info from the data attributes and send them along with the AJAX POST request to the /create-checkout-session route.

# Parse the JSON payload in the route handler and confirm that the product exists and that the price is correct before creating a Checkout Session.

# difference between requests and request:
# request is an object representing the current HTTP request being handled by a Flask application. It has a json attribute that contains the JSON payload of the request. This attribute is used in Flask applications to access the JSON data sent in the request.
# requests is a Python package used for sending HTTP requests. It has a json() method that returns the JSON-encoded content of a response as a Python object. This method is used on the response object returned by the requests library.


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": payment ...")
    app.run(host='0.0.0.0', port=6002, debug=True)
