from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.String())
    super_name = db.Column(db.String())
    created_at = db.Column ()
    updated_at = db.Column(db.DateTime)

# add any models you may need. 