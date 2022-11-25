import os
from unicodedata import category
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:{}/{}".format(
            'grimm@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    # test categories endpoint

    def test_categories(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

    def test_categories_fail(self):
        response = self.client().post('/categories')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The request method is known by the server but is not supported by the target resource.")

    # test questions endpoints
    def test_questions(self):
        response = self.client().get('/questions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

    def test_questions_fail(self):
        response = self.client().get('/question')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server can not find the requested resource.")

    def test_post_questions(self):
        _json = {
            "question": "Who are You?",
            "answer": " I dont know",
            "category": 2,
            "difficulty": 2
        }
        response = self.client().post('/questions', json=_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertIn('id', response.json['questions'])

    def test_post_questions_fail(self):
        _json = {
            "question": "Who are You?",
            "answer": " I dont know",
            "category": 2,
            "difficulty": 'sdsde'
        }
        response = self.client().post('/questions', json=_json)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server has encountered a situation it does not know how to handle.")

    def test_post_questions_fail1(self):
        _json = {"ser":"sdsd"}
        response = self.client().post('/questions', json=_json)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server has encountered a situation it does not know how to handle.")

    def test_search_questions(self):
        _json = {
            "searchTerm": "Who are You?"
        }
        response = self.client().post('/questions', json=_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertEqual(response.json['questions']
                         [0]['question'], _json['searchTerm'])

    def test_search_questions_fail(self):
        _json = {"ser":"sdsd"}
        response = self.client().post('/questions',json=_json)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server has encountered a situation it does not know how to handle.")

    def test_delete_question(self):
        id = Question.query.order_by(Question.id.desc()).first().id
        response = self.client().delete('/questions/{}'.format(id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

    def test_delete_question_fail(self):
        id = -1
        response = self.client().delete('/questions/{}'.format(id))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server can not find the requested resource.")

    def test_update_question(self):
        id = Question.query.order_by(Question.id.desc()).first().id
        _json = {
            "question": "Who are Youuuuu??????",
            "answer": " I dont know",
            "category": 2,
            "difficulty": 2
        }
        response = self.client().put('/questions/{}'.format(id),json=_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

    def test_update_question_fail(self):
        id = Question.query.order_by(Question.id.desc()).first().id
        response = self.client().put('/questions/{}'.format(id))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server has encountered a situation it does not know how to handle.")

    def test_question_category(self):
        response = self.client().get('/questions/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.json['questions'][0]['category']), 1)

    def test_question_category_fail(self):
        response = self.client().get('/questions/10')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The server can not find the requested resource.")

    def test_play(self):
        category = {}
        category['id'] = 3
        _json = {
            "quiz_category": category,
            "previous_questions": [3, 4]
        }
        response = self.client().post('/play', json=_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

    def test_play_fail(self):
        category = {}
        category['id'] = 3
        _json = {
            "quiz_category": category,
            "previous_questions": [3, 4]
        }
        response = self.client().get('/play', json=_json)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(
            response.json['message'], "The request method is known by the server but is not supported by the target resource.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
