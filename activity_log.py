import json
import os

import amqp_setup

<<<<<<< HEAD
monitorBindingKey = '#.info'


def receiveOrderLog():
    amqp_setup.check_setup()

    queue_name = 'Activity_log'

    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()


=======
monitorBindingKey='#.info'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Activity_log'
    
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()

>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729
def callback(channel, method, properties, body):
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print()

<<<<<<< HEAD

=======
>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729
def processOrderLog(order):
    print("Recording an order log:")
    print(order)


<<<<<<< HEAD
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
=======
if __name__ == "__main__": 
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729
