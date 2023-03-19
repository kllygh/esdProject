import stripe
import json
import os
import amqp_setup
import pika

stripePublicKey = 'pk_test_51MmYEkAZMKLMwhgSfZEJ2itVnibnF9zIb9wJnZlLcTE90hQXj79tC4NivjjLU6Vf5KTiEsYMzDyz8lhg7GGebL8K007UA4ZmhZ'
stripeSecretKey = 'sk_test_51MmYEkAZMKLMwhgSYhgnvpoB7BqKKNyORw03IaAtnyMJA5z3AFprqqBFJAwbv9SiN9lGtzYKhKk5M5qRU61Mlte000GF44rQT9'
stripe.api_key = stripeSecretKey

monitorBindingKey='#.refund'

def requestRefund():
    amqp_setup.check_setup()
        
    queue_name = 'Request_Refund' #can change later
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=on_request, auto_ack=True)
    amqp_setup.channel.start_consuming()

def on_request(channel, method, properties, body):
    print("\nReceived a request to notify customer by " + __file__)
    arr = json.loads(body) 
    val = arr['refund_details']
    refID = initiate_refund(val[0], val[1])
    channel.basic_publish(
        exchange=amqp_setup.exchangename, #assume we using the same exchange as the others
        routing_key=properties.reply_to, #need to be declared in Place an order MS
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=refID
                    )
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print() # print a new line feed

def initiate_refund(chargeID, amt):
    refund = stripe.Refund.create(
        charge = chargeID,
        amount = amt*100 #amount refunded in cents, assume amt variable is in dollars. Need to check if variable will be string or float
    )

    refund_id = refund.id
    return refund_id

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    requestRefund()