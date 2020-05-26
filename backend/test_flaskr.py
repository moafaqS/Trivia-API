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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))


    def test_get_questions(self):

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'] , 'Not Found')


    def test_delete_question(self):
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],6)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question , None)

    def test_delete_non_exist_question(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')

    def test_post_new_question(self):
        question = {
                "answer": "Riadh", 
                "category": 1, 
                "difficulty": 1, 
                "question": "what is the capital of saudi arabia"
                }

        res = self.client().post('/questions' , json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))

    def test_not_allowed_post_question(self):
        question = {
                "answer": "Riadh", 
                "category": 1, 
                "difficulty": 1, 
                "question": "what is the capital of saudi arabia"
                }

        res = self.client().post('/questions/100' , json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')

    def test_search(self):
        search = {'searchTerm' : 'title'}

        res = self.client().post('/questions/search' , json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))

    def test_search_not_found(self):
        search = {'searchTerm' : 'timdfhbsfdysgfygsduyfgyutle'}

        res = self.client().post('/questions/search' , json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'],False)

    def test_questions_per_categorie(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])


    def test_questions_per_not_exist_categorie(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')






       

       






        
        
        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()