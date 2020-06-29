import os
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth, gen_token

ITEMS_PER_PAGE = 20


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    CORS enabled to Allow all origins and for routes starting with /api.
    Allows browsers to send the Content-Type and Authorization header.
    Allows all methods.
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route("/api/token", methods=['POST'])
    def get_token():
        data = request.get_json()
        username = data.get('username', 'defaultuser@gmail.com')
        password = data.get('password', 'mypwd')
        scope = data.get('scope', None)

        return gen_token({
          'username': username, 'password': password, 'scope': scope})

    def paginate_items(request, items):
        '''
        Helper function to paginate items, limited by ITEMS_PER_PAGE
        Args: request, array of objects
        Returns: ITEMS_PER_PAGE number of items formatted
        [
            {
              "name": "Muhammad Ali",
              "id": 1,
            },
            {
              "name": "Miss mary",
              "id": 2,
            }
        ]
        '''
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        formatted_items = [
            item.format() for item in items]
        return formatted_items[start:end]

    def is_valid(data):
        '''
        Validates that data is not None
        Args: data
        Returns: True if presents and False if absent
        '''
        if data is '' or data is None:
            return False
        return True

    def validate_or_abort(data):
        '''
        Abort request if data is not valid
        Args: data
        '''
        if not is_valid(data):
            abort(422)

    def validate_date(date):
        '''
        Abort request if date is not valid format
        Args: date string
        '''
        format = '%Y-%m-%d'

        try:
            datetime.strptime(date, format).strftime(format)
        except ValueError as e:
            abort(422)
        return True

    @app.route("/api/actors", methods=['GET'])
    @requires_auth()
    def get_actors():
        '''
        GET /api/actors
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Args: None
        Response: An object containing a list of *actors*,
        the number of *total_actors*, and *success* message.
        {
            "actors": [
                {
                  "name": "Muhammad Ali",
                  "age": 16,
                  "gender": "male",
                  "id": 1,
                },
                {
                  "name": "Miss mary",
                  "age": 21,
                  "gender": "female",
                  "id": 2,
                },
                {
                  "name": "Glory jane",
                  "age": 16,
                  "gender": "female",
                  "id": 3,
                }...
            ],
            "success": true,
            "total_actors": 19
        }
        '''
        actors = Actor.query.order_by(Actor.id).all()
        paginated_actors = paginate_items(request, actors)

        if len(paginated_actors) == 0 and len(actors) != 0:
            abort(404)

        return jsonify({
            'actors': paginated_actors,
            'success': True,
            'total_actors': len(actors)
        })

    @app.route("/api/actors/<int:actor_id>", methods=['GET'])
    @requires_auth()
    def get_actor(actor_id):
        '''
        GET /api/actors/<actor_id>
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Args: actor_id, Id of actor to be returned.
        Response: {
          "actor": {
            "name": "Glory jane",
            "age": 16,
            "gender": "female",
            "id": 3,
          },
          "success": true
        } or passed to the
        404 error handler if not found
        '''

        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route("/api/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        '''
        DELETE /api/actors/<actor_id>
        Args: actor_id, Id of actor to be deleted.
        Response: {"success": True, "id": actor_id} or passed to the
        404 error handler
        '''

        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            'success': True,
            'id': actor_id
        })

    @app.route("/api/actors", methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(payload):
        '''
        POST /api/actors -d '{
          "name": "John Doe",
          "age": 44,
          "gender": "male"
        }' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/actors
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Creates new actor
        Response: object containing newly created actor
        {
            "actor": {
            "name": "John Doe",
            "age": 44,
            "gender": "male",
            "id": 2
          },
          "success": true
        }

        Error: 422 for any validation errors
        '''
        try:
            data = request.get_json()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)

            # validate data before creating
            validate_or_abort(name)
            validate_or_abort(age)
            validate_or_abort(gender)

            newActor = Actor(
                name=name,
                gender=gender,
                age=age
            )

            newActor.insert()

            return jsonify({
                'success': True,
                'actor': newActor.format()
            })
        except Exception:
            abort(422)

    @app.route('/api/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('post:actors')
    def update_actors(payload, actor_id):
        '''
        POST /api/actors/2 -d '{
          "name": "John Doe",
          "gender": "female"
        }' -H 'Content-Type: application/json'
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        http://127.0.0.1:5000/api/actors/2
        Updates previous actor
        Response: object containing updated actor
        {
            "actor": {
            "name": "John Doe",
            "age": 45,
            "gender": "female",
            "id": 2
          },
          "success": true
        }
        '''
        try:
            actor = Actor.query.filter_by(id=actor_id).one()
            data = request.get_json()
            name = data.get('name', None)
            if name:
                actor.name = name
            age = data.get('age', None)
            if age:
                actor.age = age
            gender = data.get('gender', None)
            if gender:
                actor.gender = gender
            actor.insert()
            return jsonify({'success': True, 'actor': actor.format()})
        except Exception:
            abort(404)

    # Movie Endpoints
    @app.route("/api/movies", methods=['GET'])
    @requires_auth()
    def get_movies():
        '''
        GET /api/movies
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Args: None
        Response: An object containing a list of *movies*,
        the number of *total_movies*, and *success* message.
        {
            "movies": [
                {
                  "title": "the beautiful ones are born",
                  "release_date": "2020-10-08"
                  "id": 1,
                },
                {
                  "title": "the beautiful ones are born",
                  "release_date": "2020-10-08"
                  "id": 2,
                }...
            ],
            "success": true,
            "total_movies": 19
        }
        '''
        movies = Movie.query.order_by(Movie.id).all()
        paginated_movies = paginate_items(request, movies)

        if len(paginated_movies) == 0 and len(movies) != 0:
            abort(404)

        return jsonify({
            'movies': paginated_movies,
            'success': True,
            'total_movies': len(movies)
        })

    @app.route("/api/movies/<int:movie_id>", methods=['GET'])
    @requires_auth()
    def get_movie(movie_id):
        '''
        GET /api/movies/<movie_id>
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Args: movie_id, Id of movie to be returned.
        Response: {
          "movie": {
            "title": "the beautiful ones are born",
            "release_date": "2020-10-08"
            "id": 3,
          },
          "success": true
        } or passed to the
        404 error handler if not found
        '''

        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route("/api/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        '''
        DELETE /api/movies/<movie_id>
        Args: movie_id, Id of movie to be deleted.
        Response: {"success": True, "id": movie_id} or passed to the
        404 error handler
        '''

        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            'success': True,
            'id': movie_id
        })

    @app.route("/api/movies", methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(payload):
        '''
        POST /api/movies -d '{
          "title": "the beautiful ones are born",
          "release_date": "2020-10-08"
        }' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/movies
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        Creates new movie
        Response: object containing newly created movie
        {
            "movie": {
            "title": "the beautiful ones are born",
            "release_date": "2020-10-08"
            "id": 2
          },
          "success": true
        }

        Error: 422 for any validation errors
        '''
        try:
            data = request.get_json()
            title = data.get('title', None)
            release_date = data.get('release_date', None)

            # validate data before creating
            validate_or_abort(title)
            validate_or_abort(release_date)
            validate_date(release_date)

            newMovie = Movie(
                title=title,
                release_date=release_date
            )

            newMovie.insert()

            return jsonify({
                'success': True,
                'movie': newMovie.format()
            })
        except Exception:
            abort(422)

    @app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('post:movies')
    def update_movies(payload, movie_id):
        '''
        POST /api/movies/2 -d '{
          "release_date": "2020-10-08"
        }' -H 'Content-Type: application/json'
        - H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
        http://127.0.0.1:5000/api/movies/2
        Updates previous movie
        Response: object containing updated movie
        {
          "movie": {
            "release_date": "2020-10-08",
            "title": "the beautiful ones are born",
            "id": 2

          },
          "success": true
        }
        '''
        try:
            movie = Movie.query.filter_by(id=movie_id).one()
            data = request.get_json()
            title = data.get('title', None)
            if title:
                movie.title = title
            release_date = data.get('release_date', None)
            if release_date:
                movie.release_date = release_date
            movie.insert()
            return jsonify({'success': True, 'movie': movie.format()})
        except Exception:
            abort(404)

    # Error Handling
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        '''
        AuthError error handler
        '''
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error
        }), ex.status_code

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad_request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not_found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method_not_allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal_server_error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
