# Import the 'Flask' class from the 'flask' library.
from flask import Flask
from flask import request
from flask import jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('mcu', user='postgres',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Movie(BaseModel):
    release_date = DateField()
    title = CharField()


class Superhero(BaseModel):
    # name = CharField()
    character = CharField()


db.connect()
db.drop_tables([Movie, Superhero])
db.create_tables([Movie, Superhero])

movie_1 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_2 = Movie(character='The Incredible Hulk',
                release_date='2008-6-13').save()
movie_3 = Movie(character='Iron Man 2', release_date='2010-5-7').save()
movie_4 = Movie(character='Thor', release_date='2011-5-6').save()
movie_5 = Movie(character='Captain America: The First Avenger',
                release_date='2011-7-22').save()
movie_6 = Movie(character="Marvel's The Avengers",
                release_date='2012-5-4').save()
movie_7 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_8 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_9 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_10 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_11 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_12 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_13 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_14 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_15 = Movie(character='Iron Man', release_date='2008-5-2').save()
movie_16 = Movie(character='Iron Man', release_date='2008-5-2').save()

scarlett_johanson = Superhero(character='Black Widow').save()
robert_downey_jr = Superhero(character='Iron Man').save()
chris_evans = Superhero(character='Captain America').save()
chadwick_boseman = Superhero(character='Black Panther').save()
tom_holland = Superhero(character='Spider-Man').save()
mark_ruffalo = Superhero(character='Hulk').save()
chris_hemsworth = Superhero(character='Thor').save()
jeremy_renner = Superhero(character='Hawkeye').save()

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
            return jsonify(model_to_dict(Superhero.get(Superhero.id == id)))
        else:
            characterList = []
            for character in Superhero.select():
                characterList.append(model_to_dict(character))
            return jsonify(characterList)

    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        new_person = dict_to_model(Superhero, request.get_json())
        new_person.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return 'DELETE request'


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
    return "Hello, world!"


# Run our application, by default on port 5000
app.run(port=9000, debug=True)
