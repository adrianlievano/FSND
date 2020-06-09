#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import Venue, Artist, Show, db_setup

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
db = db_setup(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  rows = Venue.query.distinct(Venue.city, Venue.state).order_by(Venue.city).all()
  data = []

  for row in rows:
        city = row.city
        state = row.state
        venues = db.session.query(Venue).filter(Venue.city == city)
        for venue in venues:
            venue_id = venue.id
            venue_name = venue.name
            listOfUpcomingShows = Venue.query.join(Show, Show.venue_id == Venue.id).filter(Show.start_time > datetime.utcnow()).all()
            print(listOfUpcomingShows)

            data.append({
                        'city': city,
                        'state': state,
                        'venues': [{'id': venue_id,
                                    'name': venue_name,
                                    'num_upcoming_shows':len(listOfUpcomingShows)}]                                        })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  tag = request.form.get('search_term', None)
  search_term = "%{}%".format(tag)
  query_search = db.session.query(Venue).filter(Venue.name.ilike(search_term)).all()
  count_venues = len(query_search)
  now = datetime.utcnow()
  data = []
  for venue in query_search:
      datum = {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": 0,
      }
      data.append(datum)

  response = {'count':count_venues,
                'data': data}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter(Show.venue_id == venue_id).all()
  now = datetime.utcnow()

  upcoming_shows_list = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time > now).all()
  past_shows_list = db.session.query(Show, Artist).join(Artist).filter(venue_id == Show.venue_id).filter(Show.start_time < now).all()

  upcoming_list = list()
  for show in upcoming_shows_list:
      data = {'artist_id': show.Show.artist_id,
      'artist_name': show.Artist.name,
      'artist_image_link': show.Artist.image_link,
      'start_time': str(show.Show.start_time)}
      upcoming_list.append(data)
  #
  past_list = list()
  for show in upcoming_shows_list:
      data = {'artist_id': show.Show.artist_id,
      'artist_name': show.Artist.name,
      'artist_image_link': show.Artist.image_link,
      'start_time': str(show.Show.start_time)}
      past_list.append(data)

  data = {'id': venue.id,
                'name':venue.name,
                'genres': ['Test1', 'Test2'],
                'address': venue.address,
                'city': venue.city,
                'state': venue.state,
                'phone': venue.phone,
                'website': venue.website,
                'facebook_link': venue.facebook_link,
                'seeking_talent': venue.seeking_talent,
                'seeking_description': venue.seeking_description,
                'image_link': venue.image_link,
                'past_shows': past_list,
                'upcoming_shows': upcoming_list,
                'past_shows_count': len(past_list),
                'upcoming_shows_count': len(upcoming_list)}
  result = data

  return render_template('pages/show_venue.html', venue=result)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False

  try:
      new_venue = Venue(name = request.form['name'],
                        city = request.form['city'],
                        state = request.form['state'],
                        #genres = request.form.getlist('genres'),
                        address = request.form['address'],
                        phone = request.form['phone'],
                        facebook_link= request.form['facebook_link'])
                        #seeking_talent= request.form['seeking_talent'],
                        #seeking_description = request.form['seeking_description'],
                        #website= request.form['website'],
                        #image_link= request.form['image_link'])

      db.session.add(new_venue)
  except:
      error = True
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
  finally:
      if not error:
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
          db.session.close()
  return render_template('pages/home.html')

#TODO
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      Venue.query.filter_by(id = venue_id).delete()
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.all()
  data = []
  for artist in artists:
      datum = {'id':artist.id,
               'name': artist.name}
      data.append(datum)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  tag = request.form.get('search_term', None)
  search_term = '%' + tag + '%'
  now = datetime.utcnow()
  data_list = db.session.query(Artist).filter(Artist.name.ilike(search_term)).all()
  count_artist = len(data_list)
  data = []

  for artist in data_list:
      numUpcomingShows = len(Show.query.join(Artist, Artist.id == Show.artist_id).filter(Show.artist_id == artist.id).filter(Show.start_time > now).all())
      datum = {'id': artist.id,
                'name': artist.name,
                'num_upcoming_shows': numUpcomingShows
                }
      data.append(datum)

  response={
        'count': count_artist,
        'data': data}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter(Show.artist_id == artist_id).all()

  now = datetime.utcnow()
  past_shows_list = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < now).all()
  upcoming_shows_list = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > now).all()

  past_list = list()
  for show in past_shows_list:
     data = {'venue_id': show.Show.Venue.id,
     'venue_name': show.Venue.name,
     'venue_image_link': show.Venue.image_link,
     'start_time': show.Show.start_time}
     past_list.append(data)

  upcoming_list = list()
  for show in upcoming_shows_list:
     data = {'venue_id': show.Show.Venue.id,
     'venue_name': show.Venue.name,
     'venue_image_link': show.Venue.image_link,
     'start_time': show.Show.start_time}
     upcoming_list.append(data)


  datum = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_list,
    "upcoming_shows": upcoming_list,
    "past_shows_count": len(past_list),
    "upcoming_shows_count": len(upcoming_list)}

  data = list(datum)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  qartist = Artist.query.get(artist_id)
  artist={
    "id": qartist.id,
    "name": qartist.name,
    "genres": qartist.genres,
    "city": qartist.city,
    "state": qartist.state,
    "phone": qartist.phone,
    "website": qartist.website,
    "facebook_link": qartist.facebook_link,
    "seeking_venue": qartist.seeking_venue,
    "seeking_description": qartist.seeking_description,
    "image_link": qartist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  form = request.form.to_dict(True)
  genres = request.form.getlist('genres')

  try:
      artist = Artist.query.get(artist_id)
      artist.name = form['name']
      artist.city = form['city']
      artist.state = form['state']
      artist.phone = form['phone']
      artist.website = form['website']
      artist.facebook_link = form['facebook_link']
      artist.seeking_venue = form['seeking_venue']
      artist.seeking_description = form['seeking_description']
      artist.image_link = form['image_link']
      artist.genres = list(genres)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      flash('Error. Artist ' + form['name'] + ' could not be updated.')
  finally:
      if not error:
          db.session.close()
          flash('Artist ' + form['name'] + ' was successfully updated.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  qvenue = Venue.query.get(venue_id)
  venue = {
    'id': qvenue.id,
    'name': qvenue.name,
    'genres': qvenue.genres,
    'address': qvenue.address,
    'city': qvenue.city,
    'state': qvenue.state,
    'phone': qvenue.phone,
    'website': qvenue.website,
    'facebook_link': qvenue.facebook_link,
    'seeking_talent': qvenue.seeking_talent,
    'seeking_description': qvenue.seeking_description,
    'image_link': qvenue.image_link
    }

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  error = False
  try:
      venue = Venue.query.get(venue_id)
      venue.name = request.form['name'],
      venue.genres = request.form['genres']
      venue.address = request.form['address']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.phone = request.form['phone']
      venue.website = request.form['website']
      venue.facebook_link = request.form['facebook_link']
      venue.seeking_talent = request.form['seeking_talent']
      venue.seeking_description = request.form['seeking_description']
      venue.image_link = request.form['image_link']
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      flash('Error. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
      if not error:
          db.session.close()
          flash('Artist ' + request.form['name'] + ' was successfully updated.')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
      new_artist = Artist(id = request.form['id'],
             name = request.form['name'],
             city = request.form['city'],
             state = request.form['state'],
             phone = request.form['phone'],
             genres = request.form['genres'],
             image_link = request.form['image_link'],
             facebook_link = request.form['facebook_link'],
             seeking_description = request.form['seeking_description'],
             seeking_venue = request.form['seeking_venue'],
             website_link = request.form['website_link']
            )
      db.session.add(new_artist)

  except:
        error = True
        flash('Error. Could not add artist ' + request.form['name'])
        db.session.rollback()
  finally:
      if not error:
          db.session.commit()
          flash('Successfully added new artist ' + request.form['name'])
          db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = db.session.query(Show, Artist, Venue).join(Artist).join(Venue).all()
  for show in shows:
      datum = {'venue_id': show.Show.venue_id,
                'venue_name': show.Venue.name,
                'artist_id': show.Show.artist_id,
                'artist_name': show.Artist.name,
                'artist_image_link': show.Artist.image_link,
                'start_time': str(show.Show.start_time)}
      data.append(datum)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
      Show(venue_id = request.form['venue_id'],
      artist_id = request.form['artist_id'],
      start_time = request.form['start_time'])
  except:
      error = True
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()
  finally:
      if not error:
          db.session.commit()
          flash('Show was successfully listed!')
          db.session.close()
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
