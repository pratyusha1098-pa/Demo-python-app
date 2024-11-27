import functools
from pymongo import MongoClient
from flasgger import swag_from
import json
import os
import requests
from pprint import pprint as pp

from flask import ( Blueprint, flash, g, Flask, jsonify, render_template, request, send_from_directory, redirect, url_for )

certs = Blueprint('user', __name__, url_prefix='/api/user')

dbserver = MongoClient('mongodb://localhost:27017/')
certappDB = dbserver['certapp']

@user.route('/login', methods=['POST'])
def login():
    res = []
    code = 500
    status = False
    message = 'Internal Server Error'
    try:
        if request.method == 'POST':
            data = request.get_json()
            rest = list(certappDB.user.find({"username": data['username'], "password": data['password']}))
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
    except Exception as e:
        code = 500
        status = False
        message = 'Internal Server Error'
    return jsonify({'status': status, 'message': message, 'data': res}), code   

@user.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'UP'})