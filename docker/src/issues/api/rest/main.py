import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import base64
import hashlib

from flask import Flask, abort, make_response, jsonify, url_for, request, json, send_from_directory, send_file
from flask_jsontools import jsonapi
from dateutil import parser

from rest_utils import register_encoder

from issues.model import IssuesModel

app = Flask(__name__)
app.debug = True
register_encoder(app)

@app.route('/issues/api/v1.0/pedidos_ditesi', methods=['PUT','POST'])
@jsonapi
def crear_pedido_ditesi_privado():
    data = json.loads(request.data)
    logging.debug(data)
    persona = {
        'id': data['usuario_id'],
        'telefono': data['telefono'],
        'correo': data['correo']
    }
    problema = data['problema']
    i = IssuesModel.crear_pedido_ditesi_privado(persona, problema)
    return {'status':200, 'pedido': i}

# --------- publico --------------

@app.route('/issues/api/v1.0/publico/pedidos_ditesi', methods=['PUT','POST'])
@jsonapi
def crear_pedido_ditesi():
    data = json.loads(request.data)
    logging.debug(data)
    persona = {
        'dni': data['dni'],
        'nombre': data['nombre'],
        'apellido': data['apellido'],
        'telefono': data['telefono'],
        'correo': data['correo']
    }
    problema = data['problema']
    i = IssuesModel.crear_pedido_ditesi_publico(persona, problema)
    return {'status':200, 'pedido': i}


@app.route('/', methods=['OPTIONS'])
def cors():
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.after_request
def cors_after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



def main():
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()

    """
        api rest:

        issues/api/v1.0/issue/
        issues/api/v1.0/my_issue/
        issues/api/v1.0/office_issue/
        issues/api/v1.0/assigned_issue/
    """


    """
    		  this.getMyIssues = getMyIssues;
    		  this.getOfficesIssues = getOfficesIssues;
    		  this.getAssignedIssues = getAssignedIssues;
    		  this.findById = findById;
    			this.findByIds = findByIds;
    			this.findAll = findAll;
    		  this.create = create;
    		  this.createComment = createComment;
    		  this.changeStatus = changeStatus;
    			this.changePriority = changePriority;
    			this.getOffices = getOffices;
    			this.getAreas = getAreas;
    			this.getOfficeSubjects = getOfficeSubjects;
    			this.subscribe = subscribe;
    			this.searchUsers = searchUsers;
    			this.updateIssue = updateIssue;

    """
