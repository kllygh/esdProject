import stripe
import json
import os
import amqp_setup

from dotenv import load_dotenv
import stripe
from flask import Flask


app = Flask(__name__)

# load env variables
load_dotenv()

# get them
stripeSecretKey = os.environ.get("STRIPE_SECRET_KEY")
stripePublicKey = os.environ.get("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = stripeSecretKey

monitorBindingKey = '#.refund'


@app.route("/refund")
def requestRefund():
    amqp_setup.check_setup()

    queue_name = 'Request_Refund'  # can change later

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()


def callback(channel, method, properties, body):
    print("\nReceived a request to notify customer by " + __file__)
    arr = json.loads(body)
    val = arr['refund_details']
    initiate_refund(val[0], val[1])
    print()  # print a new line feed


def initiate_refund(chargeID, amt):
    refund = stripe.Refund.create(
        charge=chargeID,
        amount=amt*100  # amount refunded in cents, assume amt variable is in dollars. Need to check if variable will be string or float
    )

    refund_id = refund.id
    return refund_id


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
