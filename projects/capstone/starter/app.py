import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)


  @app.route('/actors', methods=['GET'])
  def get_actors():
    actors = Actors.query.all()
    list_of_actors = []
    for actor in actors:
      list_of_actors.append(actor.format())
    return jsonify({'success': True,
                    'actors': list_of_actors})
  
  @app.route('/movies', methods=['GET'])
  def get_actors():
    movies = Movies.query.all()
    list_of_movies = []
    for movie in movies:
      list_of_movies.append(movie.format())
    return jsonify({'success': True,
                    'actors': list_of_movies})

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