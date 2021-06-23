#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
import os
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import VenueForm ,ArtistForm,ShowForm  
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate  import Migrate



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Shosho11@localhost:5432/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY;
engine = create_engine("postgresql://postgres:Shosho11@localhost:5432/postgres",pool_pre_ping=True)
Base = declarative_base()

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
    shows = db.relationship('Show', backref='venues', lazy=True)
   
def __repr__(self):
      return f'<Venue Name: {self.name}, City: {self.city}, State: {self.state}>'


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
    shows = db.relationship('Show', backref='artists', cascade='all, delete-orphan' , lazy=True)
 


class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'))
    start_time = db.Column(db.DateTime())
    artist_name=db.Column(db.String(120))
    venue_name=db.Column(db.String)
    artist_image_link=db.Column(db.String)
    
Session = sessionmaker(bind = engine)
session = Session()
db.create_all()



def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  result = session.query(Venue).all()
  return render_template('pages/venues.html', areas=result);
 
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
 
  search_term = request.form.get('search_term', '')
  results = (session.query(Venue).filter(Venue.name.like(f'%{search_term}%')).all())
  data = []

  for result in results:
    data.append({
      "id": result.id,
      "name": result.name,
    })
  response={
    "count": len(results),
    "data": data
  }
  print(response)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # pastShow=session.query(Show).filter(Show.start_time < datetime(),Show.venue_id==venue_id).all()
  # upcomingShows=session.query(Show).filter(Show.start_time > datetime(),Show.venue_id==venue_id).all()
  result =session.query(Venue).filter_by(id=venue_id).all()
  return render_template('pages/show_venue.html', venue=result)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  new_venue = Venue(
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    address=request.form.get('address'),
    phone=request.form.get('phone'),
    website=request.form.get('website_link'),
    facebook_link=request.form.get('facebook_link'),
    seeking_talent=request.form.get('seeking_talent') == 'y',
    image_link=request.form.get('image_link'),
    genres=request.form.getlist('genres'),
    seeking_description=request.form.get('seeking_description')
    )

  session.add(new_venue)
  session.commit()
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['DELETE','GET'])
def delete_venue(venue_id):

  session.query(Venue).filter_by(id=venue_id).delete()
  session.commit()
    
  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  result=session.query(Artist).all()
  return render_template('pages/artists.html', artists=result)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = (session.query(Artist).filter(Artist.name.like(f'%{search_term}%')).all())
  data = []

  for result in results:
    data.append({
      "id": result.id,
      "name": result.name,
    })
  response={
    "count": len(results),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # pastShow=session.query(Show).filter(Show.start_time < datetime.now(), Show.artist_id==artist_id).all()
  # upcomingShows=session.query(Show).filter(Show.start_time > datetime.now(), Show.artist_id==artist_id).all()
  data =session.query(Artist).filter_by(id=artist_id).all()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=session.query(Artist).get(artist_id)
  print(artist)
  Form = ArtistForm(
    name=artist.name,
    city=artist.city,
    state=artist.state,
    genres=artist.genres,
    phone=artist.phone,
    facebook_link=artist.facebook_link,
    website_link=artist.website,
    image_link=artist.image_link,
    seeking_talent=artist.seeking_talent,
    seeking_description=artist.seeking_description 
  )
  return render_template('forms/edit_artist.html', form=Form , artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = session.query(Artist).get(artist_id)
  form = request.form
  artist.name=form.get('name')
  artist.city=form.get('city')
  artist.state=form.get('state')
  artist.phone=form.get('phone')
  artist.website=form.get('website_link')
  artist.facebook_link=form.get('facebook_link')
  artist.seeking_talent=form.get('seeking_talent') == 'y'
  artist.image_link=form.get('image_link')
  artist.genres=form.getlist('genres')
  artist.seeking_description=form.get('seeking_description')
    
  session.add(artist)
  session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venues=session.query(Venue).get(venue_id)
  form = VenueForm(
    name=venues.name,
    city=venues.city,
    state=venues.state,
    genres=venues.genres,
    address=venues.address,
    phone=venues.phone,
    facebook_link=venues.facebook_link,
    website_link=venues.website,
    image_link=venues.image_link,
    seeking_talent=venues.seeking_talent,
    seeking_description=venues.seeking_description 
  )
 
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venues)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = session.query(Venue).get(venue_id)
  form = request.form
  venue.name=form.get('name')
  venue.city=form.get('city')
  venue.state=form.get('state')
  venue.address=form.get('address')
  venue.phone=form.get('phone')
  venue.website=form.get('website_link')
  venue.facebook_link=form.get('facebook_link')
  venue.seeking_talent=form.get('seeking_talent') == 'y'
  venue.image_link=form.get('image_link')
  venue.genres=form.getlist('genres')
  venue.seeking_description=form.get('seeking_description')
    
  session.add(venue)
  session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  new_Artist = Artist(
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    phone=request.form.get('phone'),
    website=request.form.get('website_link'),
    facebook_link=request.form.get('facebook_link'),
    seeking_talent=request.form.get('seeking_talent') == 'y',
    image_link=request.form.get('image_link'),
    genres=request.form.getlist('genres'),
    seeking_description=request.form.get('seeking_description')
    )

  session.add(new_Artist)
  session.commit()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
        # num_shows should be aggregated based on number of upcoming shows per venue.
  data=session.query(Show).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  new_Show = Show(
    venue_id=request.form['venue_id'],
    artist_id=request.form['artist_id'],
    start_time=request.form['start_time']
    )

  session.add(new_Show)
  session.commit()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
