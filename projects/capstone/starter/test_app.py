import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie
from app import create_app

database_name = "casting_agency_test"
database_path = "postgresql://{}/{}".format(
  'localhost:5432', database_name)


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents test cases for casting agency"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_actors(self):
        res = self.client().get('/api/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_for_invalid_page(self):
        res = self.client().get('/api/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not_found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
