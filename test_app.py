import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, MovieActor

database_name = "database_test.db"
executive_producer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpJeG9GTldGamRFcjYxZzFHU00tQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtOTAuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZWQ4OGI4MmRhOWJiMDAxMzY4OWJiYiIsImF1ZCI6IkNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE1OTI2NjU1MjUsImV4cCI6MTU5MjY3MjcyNSwiYXpwIjoiQlBhS2dvSFI5Z1EwOEdtWEROMWtHR2QxS2dYdzY2cWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.lo9HuWOVjuQi2UbYjD-nrEDLiMLv3TGbLEWSZoGdinhdiY-3qSvOFqloIAyqJN-iwJ1Xj8iRDaSiUEorBGc0hfLUQFleM2wb2MdDMNEfDyD6-35sBG2gy5DKBtdljxUoK3PiBCNlbDJZaLtypYqxehLl1Hdn9r7OpZkkbBv8Qr-mUlXexQghRbEBGkaYPO9R6oHWqa8ee98r712Q5D7nD1MchUNfAgvE2MrYp4SHu4fnGYcKvldRgBNSSrFiL9VhtfWMtOhwg_6z3Vddl8Vn_qRZTIiIZfm3wlUxIiDx9CILMj1USb7vc8mpvsotLHVniCJB1lgrsfJDmB1YL_f5tA'}
casting_director_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpJeG9GTldGamRFcjYxZzFHU00tQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtOTAuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZWQ4OTE4YTdjM2M1MDAxOWNlY2U2OCIsImF1ZCI6IkNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE1OTI2NjU3OTIsImV4cCI6MTU5MjY3Mjk5MiwiYXpwIjoiQlBhS2dvSFI5Z1EwOEdtWEROMWtHR2QxS2dYdzY2cWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvciIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSJdfQ.PPZhuu8gLlyprzz2WcPu-GjLKQWlsV26FiANJR3IROeHRuaDJU3bQ8_A-61ctYsZd73rOHO-mhiaaMM5Gq1B-OzKlp6HP4bjvs2c4iQ4YXeRTxNZnWhiHwpNH8yKUcyA9bZasZIKPcicFrnkjPVnfkTIlLYKo4UzLYB94JAp63-gPapRWW2IAVX0NB3GbTUkqHxoDG_rnSBgtuxxr6lnl9gCWgh0-gW3dNgFG0hI4HZg1YLL2UcGArHUrg9jZ8fs9LwNpPpvaUGxl7dg9bylp2tQIqaVXfjD49fd2240uwmNHw4wNioNU2OuQBUglQtGsCmNvIBnBhyZfbigJe_YkQ'}
casting_assistant_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpJeG9GTldGamRFcjYxZzFHU00tQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtOTAuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZWQ4ODE1YTdjM2M1MDAxOWNlY2RiMiIsImF1ZCI6IkNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE1OTI2NjU2ODIsImV4cCI6MTU5MjY3Mjg4MiwiYXpwIjoiQlBhS2dvSFI5Z1EwOEdtWEROMWtHR2QxS2dYdzY2cWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.nNRHnpidBzjrfzf51Y8mopSn6hqDiwxabDHgdkGB4YuZA1bHjWjeaBdfu38W7hJzpO9ZtElwuZTEATxIssUcW17GDdad1sWM_yT7ZCCXeYjJv9xf6uiKGrmQF76kBPishOzRc5LyaQgHAPPYMO59B3kriX5MHuphG5rNWozBIoV9iQcQVB-exNxmwaeQ2U04tBUFnCZnvkkCzF6D4W4CN04t13iQ5GBOvwbDMh2hKSysnWM_X93w0yh0cHtRKsmaPc_rThcCScwnnRQEQ-maujmFjI-qY6vADkyMV-yIEtnQEPiW_hD07da261iDRRIujeCzyEvM92PKYxoW3YqNfg'}


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(None, database_name)
        self.client = self.app.test_client
        setup_db(self.app, "database_test.db")

        self.new_movie = {
            'title': 'Rush Hour',
            'release_date': '1989-09-18'
        }

        self.new_actor = {
            'name': 'Chris Tucker',
            'age': 48,
            'gender': 'Male'
        }

        self.new_movieActor = {
            'movie_id': 1,
            'actor_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_movies_method_not_allowed(self):
        res = self.client().get('/movies/1',
                                headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_movies_casting_director(self):
        res = self.client().get('/movies',
                                headers=casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=executive_producer_headers)
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/1', json=self.new_movie,
                                 headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_movie_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        mv = Movie.query.first()
        res = self.client().patch('/movies/'+str(mv.id), json=self.new_movie,
                                  headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movies_if_not_exist(self):
        res = self.client().patch('/movies/89', json=self.new_movie,
                                  headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movies(self):
        mv = Movie.query.first()
        res = self.client().delete('/movies/'+str(mv.id),
                                   headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_if_not_exist(self):
        res = self.client().delete('/movies/89',
                                   headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_actors_method_not_allowed(self):
        res = self.client().get('/actors/1',
                                headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/1', json=self.new_actor,
                                 headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_actor_casting_director(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        ac = Actor.query.first()
        res = self.client().patch('/actors/'+str(ac.id), json=self.new_actor,
                                  headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actors_if_not_exist(self):
        res = self.client().patch('/actors/89', json=self.new_actor,
                                  headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actors(self):
        ac = Actor.query.first()
        res = self.client().delete('/actors/'+str(ac.id),
                                   headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_if_not_exist(self):
        res = self.client().delete('/actors/2000',
                                   headers=executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
