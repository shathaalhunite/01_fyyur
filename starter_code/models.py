from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Integer


import json
from collections import namedtuple

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.String) 
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    image_link =db.Column(db.String(120))
    genres = db.Column(db.String)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy=True)
   
class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.Integer)
    genres = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    image_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', cascade='all, delete-orphan' , lazy=True)

class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'))
    start_time = db.Column(db.DateTime())
