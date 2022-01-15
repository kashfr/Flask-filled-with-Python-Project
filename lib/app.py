# Import the 'Flask' class from the 'flask' library.
from unicodedata import name
from flask import Flask
from flask import request
from flask import jsonify
from markupsafe import re
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('mcu', user='postgres',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Movie(BaseModel):
    title = CharField()
    release_date = DateField()


class Superhero(BaseModel):
    # name = CharField()
    name = CharField()


db.connect()
db.drop_tables([Movie, Superhero])
db.create_tables([Movie, Superhero])

movie_1 = Movie(title='Iron Man', release_date='2008-5-2').save()
movie_2 = Movie(title='The Incredible Hulk',
                release_date='2008-6-13').save()
movie_3 = Movie(title='Iron Man 2', release_date='2010-5-7').save()
movie_4 = Movie(title='Thor', release_date='2011-5-6').save()
movie_5 = Movie(title='Captain America: The First Avenger',
                release_date='2011-7-22').save()
movie_6 = Movie(title="Marvel's The Avengers",
                release_date='2012-5-4').save()

movie_7 = Movie(title='Iron Man 3',
                release_date='2013-5-3').save()
movie_8 = Movie(title='Thor: The Dark World',
                release_date='2013-11-8').save()
movie_9 = Movie(title='Captain America: The Winter Soldier',
                release_date='2014-4-4').save()
movie_10 = Movie(title='Guardians of the Galaxy',
                 release_date='2014-8-1').save()
movie_11 = Movie(title='Avengers: Age of Ultron',
                 release_date='5/1/2015').save()
movie_12 = Movie(title='Ant-Man',
                 release_date='7/17/15').save()

movie_13 = Movie(title='Captain America: Civil War',
                 release_date='2016-5-6').save()
movie_14 = Movie(title='Doctor Strange', release_date='2008-5-2').save()
movie_15 = Movie(title='Guardians of the Galaxy Vol. 2',
                 release_date='2008-5-2').save()
movie_16 = Movie(title='Spider-Man: Homecoming',
                 release_date='2008-5-2').save()
movie_17 = Movie(title='Thor: Ragnorak', release_date='2008-5-2').save()
movie_18 = Movie(title='Black Panther', release_date='2008-5-2').save()
movie_19 = Movie(title='Avengers: Infinity War',
                 release_date='2008-5-2').save()
movie_20 = Movie(title='Ant-Man and the Wasp',
                 release_date='2008-5-2').save()
movie_21 = Movie(title='Captain Marvel', release_date='2008-5-2').save()
movie_22 = Movie(title='Avengers: Endgame', release_date='2008-5-2').save()
movie_22 = Movie(title='Spider-Man: Far From Home',
                 release_date='2019-7-2').save()

scarlett_johanson = Superhero(name='Black Widow').save()
robert_downey_jr = Superhero(name='Iron Man').save()
chris_evans = Superhero(name='Captain America').save()
chadwick_boseman = Superhero(name='Black Panther').save()
tom_holland = Superhero(name='Spider-Man').save()
mark_ruffalo = Superhero(name='Hulk').save()
chris_hemsworth = Superhero(name='Thor').save()
jeremy_renner = Superhero(name='Hawkeye').save()


# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.
app = Flask(__name__)


# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.
@app.route('/character/', methods=['GET', 'POST'])
@app.route('/character/<id>', methods=['GET', 'PUT', 'DELETE'])
def character(id=None):
    if request.method == 'GET':
        if id:
            character = Superhero.get(Superhero.id == id)
            character = model_to_dict(character)
            character = jsonify(character)
            return character
        # if id:
            # return jsonify(model_to_dict(Superhero.get(Superhero.id == id)))
        else:
            characterList = []
            for character in Superhero.select():
                characterList.append(model_to_dict(character))
            return jsonify(characterList)
        # else:
        #     characterList = []
        #     for character in Superhero.select():
        #         characterList.append(model_to_dict(character))
        #     return jsonify(characterList)

    if request.method == 'PUT':
        updated_character = request.get_json()
        character = Superhero.get(Superhero.id == id)
        character.name = updated_character['name']
        character.save()
        return jsonify(model_to_dict(Superhero.get(Superhero.id == id)))

        return character

    if request.method == "POST":
        character = request.get_json()
        character = dict_to_model(Superhero, character)
        character.save()
        character = model_to_dict(character)
        character = jsonify(character)
        return character

    # if request.method == 'POST':
    #     new_character = dict_to_model(Superhero, request.get_json())
    #     new_character.save()
    #     return jsonify({"success": True})

    if request.method == 'DELETE':
        character = Superhero.get(Superhero.id == id)
        character.delete_instance()
        return jsonify({"deleted": True})


@app.route('/movie/', methods=['GET', 'PUT', 'POST', 'DELETE'])
@app.route('/movie/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def movie(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Movie.get(Movie.id == id)))
        else:
            movieList = []
            for movie in Movie.select():
                movieList.append(model_to_dict(movie))
            return jsonify(movieList)

    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        return 'POST request'

    if request.method == 'DELETE':
        movie = Movie.get(Movie.id == id)
        movie.delete_instance()
        # return jsonify(delete_instance(Movie.get(Movie.id == id)))
        return jsonify({"deleted": True})


@app.route('/get-json')
def getJson():
    return jsonify({
        "name": "Garfield",
        "hatesMondays": True,
        "friends": ["Sheldon", "Wade", "Orson", "Squeak"],
        "jobs": ["Bartender", "Tutor", "Uber Driver"]
    })


@app.route('/')
def index():
    return "Welcome to the Marvel Cinematic Universe!"


# Run our application, by default on port 5000
app.run(port=9000, debug=True)
