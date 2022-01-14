# Import the 'Flask' class from the 'flask' library.
from flask import Flask
from flask import request
from flask import jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('people', user='postgres',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    age = IntegerField()
    birthday = DateField()


db.connect()
db.drop_tables([Person])
db.create_tables([Person])


tyler = Person(name='Tyler', age=28, birthday='1990-1-13').save()
zakk = Person(name='Zakk', age=29, birthday='1990, 11, 18').save()
# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.

app = Flask(__name__)

# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.


@app.route('/person/', methods=['GET', 'POST'])
@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def person(id=None):
    if request.method == 'GET':
        if id:
            person = Person.get(Person.id == id)
            person = model_to_dict(person)
            return jsonify(model_to_dict(Person.get(Person.id == id)))
        else:
            peopleList = []
            for person in Person.select():
                peopleList.append(model_to_dict(person))
            return jsonify(peopleList)

    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        new_person = dict_to_model(Person, request.get_json())
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


# @app.route('/endpoint', methods=['GET', 'PUT', 'POST', 'DELETE'])
# def endpoint():
#     if request.method == 'GET':
#         return 'GET request'

#     if request.method == 'PUT':
#         return 'PUT request'

#     if request.method == 'POST':
#         return 'POST request'

#     if request.method == 'DELETE':
#         return 'DELETE request'


@app.route('/')
def index():
    return "Hello, world!"


# Run our application, by default on port 5000
app.run(port=9000, debug=True)
