from dotenv import load_dotenv
import os
import stripe
import amqp_setup
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# load env variables
load_dotenv()

# get them
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")
stripe_publish_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")

# NOTE The secret key is used for server-to-server interactions with the Stripe API, while the publishable key is used for client-side interactions, specifically for tokenizing card information with Stripe.js.

stripe_keys = {
    "secret_key": stripe_secret_key,
    "publishable_key": stripe_publish_key,
}

stripe.api_key = stripe_keys["secret_key"]


@app.route("/")
def index():
    return render_template("./index.html")


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5001/"  # define domain url
    stripe.api_key = stripe_keys["secret_key"]   # send stripe secret key
    # used the secret key to create a unique Checkout Session ID

    try:
        # Create new Checkout Session for the order
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url +
            "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": 'sgd',
                        "unit_amount": "2000000",
                        "product_data": {
                            "name": 'My Product'
                        }
                    },
                    "quantity": 1,
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})   # send id back
    except Exception as e:
        return jsonify(error=str(e)), 403


# webhook endpoint
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: run some custom code here

    return "Success", 200


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancel")
def cancelled():
    return render_template("cancel.html")

# To do after UI
# Add each of your products to a database.
# Then, when you dynamically create the product page, store the product database ID and price in data attributes within the purchase button.
# Update the /create-checkout-session route to only allow POST requests.
# Update the JavaScript event listener to grab the product info from the data attributes and send them along with the AJAX POST request to the /create-checkout-session route.
# Parse the JSON payload in the route handler and confirm that the product exists and that the price is correct before creating a Checkout Session.

# difference between requests and request:
# request is an object representing the current HTTP request being handled by a Flask application. It has a json attribute that contains the JSON payload of the request. This attribute is used in Flask applications to access the JSON data sent in the request.
# requests is a Python package used for sending HTTP requests. It has a json() method that returns the JSON-encoded content of a response as a Python object. This method is used on the response object returned by the requests library.


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": payment ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
