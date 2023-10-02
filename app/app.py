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


if __name__ == '__main__':
    app.run(port=5555)
