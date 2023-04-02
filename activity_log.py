from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from datetime import date

import json
import os

import amqp_setup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/activity_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


############ 1. Creation of the database #####################################################
db = SQLAlchemy(app)
CORS(app)

class Logs(db.Model):
    __tablename__ = 'activity_log'

    activityID = db.Column(db.Integer, primary_key=True)
    activity_details = db.Column(db.String(64), nullable=False)

    def __intit__(self, activityID, activity_details):
        self.activityID = activityID
        self.activity_details = activity_details

    def json(self):
        return {"activityID": self.activityID,
                "activity_details": self.activity_details
                }

############ 2. Receiving the data from the queue #####################################################
monitorBindingKey = '#.info'


def receiveOrderLog():
    amqp_setup.check_setup()

    queue_name = 'Activity_log'

    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()


def callback(channel, method, properties, body):
    print("\nReceived an order log by " + __file__)
    processLog(json.loads(body))
    print()


def processLog(order):
    print("Recording an order log:")
    print(order)
    newLogs = order['message'] #everyone need to change their MS to return message also!

    db.session.add(newLogs)
    db.session.commit()

    #should be like this
    # {
    #     "code": 404,
    #     "data": {
    #         "order_id": 12345
    #     },
    #     "message": "Order not found." ---> REQUIRED
    # }


    #Cancel order: error return
    # this would be how the message look like
    # {
    #     "code": 404,
    #     "data": {
    #         "order_id": 12345
    #     },
    #     "message": "Order not found."
    # }

    # this would be how the message look like with the success
    # {
    #     "code": 200,
    #     "data": {
    #         "id": "12345",
    #         "product_name": "Example Product",
    #         "quantity": 2,
    #         "price": 10.99,
    #         "customer_name": "John Doe",
    #         "customer_email": "johndoe@example.com",
    #         "order_date": "2023-04-01 14:30:00"
    #     }
    # }

    #Near by: error return

    # this is how it would look like
    # {
    #     "code": 200,
    #     "data": [{'lat':37.48007705012013, 'lng':-122.14532593683853},{'lat':37.48053919210831, 'lng':-122.15144075520307},{'lat':37.477040045901575, 'lng':-122.15352062600218},{'lat':37.477139080546856, 'lng':-122.16080017167964},{'lat':37.46779623020498, 'lng':-122.14041744300732},
    #                 {'lat':37.46779623020498, 'lng':-122.1516903396774},{'lat':37.46600271717554, 'lng':-122.1568760578018},{'lat':37.46600271717554, 'lng':-122.1568760578018},{'lat':37.469206976332174, 'lng':-122.16603436035237},{'lat':37.469206976332174, 'lng':-122.16603436035237},
    #                 {'lat':1.3823169660466292, 'lng':103.68905007456796},{'lat':37.465231300843634, 'lng':-122.18633215021532},{'lat':37.46888062276618, 'lng':-122.18027645639775},{'lat':37.48068777703546, 'lng':-122.16188508879591},{'lat':37.47789932093983, 'lng':-122.13844731073895}
    #             ]
    # }

    # {
    #     "code": 404,
    #     "data": "1 hack drive, menlo park, CA",
    #     "message": "Unable to suggest top 20 nearest locaion."
    # }


    

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
