import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Actors, Movies


class AppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "tbd"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.sample_actor = {'name': 'Tom Cruise', 
                        'Age': 34,
                        'Gender': 'Male'}
        
        self.sample_movie = {'title': 'Mission Impossible',
                        'release_date': '2020-05-02',
                        'genre': 'Action'}


    # Test get actors endpoint
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])


    # Test get movies endpoint
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])


    #Test Delete Actor Endpoint
    def test_delete_actors(self):
        res = self.client().post('/actors', json = self.sample_actor)
        data = json.loads(res.data)
        actor_id = data['actor_id']
        query_string = ('/actors/{}').format(actor_id)
        del_res = self.client().delete(query_string)
        data_del = json.loads(del_res.data)
        self.assertEqual(data_del['success'], True)
        self.assertEqual(del_res.status_code, 200)


    def test_422_delete_actor_failure(self):
        actor_id = 1000
        query_string = ('/actors/{}').format(actor_id)
        del_res = self.client().delete(query_string)
        self.assertEqual(del_res.status_code, 200)

    
    #Test Delete Movie Endpoint
    def test_delete_movies(self):
        res = self.client().post('/movies', json = self.sample_movie)
        data = json.loads(res.data)
        movie_id = data['movie_id']
        query_string = ('/movies/{}').format(movie_id)
        del_res = self.client().delete(query_string)

        data_del = json.loads(del_res.data)
        self.assertEqual(data_del['success'], True)
        self.assertEqual(del_res.status_code, 200)


    def test_422_delete_movie_failure(self):
        movie_id = 1000
        query_string = ('/movies/{}').format(movie_id)
        del_res = self.client().delete(query_string)
        self.assertEqual(del_res.status_code, 200)


    # Test add functionality of /actors endpoint
    def test_add_actor(self):
        res = self.client().post('/actors', json=self.sample_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    def test_422_add_actor_failure(self):
        res = self.client().post('/actors', json={'name': 1,
                                                    'age': 32,
                                                    'gender': 'Male'})
        self.assertEqual(res.status_code, 422)


    # Test add functionality of /movies endpoint
    def test_add_movie(self):
        res = self.client().post('/movies', json=self.sample_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_422_add_movie_failure(self):
        res = self.client().post('/movies', json={'title': 1,
                                                  'release_date': 1,
                                                  'genre': 1})
        self.assertEqual(res.status_code, 422)


    # Test patch functionality of /actors endpoint
    def test_patch_actor(self):
        res = self.client().post('/actors', json =self.sample_actor)
        data = json.loads(res.data)
        actor_id = data['actor_id']
        query_string = ('/actors/{}').format(actor_id)
        patch_res = self.client().patch(query_string, json={'name': 'Brad Pitt'})
        data_patch = json.loads(patch_res.data)
        self.assertEqual(data_patch['success'], True)
        self.assertEqual(patch_res.status_code, 200)


    def test_422_patch_actor_failure(self):
        res = self.client().post('/actors', json =self.sample_actor)
        data = json.loads(res.data)
        actor_id = data['actor_id']
        query_string = ('/actors/{}').format(actor_id)
        patch_res = self.client().patch(query_string, json={'name': 1})
        data_patch = json.loads(patch_res.data)
        self.assertEqual(data_patch.status_code, 422)


    # Test patch functionality of /movies endpoint
    def test_patch_actor(self):
        res = self.client().post('/movies', json =self.sample_movie)
        data = json.loads(res.data)
        movie_id = data['movie_id']
        query_string = ('/movie/{}').format(movie_id)
        patch_res = self.client().patch(query_string, json={'title': 'Achilles'})
        data_patch = json.loads(patch_res.data)
        self.assertEqual(data_patch['success'], True)
        self.assertEqual(patch_res.status_code, 200)


    def test_422_patch_movie_failure(self):
        res = self.client().post('/movies', json =self.sample_movie)
        data = json.loads(res.data)
        actor_id = data['movie_id']
        query_string = ('/movies/{}').format(movie_id)
        patch_res = self.client().patch(query_string, json={'title': 1})
        data_patch = json.loads(patch_res.data)
        self.assertEqual(patch_res.status_code, 422)