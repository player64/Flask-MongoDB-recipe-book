from app import app
import unittest
from forms import RegistrationForm, LoginForm, RecipeForm
from werkzeug.datastructures import MultiDict
from dotenv import load_dotenv
import os
import json


class AppTestCase(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.tester = app.test_client(self)
        self.test_example_author_recipe_id = '5cd36d89162429d92fb1465b'
        self.test_example_other_recipe_id = '5ccf2d60ceda74b3755a11c9'

    def authenticate(self):
        valid_credits = {
            'username': os.getenv('TEST_USERNAME'),
            'password': os.getenv('TEST_PASSWORD')
        }
        return self.tester.post('/login', data=valid_credits, follow_redirects=True)

    def test_login(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        invalid_credits = {
            'username': 'test_user',
            'password': 'test'
        }
        response = self.tester.post('/login', data=invalid_credits, follow_redirects=True)
        self.assertIn(b'Wrong username or password', response.data)
        valid_login = self.authenticate()
        self.assertIn(b'Successfully logged in', valid_login.data)

    def test_register_login_taken(self):
        form_data = {
            'username': os.getenv('TEST_USERNAME'),
            'password': 'test_password',
            'confirm': 'test_password'
        }
        response = self.tester.post('/register', data=form_data, follow_redirects=True)
        self.assertIn(b'is already registered', response.data)

    def test_api_vote(self):
        response = self.tester.get('/api/recipe-vote', content_type='html/text')
        self.assertIn(b'method is not allowed', response.data)

        json_response = self.tester.post('/api/recipe-vote', content_type='/api/recipe-vote')
        self.assertIn('application/json', json_response.content_type)
        data = json.loads(json_response.get_data(as_text=True))
        should_response = {
            'status': 'error',
            'message': 'You need to login to vote for the recipe'
        }
        self.assertDictEqual(data, should_response)

        # authenticate
        self.authenticate()
        # this should return not valid vote author can't vote for own recipes
        json_response = self.tester.post('/api/recipe-vote', data=dict(id=self.test_example_author_recipe_id),
                                         content_type='application/x-www-form-urlencoded')
        data = json.loads(json_response.get_data(as_text=True))
        self.assertEqual(data['message'], 'An error occurred. Please try again')

        # valid vote
        json_response = self.tester.post('/api/recipe-vote', data=dict(id=self.test_example_other_recipe_id),
                                         content_type='application/x-www-form-urlencoded')
        data = json.loads(json_response.get_data(as_text=True))
        self.assertTrue('votes' in data)
        self.assertGreaterEqual(data['votes'], 0)

    def test_index(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_recipe(self):
        should_redirect = self.tester.get('/recipe/add')
        self.assertEqual(should_redirect.status_code, 302)
        self.authenticate()
        response = self.tester.get('/recipe/add')
        self.assertIn(b'Add recipe', response.data)

    def test_view_recipe(self):
        tester = app.test_client(self)
        response = tester.get('/recipe/5cd36d89162429d92fb1465b')
        self.assertIn(b'Lemon bars', response.data)


if __name__ == '__main__':
    unittest.main()
