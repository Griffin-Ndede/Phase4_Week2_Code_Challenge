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

        return heroes_data
    
    def post(self):

        new_hero = Hero(
            name = request.form["name"],
            super_name = request.form['super_name'],
        )
        db.session.add(new_hero)
        db.session.commit()

        response_dict = new_hero.to_dict()

        response = make_response(
            jsonify(response_dict),
            201
        )
        return response

api.add_resource(Heroes, "/heroes")
        

if __name__ == '__main__':
    app.run(port=5555)
