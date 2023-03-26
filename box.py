from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from os import environ
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
# app.config['SQLAlCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/box'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class Box(db.Model):
    __tablename__ = 'box'

    boxID = db.Column(db.Integer, primary_key=True)
    boxName = db.Column(db.String(30), nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    cust_id = db.Column(db.Integer, nullable=False)
    postTime = db.Column(db.DateTime, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    collectionTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    postName = db.Column(db.String(30), nullable=False)
    postDate = db.Column(db.Date, nullable=False)

    def __intit__(self, boxID, boxName, restaurant_id, cust_id, postTime, inventory, collectionTime, price, description, postName, postDate):
        self.boxID = boxID
        self.boxName = boxName
        self.restaurant_id = restaurant_id
        self.cust_id = cust_id
        self.postTime = postTime
        self.inventory = inventory
        self.collectionTime = collectionTime
        self.price = price
        self.description = description
        self.postName = postName
        self.postDate = postDate

    def json(self):
        return {"boxID": self.boxID,
                "boxName": self.boxName,
                "restaurant_id": self.restaurant_id,
                "cust_id": self.cust_id,
                "postTime": self.postTime,
                "inventory": self.inventory,
                "collectionTime": self.collectionTime,
                "price": self.price,
                "description": self.description,
                "postName": self.postName,
                "postDate": self.postDate
                }

# get all posts - filter based on date


@app.route("/box/open")
def get_all():
    boxlist = Box.query.filter_by(postDate=date.today()).all()
    if len(boxlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "boxes": [box.json() for box in boxlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no boxes."
        }
    ), 404

# get post's inventory NOTE


@app.route("/box/inventory/<int:boxID>/<int:quantity>")
def check_inventory(boxID, quantity):
    box = Box.query.filter_by(boxID=boxID).first()
    box_json = box.json()
    if box_json["inventory"] < quantity:
        return jsonify(
            {
                "code": 400,
                "message": "There is insufficient inventory ."
            }
        )
    return jsonify(
        {
            "code": 200,
            "data": box.json(),
            "message": "There is sufficient inventory."
        }
    )


# get a post
@app.route("/box/<int:boxID>")
def find_by_boxID(boxID):
    box = Box.query.filter_by(boxID=boxID).first()
    if box:
        return jsonify(
            {
                "code": 200,
                "data": box.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Box not found."
        }
    ), 404

# update a post


@app.route("/box/<int:boxID>", methods=["PUT"])
def update_box(boxID):
    box = Box.query.filter_by(boxID=boxID).first()
    if box:
        data = request.get_json()
        if data['inventory']:
            box.inventory = data['inventory']

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": box.json(),
                "message": "Updated Inventory successfully."
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "boxID": boxID
            },
            "message": "Box not found."
        }
    ), 404

# delete a post


@app.route("/box/<int:boxID>", methods=['DELETE'])
def delete_box(boxID):
    box = Box.query.filter_by(boxID=boxID).first()
    if box:
        db.session.delete(box)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "boxID": boxID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "boxID": boxID
            },
            "message": "Box not found."
        }
    ), 404

# get a few post


@app.route("/box/rest/<int:restaurant_id>")
def find_by_restaurantID(restaurant_id):
    boxlist = Box.query.filter_by(restaurant_id=restaurant_id)

    if boxlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    'box': [box.json() for box in boxlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Box not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
