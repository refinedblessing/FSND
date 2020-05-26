import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_short_drinks():
    drinks = Drink.query.all()
    short_drinks = [drink.short() for drink in drinks]
    return {"success": True, "drinks": short_drinks}


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_long_drinks(payload):
    drinks = Drink.query.all()
    long_drinks = [drink.long() for drink in drinks]
    return {"success": True, "drinks": long_drinks}


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    try:
        data = request.get_json()
        title = data.get('title', None)
        validate_or_abort(title)

        recipe = data.get('recipe', None)
        validate_or_abort(recipe)

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        return {"success": True, "drinks": [drink.long()]}
    except Exception:
        abort(422)


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).one()
        data = request.get_json()
        title = data.get('title', None)
        if title:
            drink.title = title
        recipe = data.get('recipe', None)
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.insert()
        return {"success": True, "drinks": [drink.long()]}
    except Exception:
        abort(404)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).one()
        drink.delete()

        if drink is None:
            abort(404)

        return {"success": True, "delete": id}
    except Exception:
        abort(404)


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

# Utility functions


def is_valid(data):
    '''
    Validates that data is not None
    Args: data
    Returns: True if presents and False if absent
    '''
    if data is None:
        return False
    return True


def validate_or_abort(data):
    '''
    Abort request if data is not valid
    Args: data
    '''
    if not is_valid(data):
        abort(422)
