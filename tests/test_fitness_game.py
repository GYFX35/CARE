import unittest
from unittest.mock import patch
from app import app, db
from app.models import User

class FitnessGameCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['OPENAI_API_KEY'] = 'dummy'
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fitness_game_page_loads_for_logged_in_user(self):
        # Create a user and log in
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()
        self.client.post('/login', data={'username': 'susan', 'password': 'cat'}, follow_redirects=True)

        # Access the fitness game page
        response = self.client.get('/fitness_game', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fitness Challenge', response.data)

    def test_fitness_game_page_redirects_for_anonymous_user(self):
        # Access the fitness game page without logging in
        response = self.client.get('/fitness_game', follow_redirects=True)
        self.assertIn(b'Sign In', response.data)

    @patch('openai.resources.chat.completions.Completions.create')
    def test_fitness_coach_endpoint(self, mock_create):
        # Configure the mock to return a fake response
        class MockMessage:
            def __init__(self, content):
                self.content = content

        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)

        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]

        mock_create.return_value = MockResponse('A squat is a great exercise!')

        # Create a user and log in
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()
        self.client.post('/login', data={'username': 'susan', 'password': 'cat'}, follow_redirects=True)

        # Send a message to the fitness coach
        response = self.client.post('/fitness_coach', data={'message': 'What is a squat?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A squat is a great exercise!', response.data)

if __name__ == '__main__':
    unittest.main()
