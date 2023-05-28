from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

from model import Readers, db

reader_api = Blueprint('reader_api', __name__, url_prefix='/api/reader')
api = Api(reader_api)

class ReaderAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            
            username = body.get('username')
            name = body.get('name')
            book = body.get('book')
            finishedate = body.get('finishedate')
            rating = body.get('rating')
            
            if not username or len(username) < 1:
                return {'message': 'Username is missing or invalid'}, 400
            
            if not name or len(name) < 1:
                return {'message': 'Name is missing or invalid'}, 400
            
            if not book or len(book) < 1:
                return {'message': 'Book name is missing or invalid'}, 400
            
            if not finishedate or len(finishedate) < 1:
                return {'message': 'Date book finished is missing'}, 400
            
            if rating is None or rating < 0 or rating > 5:
                return {'message': 'Book rating is missing or invalid'}, 400
            
            reader = Readers(username=username, name=name, book=book, finishedate=finishedate, rating=rating)
            db.session.add(reader)
            db.session.commit()
            
            return jsonify(reader.read()), 201

    class _Read(Resource):
        def get(self):
            readers = Readers.query.all()
            json_ready = [reader.read() for reader in readers]
            return jsonify(json_ready)

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')

def init_app(app):
    app.register_blueprint(reader_api)

