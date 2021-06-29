from datetime import datetime
import os
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import DEBUG, Formatter, FileHandler
from forms import VenueForm ,ArtistForm,ShowForm  
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate  import Migrate
from models import Artist, Venue , Show


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
moment = Moment(app)
app.config.from_pyfile('config.py') 
app.config.from_object('config')


    
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
  result=db.session.query(Venue).all()
  return render_template('pages/venues.html', areas=result);
 
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
 
  search_term = request.form.get('search_term', '')
  results = (Venue.query.filter(Venue.name.like(f'%{search_term}%')).all())
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
  result =Venue.query.filter_by(id=venue_id).all()
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

  db.session.add(new_venue)
  db.session.commit()
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['DELETE','GET'])
def delete_venue(venue_id):

  db.session.query(Venue).filter_by(id=venue_id).delete()
  db.session.commit()
    
  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  result=Artist.query.all()
  return render_template('pages/artists.html', artists=result)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = (Artist.query.filter(Artist.name.like(f'%{search_term}%')).all())
  print(results)
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
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # pastShow=session.query(Show).filter(Show.start_time < datetime.now(), Show.artist_id==artist_id).all()
  # upcomingShows=session.query(Show).filter(Show.start_time > datetime.now(), Show.artist_id==artist_id).all()
  data =Artist.query.filter_by(id=artist_id).all()
  print(data)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=Artist.query.get(artist_id)
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
  artist = Artist.query.get(artist_id)
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
    
  db.session.add(artist)
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venues=Venue.query.get(venue_id)
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
  venue = Venue.query.get(venue_id)
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
    
  db.session.add(venue)
  db.session.commit()
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

  db.session.add(new_Artist)
  db.session.commit()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()
  print(data)
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

  db.session.add(new_Show)
  db.session.commit()
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