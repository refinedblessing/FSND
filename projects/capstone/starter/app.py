import os
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

    @app.route("/api/actors", methods=['GET'])
    def get_actors():
        '''
        GET /api/actors
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

        if len(paginated_actors) == 0:
            abort(404)

        return jsonify({
            'actors': paginated_actors,
            'success': True,
            'total_actors': len(actors)
        })

    # Error Handling
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

    '''
    AuthError error handler
    '''

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error
        }), ex.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
