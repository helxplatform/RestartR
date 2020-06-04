import argparse
import json
import logging
import os
import pymongo
import requests
import sys
import time
import traceback
import yaml
import uuid
from flasgger import Swagger
from flask import Flask, jsonify, g, Response, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    """ JSON Encodes Mongo ObjectId. """ 
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

"""
Defines the restarting research genomics data API.
"""
logger = logging.getLogger (__name__)

app = Flask(__name__)

""" Enable CORS. """
api = Api(app)
CORS(app)
debug=False

""" Describe the API. """
app.config['SWAGGER'] = {
    'title': 'RestartingResearch Genomics Data API',
    'description': 'An API for genomics observations.',
    'uiversion': 3
}
swagger = Swagger(app)

""" Connect to databases for various datatypes. Include authentication. """
mongo_uri = os.environ['MONGO_URL']
auth_src = "?authSource=admin&ssl=false&ssl_cert_reqs=CERT_NONE"
observation = PyMongo(app, uri=f"{mongo_uri}/observation{auth_src}", ssl=False)
#contact = PyMongo(app, uri=f"{mongo_uri}/contact{auth_src}")
#survey = PyMongo(app, uri=f"{mongo_uri}/survey{auth_src}")

class APIKey:
    """ Use environment provided API Key to secure services. """
    @staticmethod
    def initialize ():
        api_key = observation.db.observation.find_one ({ "api_key" : "true" })
        if api_key:
            api_key = api_key['value']
        else:
            api_key = os.environ ['API_KEY']
            observation.db.observation.insert_one ({
                "api_key" : "true",
                "value"   : api_key
            })
        return api_key
    @staticmethod
    def get_key ():
        return APIKey.initialize ()

for attempt in range(0, 7):
    logger.info (f"-- attempting to connect to db.")
    try:
        api_key = APIKey.initialize ()
        logger.info (f"-- initialized db.")
        break
    except Exception as e:
        traceback.print_exc ()
        logger.info (f"-- unable to connect to db. pausing.")
        time.sleep (3)

class RestartRResource(Resource):

    """ Record an observation """
    def __init__(self, api_key):
        self.api_key = api_key

    """ Base class handler for API requests. """
    def create_response (self, result=None, status='success', message='', exception=None):
        """ Create a response. Handle formatting and modifiation of status for exceptions. """
        if exception:
            traceback.print_exc ()
            status='error'
            exc_type, exc_value, exc_traceback = sys.exc_info()
            result = {
                'error' : repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            }
        return {
            'status'  : status,
            'result'  : result,
            'message' : message
        }
            
class ObservationResource(RestartRResource):
    """ System initiation. """
    def post(self):
        """
        Record an observation.
        
        ---
        tag: observation
        description: Add an observation.
        requestBody:
            description: Insert observation request.
            required: true
            content:
                application/json:
                    schema:
                        type: object

                        properties:
                          foo:
                            type: string
                          bar:
                            type: string
                          baz:
                            type: string
                    example:
                        metadata:
                            date : "yyyymmdd"
                            timestamp: "109379172344860101937"
                            origin : "lab-x"
                        opaque_id : "p45l2kjq5q34adfaoihakbalkjbialh3453"
        responses:
            '200':
                description: Success
                content:
                    text/plain:
                        schema:
                            type: string
                            example: "Nominal observation"
            '400':
                description: Malformed message
                content:
                    text/plain:
                        schema:
                            type: string

        parameters:
            - in: body
              name: observation
              schema:
                type: object
              example:
                metadata:
                  date : "yyyymmdd"
                  timestamp: "109379172344860101937"
                  origin : "lab-x"
                opaque_id : "p45l2kjq5q34adfaoihakbalkjbialh3453"
              required: true
              description: The observation to record.
        """
        logger.debug (f"observation:{json.dumps(request.json, indent=2)}")
        response = {}
        try:
            obj = dict(request.json)
            authenticated = request.headers['X-API-Key'] == self.api_key
            assert authenticated, f"API Key presented does not match key configured for this system."
            response = {
                "id" : JSONEncoder().encode(
                    observation.db.observation.insert_one (obj).inserted_id
                )
            }
        except Exception as e:
            response = self.create_response (
                exception=e,
                message=f"Insert failed: {json.dumps(request.json, indent=2)}.")
        return response

class ObservationQueryResource(RestartRResource):
    """ System initiation. """
    def post(self):
        """
        Query observations.
        
        ---
        tag: observation
        description: Query observations.
        requestBody:
            description: Query request.
            required: true
            content:
                application/json:
                    schema:
                        type: object
                    example:
                      nodes:
                        - id: n0
                          type: chemical_substance
                        - id: n1
                          type: gene
        responses:
            '200':
                description: Success
                content:
                    text/plain:
                        schema:
                            type: string
                            example: "Nominal query"
            '400':
                description: Malformed message
                content:
                    text/plain:
                        schema:
                            type: string

        """
        response = {}
        try:
            obj = dict(request.json)
            authenticated = request.headers['X-API-Key'] == self.api_key
            assert authenticated, f"API Key presented does not match key configured for this system."
            response = {
                "id" : JSONEncoder().encode(
                    [ x for x in observation.db.observation.find (obj) ]
                )
            }
        except Exception as e:
            response = self.create_response (
                exception=e,
                message=f"Query failed: {json.dumps(request.json, indent=2)}.")
        return response
    

""" Register endpoints. """
resource_kw_args={ 'api_key' : APIKey.get_key () }
api.add_resource(ObservationResource, '/observation', resource_class_kwargs=resource_kw_args)
api.add_resource(ObservationQueryResource, '/query', resource_class_kwargs=resource_kw_args)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Genomic Observation API')
   parser.add_argument('-p', '--port',  type=int, help='Port to run service on.', default=5552)
   parser.add_argument('-d', '--debug', help="Debug log level.", default=False, action='store_true')
   args = parser.parse_args ()

   debug = False
   """ Configure """
   if args.debug:
       debug = True
       logging.basicConfig(level=logging.DEBUG)
       logger.debug (f"-- log level debug")
   logger.info (f"starting RestartR on port={args.port} with debug={args.debug}")
   app.run(host='0.0.0.0', port=args.port, debug=debug, threaded=True)
