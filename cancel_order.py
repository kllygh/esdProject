from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
# from os import environ

import requests
# from invokes import invoke_http

import pika
import json
import amqp_setup
import notification

app = Flask(__name__)
CORS(app)

##need to add code to receive OrderID

##step 1, 14
def CancelOrder():
    return

##step 2-3
##is refund going to be triggered onclick, or need to have flask route?
def GetOrderDetails(): 
    return

##step 4-5
def UpdateInventory(): 
    return

##step6-7
def startRefund():
    amqp_setup.check_setup()

    ##look at jolene's order MS to see how to get phoneNo, chargeID and Amt

    # Send a message with reply-to header under properties
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename,
                        routing_key='refund.reply',
                        properties=pika.BasicProperties(reply_to='Refund_Reply'),
                        body='') ##body need to include chargeID and amount, send as {{'refund_details': [chargeID, Amt]}}

    # Listen for the response message on the reply-to queue
def on_response(channel, method, properties, body):
    print("Response received")
    GetOrderDetails() #get phoneNo (str) and Amt (float)
    notification.refundCompleted(phoneNo,body.decode(), Amt) 
    amqp_setup.connection.close()

## are we supposed to add this into a function? but if we do then how to we trigger the function?
amqp_setup.channel.basic_consume(queue='Refund_Reply',
                    on_message_callback=on_response,
                    auto_ack=True)

amqp_setup.channel.start_consuming()

##step 8-10,13
def ProcessRefund(): ##send data to activity and error log
    return

##step 11-12
def UpdateOrder():
    return