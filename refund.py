import stripe
import json
import os
import amqp_setup

# from flask import Flask
import pika


# app = Flask(__name__)

# get them
stripeSecretKey = os.environ.get("STRIPE_SECRET_KEY")
stripePublicKey = os.environ.get("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = stripeSecretKey
stripe.api_key = stripeSecretKey

monitorBindingKey = '#.refund'

def requestRefund():
    amqp_setup.check_setup()
        
    queue_name = 'Refund' #can change later
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=on_request, auto_ack=True)
    amqp_setup.channel.start_consuming()

def on_request(channel, method, properties, body):
    print("\nReceived a request to notify customer by " + __file__)
    print('\n--------------TEST 1 PASSED----------------')
    arr = json.loads(body) 
    print(arr)

    val = arr['refund_details']
    ref_json = initiate_refund(val[0], val[1])
    ref = json.dumps(ref_json)
    print('\n--------------TEST 2 PASSED----------------')

    amqp_setup.check_setup()
    if channel.is_open:
        print('\n--------------CHANNEL OPEN, INITIATING RETURN MESSAGE----------------')
        amqp_setup.channel.basic_publish(
            exchange=amqp_setup.exchangename, #assume we using the same exchange as the others
            routing_key=properties.reply_to, #need to be declared in cancel an order MS
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=ref
                        )
        print("Message sent.") # print a new line feed
    else:
        print("Channel not open, unable to send message.")


def initiate_refund(chargeID, amt):
    print('\n\n--------Start Refund--------')

    amt = int(amt*100)
    refund = stripe.Refund.create(
        payment_intent = chargeID,
        amount = amt #amount refunded in cents, MUST BE INT NOT FLOAT
    )
    print('\n\n--------End Refund--------')
    if refund.status == 'succeeded':
        refund_id = refund.id
        return {
            "refund_id": refund_id,
            "status": refund.status
        }
    return {
        "status": refund.status
    }

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    requestRefund()