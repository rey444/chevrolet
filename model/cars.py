from sqlalchemy import Column, Integer, String
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from __init__ import db
import random
from random import randrange
from datetime import date
import os, base64
import json

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Car(db.Model):
    __tablename__ = 'cars'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255), nullable=False)
    mileage = db.Column(db.String(255), unique=False, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    powSource = db.Column(db.String(255), nullable=False)
    people = db.Column(db.Integer, primary_key=True)
    transmission = db.Column(db.String(225), nullable=False)
    

    def __init__(self, model, mileage, type, powSource, people, transmission):
        self._model = model
        self._mileage = mileage
        self._type = type
        self._powSource = powSource
        self._people = people
        self._transmission = transmission
        self.determine_value()

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Cars(" + str(self.id) + "," + self.model + "," + str(self.mileage) + "," + self.type + "," + self.powSource + "," + str(self.people) + "," + self.transmission + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

   # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
    # CRUD read converts self to dictionary
    # returns dictionary
        return {
            "model": self.model,
            "mileage": self.mileage,
            "type": self.type,
            "power source": self.powSource,
            "seating capacity": self.people,
            "transmission": self.transmission
        }

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

class Car(db.Model):
    __tablename__ = 'cars' #tablename is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _model = db.Column(db.String(255), nullable=False)
    _mileage = db.Column(db.String(255), unique=False, nullable=False)
    _type = db.Column(db.String(255), nullable=False)
    _powSource = db.Column(db.String(255), nullable=False)
    _people = db.Column(db.Integer, primary_key=True)
    _transmission = db.Column(db.String(225), nullable=False)
    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)
    

    def __init__(self, model, mileage, type, powSource, people, transmission):
        self._model = model
        self._mileage = mileage
        self._type = type
        self._powSource = powSource
        self._people = people
        self._transmission = transmission
        self.determine_value()

    # model getter
    @property
    def model(self):
        return self._model 

    # setter function to car's model
    @model.setter
    def model(self, model):
        self._model = model 

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, mileage):
        self._mileage = mileage
        
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type (self, type):
        self._type = type
    
    @property
    def powSource (self):
        return self._powSource
    
    @powSource.setter
    def powSource(self, powSource):
        self._powSource = powSource
    
    @property
    def people (self):
        return self._people
    
    @people.setter
    def people(self, people):
        self._people = people
           
    @property
    def transmission (self):
        return self._transmission
    
    @transmission.setter
    def transmission(self, transmission):
        self._transmission = transmission

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

# CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "model": self.model,
            "mileage": self.mileage,
            "type": self.type,
            "power source": self.powSource,
            "seating capacity": self.people,
            "transmission": self.transmission
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, model="", mileage="", type="", powSource="", people="", transmission=""):
        """only updates values with length"""
        if len(mileage) > 0:
            self.mileage = mileage
        self.model = model
        self.type = type
        self.powSource = powSource
        self.people = people
        self.transmission = transmission
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initCars():""
db.create_all()
# Tester Data for table

u1 = Car(model='Chevrolet Tahoe', type='SUV', powSource='Gas', people='7-8', transmission='Automatic')
u2 = Car(model='Chevrolet Equinox', type='SUV', powSource='Gas', people='5', transmission='Automatic')
u3 = Car(Model='Chevrolet Silverado', type='Pickup Truck', powSource = 'Gas', people='5', transmission='Automatic')

cars = [u1, u2, u3,]

# building sample user/notes data

for car in cars:
    try:
        car.create()
    except IntegrityError:
        db.session.remove()
        print((f"Records exist, duplicate email, or error: {car.model}"))