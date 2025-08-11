import unittest
from app import app, db
from app.models import User, Post, Category

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

class PostModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        # create a user and a category
        u = User(username='john', email='john@example.com')
        c = Category(name='Health')
        db.session.add(u)
        db.session.add(c)
        db.session.commit()

        # create a post
        p = Post(title="Test Post", content="This is a test post.", author=u, category=c)
        db.session.add(p)
        db.session.commit()

        # check the post
        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(Post.query.first().title, "Test Post")

if __name__ == '__main__':
    unittest.main(verbosity=2)
