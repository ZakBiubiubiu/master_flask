import unittest
from webapp.models import db, User, Role

from webapp import create_app
from webapp.exts import admin, rest_api
from webapp.models import db


class TestURLs(unittest.TestCase):

    def setUp(self):
        admin._views = []
        rest_api.resources = []
        app = create_app('webapp.config.TestConfig')
        self.client = app.test_client()

        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_redirect(self):

        result = self.client.get('/')
        assert result.status_code == 302
        assert '/blog/' in result.headers['Location']

    def test_login(self):
        'test if the login form works correctly'
        test_role = Role('default')
        db.session.add(test_role)
        db.session.commit()

        test_user = User('test')
        test_user.set_password('test')
        db.session.add(test_user)
        db.session.commit()

        result = self.client.post('/login', data=dict(
            username='test',
            password='test'
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('你已经穿好衣服可以见人了', result.data.decode())


if __name__ == '__main__':
    unittest.main()

