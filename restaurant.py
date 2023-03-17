from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(64), nullable=False)
    restaurant_location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


    def __init__(self, restaurant_id, restaurant_name, restaurant_location, latitude, longitude):
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.restaurant_location = restaurant_location
        self.latitude = latitude
        self.longitude = longitude


    def json(self):
        return {"restaurant_id": self.restaurant_id, "restaurant_name": self.restaurant_name, "restaurant_location": self.restaurant_location, "latitude": self.latitude, "longitude":self.longitude}


#################### GET ALL RESTAURANTS #################################
@app.route("/restaurant")
def get_all():
    restaurantlist = Restaurant.query.all()
    if len(restaurantlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "restaurants": [restaurant.json() for restaurant in restaurantlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no restaurants."
        }
    ), 404


#################### GET A RESTAURANT BY ID #################################
@app.route("/restaurant/<int:restaurant_id>")
def find_by_restaurant_id(restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if restaurant:
        return jsonify(
            {
                "code": 200,
                "data": restaurant.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Restaurant not found."
        }
    ), 404


#################### GET SOME RESTAURANTS #################################
######### /restaurants?count=5 to retrieve the first 5
@app.route("/restaurants")
def get_some():
    count = request.args.get("count", default=10, type=int) # set a default value of 10 if count parameter not provided
    restaurantlist = Restaurant.query.limit(count).all()
    if len(restaurantlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "restaurants": [restaurant.json() for restaurant in restaurantlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no restaurants."
        }
    ), 404


#################### ADD A RESTAURANT #################################
@app.route("/restaurant/<int:restaurant_id>", methods=['POST'])
def create_restaurant(restaurant_id):
    if (Restaurant.query.filter_by(restaurant_id=restaurant_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "restaurant_id": restaurant_id
                },
                "message": "Restaurant already exists."
            }
        ), 400

    data = request.get_json()
    restaurant = Restaurant(restaurant_id, **data)

    try:
        db.session.add(restaurant)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "restaurant_id": restaurant_id
                },
                "message": "An error occurred creating the restaurant."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": restaurant.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(port=5000, debug=True)

