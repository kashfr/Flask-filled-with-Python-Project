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
    # release_date = DateField()
    # release_date = TextField()
    release_date = CharField()


class Superhero(BaseModel):
    # name = CharField()
    name = CharField()
    # image = TextField()
    # image = URLField()
    image = CharField()


db.connect()
db.drop_tables([Movie, Superhero])
db.create_tables([Movie, Superhero])

# Phase One
movie_1 = Movie(title='Iron Man', release_date='May 2, 2008').save()
movie_2 = Movie(title='The Incredible Hulk',
                release_date='June 13, 2008').save()
movie_3 = Movie(title='Iron Man 2', release_date='May 7, 2010').save()
movie_4 = Movie(title='Thor', release_date='May 6, 2011').save()
movie_5 = Movie(title='Captain America: The First Avenger',
                release_date='July 22, 2011').save()
movie_6 = Movie(title="Marvel's The Avengers",
                release_date='May 4, 2012').save()

# # Phase Two
movie_7 = Movie(title='Iron Man 3',
                release_date='May 3, 2013').save()
movie_8 = Movie(title='Thor: The Dark World',
                release_date='November 8, 2013').save()
movie_9 = Movie(title='Captain America: The Winter Soldier',
                release_date='April 4, 2014').save()
movie_10 = Movie(title='Guardians of the Galaxy',
                 release_date='August 1, 2014').save()
movie_11 = Movie(title='Avengers: Age of Ultron',
                 release_date='May 1, 2015').save()
movie_12 = Movie(title='Ant-Man',
                 release_date='July 17, 2015').save()

# Phase Three
movie_13 = Movie(title='Captain America: Civil War',
                 release_date='May 6, 2016').save()
movie_14 = Movie(title='Doctor Strange',
                 release_date='November 4, 2016').save()
movie_15 = Movie(title='Guardians of the Galaxy Vol. 2',
                 release_date='May 5, 2017').save()
movie_16 = Movie(title='Spider-Man: Homecoming',
                 release_date='July 7, 2017').save()
movie_17 = Movie(title='Thor: Ragnorak',
                 release_date='November 3, 2017').save()
movie_18 = Movie(title='Black Panther',
                 release_date='February 16, 2018').save()
movie_19 = Movie(title='Avengers: Infinity War',
                 release_date='April 27, 2018').save()
movie_20 = Movie(title='Ant-Man and the Wasp',
                 release_date='July 6, 2018').save()
movie_21 = Movie(title='Captain Marvel', release_date='March 8, 2019').save()
movie_22 = Movie(title='Avengers: Endgame',
                 release_date='April 26, 2019 ').save()
movie_23 = Movie(title='Spider-Man: Far From Home',
                 release_date='July 2, 2019 ').save()

# Phase 4
movie_24 = Movie(title='Black Widow', release_date='July 9, 2021').save()
movie_25 = Movie(title='Shang-Chi and the Legend of the Ten Rings',
                 release_date='September 3, 2021').save()
movie_26 = Movie(title='Eternals', release_date='November 5, 2021').save()
movie_27 = Movie(title='Spider-Man: No Way Home',
                 release_date='December 17, 2021').save()


# Actors
scarlett_johanson = Superhero(
    name='Black Widow', image='https://static.wikia.nocookie.net/marvelcinematicuniverse/images/9/9a/BlackWidow-EndgameProfile.jpg').save()
robert_downey_jr = Superhero(
    name='Iron Man', image='https://static.wikia.nocookie.net/marvelcinematicuniverse/images/3/35/IronMan-EndgameProfile.jpg').save()
chris_evans = Superhero(name='Captain America',
                        image='https://static.wikia.nocookie.net/marvelcinematicuniverse/images/d/d7/CapAmerica-EndgameProfile.jpg').save()
chadwick_boseman = Superhero(
    name='Black Panther', image='https://static.wikia.nocookie.net/marvelcinematicuniverse/images/9/99/Black_Panther_AIW_Profile.jpg').save()
# tom_holland = Superhero(name='Spider-Man').save()
# mark_ruffalo = Superhero(name='Hulk').save()
# chris_hemsworth = Superhero(name='Thor').save()
# jeremy_renner = Superhero(name='Hawkeye').save()


# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.
app = Flask(__name__)


# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.
@app.route('/character/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/character/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def character(id=None):
    if request.method == 'GET':
        # if id:
        # character = Superhero.get(Superhero.id == id)
        # character = model_to_dict(character)
        # character = jsonify(character)
        # return character
        if id:
            return jsonify(model_to_dict(Superhero.get(Superhero.id == id)))
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
        character.image = updated_character['image']
        # Superhero.get(Superhero.id == id).name = updated_character['name']
        # Superhero.get(Superhero.id == id).save()
        character.save()
        # character = model_to_dict(character)
        # character = jsonify(character)
        # return character
        return jsonify(model_to_dict(character))

    # if request.method == "POST":
    #     character = request.get_json()
    #     character = dict_to_model(Superhero, character)
    #     character.save()
    #     character = model_to_dict(character)
    #     character = jsonify(character)
    #     return character

    # if request.method == 'POST':
    #     new_character = dict_to_model(Superhero, request.get_json())
    #     new_character.save()
    #     return jsonify({"success": True})

    if request.method == 'POST':
        dict_to_model(Superhero, request.get_json()).save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Superhero.get(Superhero.id == id).delete_instance()
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
        updated_movie = request.get_json()
        movie = Movie.get(Movie.id == id)
        movie.title = updated_movie['title']
        movie.release_date = updated_movie['release_date']
        movie.save()
        # movie = model_to_dict(movie)
        # movie = jsonify(movie)
        # return movie
        return jsonify(model_to_dict(movie))
        # return jsonify(model_to_dict(Movie.get(Movie.id == id)))

    if request.method == 'POST':
        dict_to_model(Movie, request.get_json()).save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Movie.get(Movie.id == id).delete_instance()
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
