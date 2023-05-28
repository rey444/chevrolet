from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import db

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

reader_api = Blueprint('reader_api', __name__, url_prefix='/api/reader')
api = Api(reader_api)

class Readers(db.Model):
    __tablename__ = 'readers'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    book = db.Column(db.String(255), nullable=False)
    finishedate = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, username, name, book, finishedate, rating):
        self.username = username
        self.name = name
        self.book = book
        self.finishedate = finishedate
        self.rating = rating


    # a name getter method, extracts username from object
    @property
    def username(self):
        return self._username
   
    # a setter function, allows username to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
   
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
   
    # a getter method, extracts book from object
    @property
    def book(self):
        return self._book
   
    # a setter function, allows book to be updated after initial object creation
    @book.setter
    def book(self, book):
        self._book = book
   
    # a getter method, extracts year from object
    @property
    def finishedate(self):
        return self._finishedate
   
    # a setter function, allows year to be updated after initial object creation
    @finishedate.setter
    def finishedate(self, finishedate):
        self._finishedate = finishedate
   
    # a getter method, extracts rating from object
    @property
    def rating(self):
        return self._rating
   
    # a setter function, allows book to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating        
            
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
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "book": self.book,
            "finishedate": self.finishedate,
            "rating": self.rating
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, username, name, book, finishedate, rating):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(name) > 0:
            self.name = name
        if len(book) > 0:
            self.book = book
        if len(finishedate) > 0:
            self.finishedate = finishedate
        if 0 < rating < 5:
            self.rating = rating
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

"""Database Creation and Testing """


# Builds working data for testing
def initReaders():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Readers(username="rey444", name="Shreya", book ="The Hunger Games", year=2019, rating=5)
        r2 = Readers(username="jiyu", name="Jiya", book ="Divergent", year=2021, rating=3)
        r3 = Readers(username="vai", name="Vaishavi", book ="Animal Farm", year=2020, rating=4)


        readers = [r1, r2, r3]

    """Builds sample car/note(s) data""" # NEEDS TO CONNECT TO CARSPEC.PY FILE THAT BUILDS THE API
    for reader in readers:
        try:
            reader.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate book, or error: {reader.model}")

