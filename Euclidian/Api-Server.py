# Import Flask Libraries for Python API
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

#import pandas for results
import pandas as pd
import json as js

# Import Security Library
from Security.security import authenticate, identity

# Setup logging
import logging
logging.basicConfig(filename='api-server.log', level= logging.ERROR)

# import Euclid
from euclid import *


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'securepassword' # dont send this
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Similarpeople(Resource):
    #@jwt_required()
    def get(self, people):
        retorno = getSimilares(basepeople,people)
        return retorno, 200
    
class Similaritem(Resource):
    #@jwt_required()
    def get(self, item):
        retorno = getSimilares(baseitem,item)
        return retorno, 200

class Peoplerecommendation(Resource):
    #@jwt_required()
    def get(self, people):
        retorno = getRecomendacoesUsuario(basepeople,people)
        return retorno, 200

class Itemrecommendation(Resource):
    #@jwt_required()
    def get(self, item):
        retorno = getSimilares(baseitem,item)
        return retorno, 200


api.add_resource(Similarpeople, '/id/<string:people>/similarpeople')
api.add_resource(Similaritem, '/id/<string:item>/similaritem')
api.add_resource(Peoplerecommendation, '/id/<string:people>/peoplerecommendation')
api.add_resource(Itemrecommendation, '/id/<string:item>/itemrecommendation')


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # important to mention debug=True