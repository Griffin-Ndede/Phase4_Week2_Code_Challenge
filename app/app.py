#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, HeroPower, Power

def create_app():
    app = Flask(__name__)

    # Create an instance of the Flask-RESTful API
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app


app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
api = Api(app)


class Home(Resource):
    def get(self):

        response_dict = {
            "Message": "Welcome to my Heroes and their superpowers API"
        }

        response = make_response(
            jsonify(response_dict),
            200
        )
        return response
    
api.add_resource(Home, "/")




if __name__ == '__main__':
    app.run(port=5555)
