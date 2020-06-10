import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #Test /category/<int:category_id>/questions endpoint
    def test_question_search_by_category(self):
        res = self.client.post('category/1/questions')
        data = json.loads(res.data)

        assertEqual(data['success'], True)
        assertTrue(data['questions'])

    def test_404_question_search_by_invalid_category(self):
        res = self.client.post('category/1000/questions')
        data = json.loads(res.data)

        assertEqual(data['success'], False)
        assertEqual(data['error'], 404)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
