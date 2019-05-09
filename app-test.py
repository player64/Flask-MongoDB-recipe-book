from app import app
import unittest
# https://medium.com/@piotrkarpaa/unit-testing-python-flask-web-api-with-mockupdb-c2cb72600854
# http://blog.paulopoiati.com/2013/02/22/testing-flash-messages-in-flask/
# https://www.patricksoftwareblog.com/unit-testing-a-flask-application/

class MyTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
