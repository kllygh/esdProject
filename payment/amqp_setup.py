import pika

hostname = "localhost"
port = 5672
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
    ))

channel = connection.channel()

# Set up the exchange
exchangename = "refund"
exchangetype = "direct"
channel.exchange_declare(exchange=exchangename,
                         exchange_type=exchangetype, durable=True)


############   Refund queue   #############
# delcare queue
queue_name = 'Refund'
channel.queue_declare(queue=queue_name, durable=True)

# bind queue
channel.queue_bind(exchange=exchangename,
                   queue=queue_name, routing_key='refund')
# bind the queue to the exchange via the key

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'direct' exchange to be used by the microservices in the solution.
"""


def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
