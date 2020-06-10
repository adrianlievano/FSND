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
    #Test get categories endpoint
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)
        assertEqual(data['success'], True)
        assertEqual(data['status_code'], 200)
        assertTrue(date['total_questions'])

    #Test get questions endpoint
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)
        assertEqual(data['success'], True)
        assertEqual(data['status_code'], 200)
        assertTrue(date['total_questions'])

    #Test delete functionality of /questions/<int: question_id> endpoint
    def test_delete_question(self):
        res = self.client.post('/questions', json = {'question': 'What is a test question give?'
                                                         'answer': 'A test answer.'
                                                        'category': 1,
                                                        'difficulty': 5})
        data = json.loads(res.data)
        question_id = data['created']
        del_res = self.client.delete('/questions/question_id')

        data_del = json.loads(del_res.data)
        assertEqual(data_del['success'], True)
        assertEqual(data_del['status_code'], 200)

    #Test add functionality of /questions endpoint
    def test_add_question(self):
        res = self.client.post('/questions', json = {'question': 'What is a test question give?'
                                                         'answer': 'A test answer.'
                                                        'category': 1,
                                                        'difficulty': 5})
        data = json.loads(res.data)
        assertEqual(data['success'], True)
        assertTrue(data['total_questions'])
        assertTrue(data['category'])

    #Test search functionality of /questions endpoint
    def test_question_search_by_term(self):
        res = self.client.post('/questions', json = {'searchTerm': 'actor'})
        data = json.loads(res.data)
        assertEqual(data['success'], True)
        assertEqual(data['status_code'], 200)

    def test_question_invalid_search_422_by_term(self):
        res = self.client.post('/questions', json = {'searchTerm': 'Godzilla'})
        data = json.loads(res.data)
        assertEqual(data['success'], False)
        assertEqual(data['status_code'], 404)

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

    #Test /quizzes endpoints
    def test_quiz_render_by_category(self):
        res = self.client.post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        assertEqual(data['success'], True)
        assertTrue(data['status_code'], 200)
    def test_quiz_render_404_error_by_category(self):
        res = self.client.post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category': {'id': 999}})
        data = json.loads(res.data)
        assertEqual(data['success'], False)
        assertTrue(data['status_code'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
