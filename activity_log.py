import json
import os

import amqp_setup

monitorBindingKey = '#.info'


def receiveOrderLog():
    amqp_setup.check_setup()

    queue_name = 'Activity_log'

    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()


def callback(channel, method, properties, body):
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print()


def processOrderLog(order):
    print("Recording an order log:")
    print(order)

    #Cancel order: error return
    # return {
    #         "code": 500,
    #         "data": {"cancel_order_result": box, "status": "Failed"},
    #         "message": "Unable to update inventory."
    #     }

    

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
