from flask import Flask, jsonify, render_template
import sys
import os
# try:
#     from flask_cors import CORS, cross_origin  # The typical way to import flask-cors
# except ImportError:
#     # Path hack allows examples to be run without installation.
#     import os
#     parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     os.sys.path.insert(0, parentdir)
#     from flask_cors import CORS, cross_origin

# from flasgger import Swagger, swag_from
from pprint import pprint as pp

# template = {
#     "swagger": "2.0",
#     "info": {
#         "title": "API",
#         "description": "API for my data",
#         "version": "0.1.0",
#         "contact": {
#             "email": "lineesh.niduvappurathmeethal@barclays.com"
#         }  
#     }
# }

app = Flask(__name__, static_folder='static')
# app.config['SWAGGER'] = {
#     'title': 'My API',
#     'uiversion': 3,
#     'specs_route': '/swagger/',
# }
# swagger = Swagger(app, template=template)
# CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
    # return {'hello': 'world'}

@app.route('/hello')
def get(self):
    return {'hello': 'world'}

@app.route('/health')
def health():
    return jsonify({'status': 'UP'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)