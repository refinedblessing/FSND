import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie
from app import create_app
from auth import gen_token

database_name = "casting_agency_test"
database_path = "postgresql://{}/{}".format(
  'localhost:5432', database_name)

director = {
    "username": "castingd@gmail.com",
    "password": "CastingD@1"
}

producer = {
    "username": "castinga@gmail.com",
    "password": "Casting@1"
}


director_role_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpHS2R3YkZZVnFveG85eDNEWG8tcyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRlbnYuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZjkwYjI5YWI1ZDhjMDAxOWM5OGVlNSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTkzMzkzMjcxLCJleHAiOjE1OTM2NTI0NzEsImF6cCI6Ik5pWjl5YlFsYWJsNHUyQTZDa0xaSjZIOWVTbXZadEV1IiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.uggiD_yhO_Ffl-eLJdWAEi3risTm0kUb_KJU5NpdgmTiuyWR66iB0cB_eixC73kFPO9sEXT09JVpbd1ptofVYaM9lEA-Mx7tVfIKnbQ5nlEHj98VZ3Jt6yPr6qHApr4UjXTBGKpi3MvpwW4vDCL7DCWjaktYOB48Wtkaex-77oS5s1pZTT2rjSQD9PWc4Hdh3qJFYjVhxjWdPxaVrt-m22qw6XyXvyTDSxPDptHrO3TnaHPqojZ0YdNJlYCajgiDJqyOErL9QCxhcqeB3FbQaePxxPLmsLKht8zqX14Ddov3xFiMjlh9ZmOhSSPOfZroLycSq1EJ3VvjJn6QJoiaCQ'
producer_role_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpHS2R3YkZZVnFveG85eDNEWG8tcyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRlbnYuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZjhmYmJkZTgyNGE1MDAxOTIxMmVhZCIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTkzMzkzNzExLCJleHAiOjE1OTM2NTI5MTEsImF6cCI6Ik5pWjl5YlFsYWJsNHUyQTZDa0xaSjZIOWVTbXZadEV1IiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.TJiDy8sqJWEacb-Jp4qyZxj7Fq9k49yx6iZT2zyWre3TT2DAtXRXgy2jh5a-LERws36G93w3KL__4Ei6zsUTjtXfutH0qQCzGoT1a3ogvyKaCp8HlHHlLRd92MfmwAltsVaLMnpuQu_e5KoXSPwQ-AEISvjBGh5RoFWAvGOCvoMBWb4pqPMxvVyRhj0zNVi7ALEbD-lwVeBr377T0PltxcvvTxg7nCb8ydpnzJtmWaII80s84a9_qeCl10SwBhNIJxL7FrNTQDgkg31xg6U2Ee4uvgNql0hTN5NkVRuRwDHoD5_BJNtUK6yR05s5z9JG8oooka7c9N4a91Ry-DbLRg'
# director_role_token = ''
# producer_role_token = ''


# def setToken():
#     director_role_token = gen_token(director)
#     producer_role_token = gen_token(producer)


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents test cases for casting agency"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        # setToken()

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

    def test_get_actor(self):
        res = self.client().get('/api/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['id'], 1)

    def test_get_actor_invalid_id(self):
        res = self.client().get('/api/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor_by_director(self):
        a = Actor(
            name="James Bond", age=10, gender="male"
        )
        a.insert()
        actor_id = str(a.format()['id'])
        res = self.client().delete(
          '/api/actors/' + actor_id,
          headers={"Authorization": "Bearer " + director_role_token}
        )

        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], a.format()['id'])
        self.assertEqual(actor, None)

    def test_delete_actor_by_producer(self):
        a = Actor(
            name="James Bond", age=10, gender="male"
        )
        a.insert()
        actor_id = str(a.format()['id'])
        res = self.client().delete(
          '/api/actors/' + actor_id,
          headers={"Authorization": "Bearer " + producer_role_token}
        )
        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], a.format()['id'])
        self.assertEqual(actor, None)

    def test_delete_invalid_id_actor(self):
        res = self.client().delete(
          '/api/actors/1000',
          headers={"Authorization": "Bearer " + director_role_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not_found')

    def test_delete_actor_no_token(self):
        res = self.client().delete('/api/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
          data['message']['code'], 'authorization_header_missing')

    def test_create_actor_by_director(self):
        res = self.client().post(
          '/api/actors',
          json={"name": "John Doe", "age": 44, "gender": "male"},
          headers={"Authorization": "Bearer " + director_role_token}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['age'], 44)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_create_actor_by_producer(self):
        res = self.client().post(
          '/api/actors',
          json={"name": "John Doe", "age": 44, "gender": "male"},
          headers={"Authorization": "Bearer " + producer_role_token}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['age'], 44)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_create_invalid_actor(self):
        res = self.client().post('/api/actors', json={
            'actor': 'actor',
          },
          headers={"Authorization": "Bearer " + producer_role_token}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_actor_invalid_token(self):
        res = self.client().post('/api/actors', json={
          "name": "John Doe", "age": 44, "gender": "male"},
          headers={"Authorization": "Bearer "}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 'Token not found.')

    def test_patch_actor_by_director(self):
        res = self.client().patch(
          '/api/actors/1',
          json={"name": "John David"},
          headers={"Authorization": "Bearer " + director_role_token}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], "John David")

    def test_patch_actor_invalid_id(self):
        res = self.client().patch(
          '/api/actors/80000',
          json={"name": "John David"},
          headers={"Authorization": "Bearer " + director_role_token}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/api/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_invalid_page(self):
        res = self.client().get('/api/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not_found')

    def test_get_movie(self):
        res = self.client().get('/api/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 1)

    def test_get_movie_invalid_id(self):
        res = self.client().get('/api/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
