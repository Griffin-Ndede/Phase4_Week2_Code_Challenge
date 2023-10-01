#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, hero_powers, Power

app = Flask(__name__)

# Create an instance of the Flask-RESTful API
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'This is my Hero API home page'

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

api.add_resource(Heroes, "/heroes")
        

if __name__ == '__main__':
    app.run(port=5555)
