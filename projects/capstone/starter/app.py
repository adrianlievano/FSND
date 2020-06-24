import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)


  @app.route('/actors', methods=['GET', 'POST'])
  def get_actors():
    actors = Actors.query.all()
    list_of_actors = []
    for actor in actors:
      list_of_actors.append(actor.format())
    try: 
      if request.get_json() is None:
        abort(422)
      else: 
        data = request.get_json()
        new_name = data.get('name', None)
        new_age = data.get('age', None)
        new_gender = data.get('gender', None)
        new_actor = Actors(name = new_name, age = new_age, gender = new_gender)
        Actors.insert(new_actor)
        list_of_actors = Actors.query.all()
        return jsonify({'success': True, 'actors': list_of_actors})
    return jsonify({'success': True,
                    'actors': list_of_actors})
  
  @app.route('/movies', methods=['GET', 'POST'])
  def get_movies():
    movies = Movies.query.all()
    list_of_movies = []
    for movie in movies:
      list_of_movies.append(movie.format())
    try: 
      if request.get_json() is None:
        abort(422)
      else: 
        data = request.get_json()
        new_title = data.get('title', None)
        new_release_date = data.get('release_date', None)
        new_genre = data.get('genre', None)
        new_movie = Movies(name = new_title, age = new_release_date, gender = new_genre)
        Movies.insert(new_actor)
        list_of_movies = Movies.query.all()
        return jsonify({'success': True, 'movies': list_of_movies})
    return jsonify({'success': True,
                    'movies': list_of_movies})

  @app.route('/actors/<int: actor_id>', methods = ['DELETE'])
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

  @app.route('/movies/<int: movie_id>', methods = ['DELETE'])
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

  # Error Handling
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