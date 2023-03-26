import pika

hostname = "localhost"
port = 5672
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
    ))

channel = connection.channel()
exchangename = "order_topic"
exchangetype = "topic"
channel.exchange_declare(exchange=exchangename,
                         exchange_type=exchangetype, durable=True)

<<<<<<< HEAD
queue_name = 'Activity_log'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename,
                   queue=queue_name, routing_key='#.info')
=======
queue_name='Activity_log'
channel.queue_declare(queue=queue_name,durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.info')

queue_name="Error"
channel.queue_declare(queue=queue_name,durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.error')

queue_name="Notification"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.notify')
>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729

queue_name = "Error"
channel.queue_declare(queue=queue_name, durable=True)
<<<<<<< HEAD
channel.queue_bind(exchange=exchangename,
                   queue=queue_name, routing_key='#.error')

queue_name = "Notification"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name,
                   routing_key='#.notify')

queue_name = "Refund"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name,
                   routing_key='#.refund')

queue_name = "Refund_Reply"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename,
                   queue=queue_name, routing_key='#.reply')

=======
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.refund')

queue_name="Refund_Reply"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.reply')
>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729

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
