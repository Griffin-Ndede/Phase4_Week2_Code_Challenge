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

class Heroes(Resource):
    def get(self):
        #quering the database to retrieve heroes
        heroes = Hero.query.all()

        # Converting the heroes to a list of dictionaries
        heroes_data = [{
            "id": hero.id, 
            "name": hero.name, 
            "super_name": hero.super_name
            } for hero in heroes]

        return jsonify(heroes_data)
    
api.add_resource(Heroes, "/heroes")

class HeroesById(Resource):
    def get(self, id):
        # retrieving the hero id from the database
        hero = Hero.query.filter_by(id=id).first()

        # converting the hero object to a dictionary
        hero_info = {
            "id":hero.id,
            "name":hero.name,
            "super_name":hero.super_name,
        }
        response = make_response(jsonify(hero_info),200)
        
        return response

api.add_resource(HeroesById, "/heroes/<int:id>")

class Powers(Resource):
    def get(self):
        # retrieving powers by id
        powers = Power.query.all()

        # converting the power to object to a dictionary
        power_data = [{
            "id": powers.id,
            "name": powers.name,
            "description": powers.description,
        } for powers in powers]

        return jsonify(power_data)
    
api.add_resource(Powers, "/powers" )

class PowersById(Resource):
    def get(self, id):
        # retrieving powers by id
        power = Power.query.filter_by(id=id).first()

        # converting the power to object to a dictionary

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        response = make_response(jsonify(power_data), 200)

        return response
    def patch(self, id):
        powerupdate = Power.query.get(id)

        data = request.get_json()
        if "name" in data:
            powerupdate.name = data["name"]
        if "description" in data:
            powerupdate.description = data["description"]

        db.session.commit()

        # Create a response with JSON data and set the Content-Type header
        response = make_response({
            "id": powerupdate.id,
            "name": powerupdate.name,
            "description": powerupdate.description
        }, 200)
        
        response.headers['Content-Type'] = 'application/json'  # Set the Content-Type header

        return response
    
api.add_resource(PowersById, "/powers/<int:id>" )

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()

        # Validating that the required fields are present in the request data
        if "strength" not in data or "power_id" not in data or "hero_id" not in data:
            return {"errors": ["validation errors"]}, 400

        # Checking if the provided hero and power IDs exist in the database
        hero = Hero.query.get(data["hero_id"])
        power = Power.query.get(data["power_id"])

        if hero is None or power is None:
            return {"errors": ["validation errors"]}, 400

        # Creating a new HeroPower and associate it with the hero and power
        hero_power = HeroPower(strength=data["strength"], hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        # Retrieving the hero's data including their associated powers
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description,
                }
            ],
        }

        return hero_data, 201

api.add_resource(HeroPowers, "/hero_powers")


if __name__ == '__main__':
    app.run(port=5555)
