from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from gevent.pywsgi import WSGIServer
from datetime import datetime
from services.charge import charge
import jsonschema
import simplejson as json

app = Flask(__name__)
api = Api(app)
timevalidate = ""
inc = 0
lis = []


class AddCard(Resource):
    def post (self):
        card_number = request.json['card_number']
        card_limit = request.json['card_limit']
        card_status = request.json['card_status']
        last_transaction = request.json['last_transaction']

        try:
            query = conn.execute("insert into charge values(null,'{0}','{1}','{2}','{3}')".format(card_number,card_limit,card_status,last_transaction))
            return {'status':'success'}
        except:
            return {'status':'credit card already registered'}     

class Transaction(Resource):
    def post (self):
        db_connect = create_engine('sqlite:///charge.db')
        conn = db_connect.connect()
        card_number = request.json['card_number']
        transaction = request.json['transaction']
        merchant = request.json['merchant']
        timenow = datetime.now().strftime("%s")
        
        global timevalidate
        global inc
        global list        

        if not timevalidate:
            timevalidate = timenow
            inc += 1
            return charge(card_number,transaction,merchant)
        else:
            res = int(timenow) - int(timevalidate)
            if res > 120:
                timevalidate = timenow  
                inc = 1
                return charge(card_number,transaction,merchant)
            else:            
                inc += 1
                if inc > 3:
                    return {"approved": "false", "deniedReasons": "Transactions number exceeded"}    
                else:
                    return charge(card_number,transaction,merchant)     
                

api.add_resource(AddCard, '/addcard')
api.add_resource(Transaction, '/transaction')

if __name__ == '__main__':
     http_server = WSGIServer(('', 7000), app)
     http_server.serve_forever()