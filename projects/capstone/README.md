# Udacity Capstone Project - Casting Agency

The Casting Agency is a company that is responsible for creating movies and managing and assigning actors to those movies. As an Executive Producer within the company I have decided to create a system to simplify and streamline my process.

## Getting Started

### Installing Dependencies

Navigate to your backend directory.

```sh
cd starter
```

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Activate your virtual environment if you havent by running the below.

```sh
virtualenv --no-site-packages env
source env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) iis an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Database Setup

Start by running

```sh
flask db upgrade
```

Note: All backend code follows [PEP8 style guidelines.](https://www.python.org/dev/peps/pep-0008/)

## API Documentation

- Base URL: Currently hosted at *heroku link*, when run locally it is hosted at the default `http://127.0.0.1:5000`
- Authentication: No authentication needed for this version

### Actor resource endpoints

#### GET `/api/actors`

- Fetches actors, by default you get an array of the first 10 actors i.e page 1.
- Request Arguments: page/none, to get a certain page you can make use of the page query parameter as shown below, e.g sending page=2, will give you the second set of ten actors, actors 11 - 20.
- Response: An object containing a list of *actors*, the number of *total_actors*, and *success* message.
  
Sample Request

```sh
curl -H 'Content-Type: application/json' http://127.0.0.1:5000/api/actors?page=2
```

Sample Response

```json
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
```

#### GET `/api/actors/<actor_id>`

- Gets any actor with id equals actor_id from the database.
- Request Arguments: actor_id. This refers to the id of the specific actor to be returned.
- Response: success and actor information or 404 if not found.

Sample Request

```sh
curl -X GET http://127.0.0.1:5000/api/actors/3
```

Sample Response

```json
{
  "actor": {
    "name": "Glory jane",
    "age": 16,
    "gender": "female",
    "id": 3,
  },
  "success": true
}
```

#### DELETE `/api/actors/<actor_id>`

- Deletes any actor with id equals actor_id from the database.
- Request Arguments: actor_id. This refers to the id of the specific actor to be deleted.
- Response: success and actor id or 404 if not found.

Sample Request

```sh
curl -X DELETE http://127.0.0.1:5000/api/actors/3
```

Sample Response

```sh
{
  "success": True
  "id": 3
}
```

#### POST `/api/actors`

- Creates a new actor using the given data.
- Response: object containing newly created actor.

Sample Request

```sh
curl -X POST -d '{
    "name": "John Doe",
    "age": 44,
    "gender": "male"
  }' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/actors
```

Sample Response

```sh
{
  "actor": {
    "name": "John Doe",
    "age": 44,
    "gender": "male",
    "id": 2
  },
  "success": true
}
```

### Movies resource endpoints

#### POST `/api/movies`

- Creates a new movie using the given data.
- Response: object containing newly created movie.

Sample Request

```sh
curl -X POST -d '{
  "title": "the beautiful ones are born",
  "release_date": "2020-10-08"
}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/movies
```

Sample Response

```sh
{
  "movie": {
    "title": "the beautiful ones are born",
    "release_date": "2020-10-08",
    "id": 2
  },
  "success": true
}
```

#### GET `/api/movies`

- Fetches movies, by default you get an array of the first 10 movies i.e page 1.
- Request Arguments: page/none, to get a certain page you can make use of the page query parameter as shown below, e.g sending page=2, will give you the second set of ten movies, movies 11 - 20.
- Response: An object containing a list of *movies*, the number of *total_movies*, and *success* message.
  
Sample Request

```sh
curl -H 'Content-Type: application/json' http://127.0.0.1:5000/api/movies?page=2
```

Sample Response

```json
{
  "movies": [
    {
      "title": "Muhammad Ali",
      "release_date": "2020-10-08",
      "id": 1,
    },
    {
      "title": "Miss mary",
      "release_date": "2020-10-08",
      "id": 2,
    },
    {
      "title": "Glory jane",
      "release_date": "2020-10-08",
      "id": 3,
    }...
  ],
  "success": true,
  "total_movies": 19
}
```

#### GET `/api/movies/<movie_id>`

- Gets any movie with id equals movie_id from the database.
- Request Arguments: movie_id. This refers to the id of the specific movie to be returned.
- Response: success and movie information or 404 if not found.

Sample Request

```sh
curl -X GET http://127.0.0.1:5000/api/movies/3
```

Sample Response

```json
{
  "movie": {
    "title": "Glory jane",
    "release_date": "2020-10-08",
    "id": 3,
  },
  "success": true
}
```

#### DELETE `/api/movies/<movie_id>`

- Deletes any movie with id equals movie_id from the database.
- Request Arguments: movie_id. This refers to the id of the specific movie to be deleted.
- Response: success and movie id or 404 if not found.

Sample Request

```sh
curl -X DELETE http://127.0.0.1:5000/api/movies/3
```

Sample Response

```sh
{
  "success": True
  "id": 3
}
```

#### Roles

Casting Assistant:

- Can view actors and movies

Casting Director:

- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
  
Executive Producer:

- All permissions a Casting Director has and…
- Add or delete a movie from the database

#### Error Handling

Errors are returned in the following format:

```sh
{
  "sucess": False,
  "error": 400,
  "message": "bad_request
}
```

We have 5 error types to be returned

- 400: bad_request
- 404: not_found
- 405: method_not_allowed
- 422: unprocessable_entity
- 500: internal_server_error

## Testing

With Postgres running, run

```sh
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

Then run the test file

```sh
python test_flaskr.py
```

## Authors

[Blessing E Ebowe](https://www.linkedin.com/in/blessingebowe/)
