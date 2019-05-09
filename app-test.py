from app import app
import unittest
from forms import RegistrationForm, LoginForm, RecipeForm
from werkzeug.datastructures import MultiDict
# import re

# https://medium.com/@piotrkarpaa/unit-testing-python-flask-web-api-with-mockupdb-c2cb72600854
# http://blog.paulopoiati.com/2013/02/22/testing-flash-messages-in-flask/
# https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
# http://flask.pocoo.org/docs/1.0/testing/
# https://realpython.com/python-web-applications-with-flask-part-iii/

# ALL ASSERT LIST
# https://www.mattcrampton.com/blog/a_list_of_all_python_assert_methods/
# https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index

class MyTestCase(unittest.TestCase):
    """\
        def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, b'Hello World!')
"""
    """
    from flask import jsonify
    
    @app.route("/dummy")
    def dummy(): 
        return jsonify({"dummy":"dummy-value"})
        
    def setUp(self):
        my_app.app.config['TESTING'] = True
        self.app = my_app.app.test_client()

    def test_dummy(self):
        response = self.app.get("/dummy")
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['dummy'], "dummy-value")
    """
    def setUp(self):
        username = 'mariusz'
        self.username = username

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_form(self):
        tester = app.test_client(self)
        form_data = [
            ('username', ''),
            ('password', '')
        ]
        form = LoginForm(MultiDict(form_data))

        data = dict(username='mark', password='ddd867490')
        response = tester.post('/login', data=data, follow_redirects=True)
        # self.assertTrue(re.search('Wrong username or password', response.get_data(as_text=True)))
        self.assertIn(b'Wrong username or password', response.data)
        self.assertEqual(response.status_code, 200)
        # form = LoginForm(response)
        # validate = form.validate()
        # print(response.get_data(as_text=True))
        # print(form.errors)
        self.assertFalse(form.validate())
        # self.assertFalse(1,1)

    def test_view_recipe(self):
        tester = app.test_client(self)
        response = tester.get('/recipe/5cd36d89162429d92fb1465b')
            # with c.session_transaction() as sess:

        print(self.username)
        # print(session['recipe_views'])
        self.assertIn(b'Lemon bars', response.data)



if __name__ == '__main__':
    unittest.main()
