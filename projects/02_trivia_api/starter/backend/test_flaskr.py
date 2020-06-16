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
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
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

    # Test get categories endpoint
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_categories'])

    # Test get questions endpoint
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])

    # Test delete functionality of /questions/<int: question_id> endpoint
    def test_delete_question(self):
        res = self.client().post('/questions', json={'question': 'What?',
                                                   'answer': 'Yo',
                                                   'category': 1,
                                                   'difficulty': 5})
        data = json.loads(res.data)
        question_id = data['question_id']
        query_string = ('/questions/{}').format(question_id)
        del_res = self.client().delete(query_string)

        data_del = json.loads(del_res.data)
        self.assertEqual(data_del['success'], True)
        self.assertEqual(res.status_code, 200)

    # Test add functionality of /questions endpoint
    def test_add_question(self):
        res = self.client().post('/questions', json={'question': 'What?',
                                                   'answer': 'A test answer.',
                                                   'category': 1,
                                                   'difficulty': 5})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
    # Test search functionality of /questions endpoint
    def test_question_search_by_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'actor'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_question_invalid_search_422_by_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'Godzilla'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)

    # Test /category/<int:category_id>/questions endpoint
    def test_question_search_by_category(self):
        res = self.client().get('/category/1/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_404_question_search_by_invalid_category(self):
        res = self.client().post('category/1000/questions')
        self.assertEqual(res.status_code, 404)

    # Test /quizzes endpoints
    def test_quiz_render_by_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
                                                 'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
