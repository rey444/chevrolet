from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
import json


car_api = Blueprint('car_api', __name__,
                   url_prefix='/api/cars')

api = Api(car_api)

class CarAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate model
            model = body.get('model')
            if model is None or len(model) < 2:
                return {'message': f'Model is missing, or is less than 2 characters'}, 210
            
            # validate mileage
            mileage = body.get('mileage')
            if mileage is None or len(mileage) < 2:
                return {'message': f'Mileage is missing, or is less than 2 characters'}, 210
           
            type = body.get('type')
            if type is None or len(type) < 2:
                return {'message': f'Type is missing, or is less than 2 characters'}, 210
            
            powSource = body.get('powSource')
            if powSource is None or len(powSource) < 2:
                return {'message': f'Power Source is missing, or is less than 2 characters'}, 210
            
            people = body.get('people')
            if people is None or len(people) < 2:
                return {'message': f'Seating capacity is missing, or is less than 2 characters'}, 210
            
            transmission = body.get('transmission')
            if transmission is None or len(transmission) < 2:
                return {'message': f'Transmission is missing, or is less than 2 characters'}, 210
            

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Car(model=model, 
                    mileage = mileage,
                    type=type,
                    powSource=powSource,
                    people=people,
                    transmission=transmission)
            
            ''' #2: Key Code block to add the car the user matched with to database '''
            # create user in database
            car = uo.create()
            # success returns json of car
            if car:
                return jsonify(car.read())
            # failure returns error
            return {'message': f'Processed {model}, either a format error or model name {model} is duplicate'}, 210

    class _create(Resource):
        def get(self):
            cars = Car.query.all()    # read/extract all cars from database
            json_ready = [car.read() for car in cars]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')   