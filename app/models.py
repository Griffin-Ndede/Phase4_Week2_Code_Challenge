from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    super_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
# Define the many-to-many relationship with powers through hero_powers
    powers = db.relationship('Power', secondary='hero_powers', backref='heroes', lazy=True)


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    # Define a one-to-many relationship between Power and HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', lazy=True)

class hero_powers(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(), nullable=False)
    hero_id = db.column(db.Integer, db.ForeignKey('hero.id'))
    powers_id = db.column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    # Define the relationship to the Power model
    power = db.relationship('Power', back_populates='hero_powers', lazy=True)
    # Define the relationship to the Hero model
    hero = db.relationship('Hero', back_populates='hero_powers', lazy=True)
