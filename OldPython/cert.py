import functools
from pymongo import MongoClient
from flasgger import swag_from
import json
import os
import requests
from pprint import pprint as pp

from flask import ( Blueprint, flash, g, Flask, jsonify, render_template, request, send_from_directory, redirect, url_for )

certs = Blueprint('certs', __name__, url_prefix='/api')

dbserver = MongoClient('mongodb://localhost:27017/')
certappDB = dbserver['certapp']

@certs.route('/certs', methods=['GET', 'POST', 'PATCH', 'DELETE']) 
def certs():
    res = []
    code = 500
    status = False
    message = 'Internal Server Error'
    try:
        if request.method == 'GET':
            rest = list(certappDB.certs.find())
            for r in rest:
                r['_id'] = str(r['_id'])
                res.append(r)
            if res:
                code = 200
                status = True
                message = 'Success'
            else:
                code = 404
                status = False
                message = 'Not Found'
        elif request.method == 'POST':
            data = request.get_json()
            res = certappDB.certs.insert_one(data)
            if res.acknowledged:
                code = 201
                status = True
                message = 'Created'
            else:
                code = 400
                status = False
                message = 'Bad Request'
        elif request.method == 'PATCH':
            data = request.get_json()
            certappDB.certs.update_one({'_id': data['_id']}, {'$set': data})
            res = certappDB.certs.find_one({"name": data['name']})
            res['_id'] = str(res['_id'])
            if res:
                code = 200
                status = True
                message = 'Updated'
            else:
                code = 404
                status = False
                message = 'Not Found'
        elif request.method == 'DELETE':
            data = request.get_json()
            certappDB.certs.delete_one({'_id': data['_id']})
            res = certappDB.certs.find_one({"name": data['name']})
            if not res:
                code = 200
                status = True
                message = 'Deleted'
            else:  
                code = 404
                status = False
                message = 'Not Deleted'
    except Exception as e:
        message = {"error": str(e)}
        status = "Error"
        code = 500

    return jsonify({'status': status, 'message': message, 'data': res}), code

@certs.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'UP'})


