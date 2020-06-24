import os
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def home():
    return 'Hello'
  

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors():
    actors = Actors.query.all()
    list_of_actors = []
    for actor in actors:
      list_of_actors.append(actor.format())
    return jsonify({'success': True, 'actors': list_of_actors})
  

  @app.route('/actors', methods = ['POST'])
  @requires_auth('post:actors')  
  def add_actor():
    data = request.get_json()
    new_name = data.get('name', None)
    new_age = data.get('age', None)
    new_gender = data.get('gender', None)
    new_actor = Actors(name = new_name, age = new_age, gender = new_gender)
    Actors.insert(new_actor)
    list_of_actors = Actors.query.all()
    return jsonify({'success': True, 'actors': list_of_actors})
  

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies():
    movies = Movies.query.all()
    list_of_movies = []
    for movie in movies:
      list_of_movies.append(movie.format())
    return jsonify({'success': True,
                    'movies': list_of_movies})


  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')  
  def add_movie():
    data = request.get_json()
    new_title = data.get('title', None)
    new_release_date = data.get('release_date', None)
    new_genre = data.get('genre', None)
    new_movie = Movies(title = new_title, release_date = new_release_date, genre = new_genre)
    Movies.insert(new_movie)
    list_of_movies = Movies.query.all()
    return jsonify({'success': True, 'movies': list_of_movies})
  

  @app.route('/actors/<int:actor_id>', methods = ['DELETE'])
  @requires_auth('delete:actor')  
  def del_actor(actor_id):
    data = request.get_json()
    actor_id = data.get('actor_id', None)
    try:
      actor = Actors.query.filter(Actors.actor_id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      actor.delete()
      list_of_actors = Actors.query.all()
      return jsonify({'success': True, 'actor_id': actor_id, 'actors': list_of_actors})
    except BaseException:
      abort(422)


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')  
  def del_movie(movie_id):
    data = request.get_json()
    movie_id = data.get('movie_id', None)
    try:
      movie = Movies.query.filter(Movies.movie_id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      movie.delete()
      list_of_movies = Movies.query.all()
      return jsonify({'success': True, 'movie_id': movie_id, 'actors': list_of_movies})
    except BaseException:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(actor_id):
    data = request.get_json()
    try:
      actor = Actors.query.filter(Actors.actor_id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      else: 
        if 'name' in data:
          actor.name = data.get('name')
        elif 'age' in data:
          actor.age = data.get('age')
        elif 'gender' in data:
          actor.gender = data.get('gender')
        actor.update()
      return jsonify({'success': True,
                      'actors': Actors.query.all()})
    except BaseException:
        abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(movie_id):
    data = request.get_json()
    try:
      movie = Movies.query.filter(Movies.movie_id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      else: 
        if 'title' in data:
          movie.title = data.get('title')
        elif 'age' in data:
          movie.release_date = data.get('release_date')
        elif 'gender' in data:
          movie.genre = data.get('genre')
        movie.update()
      return jsonify({'success': True,
                      'actors': Movies.query.all()})
    except BaseException:
        abort(422)


  #Error Handling
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422


  @app.errorhandler(404)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404


  @app.errorhandler(AuthError)
  def auth_error(ex):
    return jsonify({
      "success": False,
      "error": ex.status_code,
      "message": ex.error['code']
    }), 401
  return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)