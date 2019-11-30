import json
from flask import request, jsonify
from app import db
from app import app
from app.models import File, Directory
from app import models
import requests
import random

db.create_all()

datanodes = ["ec2-3-134-80-70.us-east-2.compute.amazonaws.com"]


@app.route('/init')
def init():
    try:
        num_files_deleted = db.session.query(File).delete()
        num_dirs_deleted = db.session.query(Directory).delete()
        db.session.commit()
    except:
        db.session.rollback()
    response = {
        "status": 'success',
        "message": f'Number of rows deleted {num_files_deleted}',
        "datanodes": datanodes
    }
    print(num_files_deleted, num_dirs_deleted)
    #return jsonify(response), 200

@app.route('/info/<name>')
def info(name):
    fail_response = {
        "status": 'fail',
        "message": 'File not exist'
    }
    file = File.query.filter_by(name=name).all()[0]
    if not file:
        return jsonify(fail_response), 404
    else:
        response = {
            "datanodes": datanodes,
            "timestamp": file.timestamp,
            "size": file.size,
        }
    #return jsonify(response), 200

@app.route('/create')
def create():
    data = request.get_json()
    name = data['name']
    size = data['size']
    dir_id = data['dir_id']

    file = File(name=name, size=size, dir_id=dir_id)
    db.session.add(file)
    db.session.commit()
    response = {
        "status": 'success',
        "message": 'Added',
        "datanodes": datanodes
    }
    return jsonify(response),200


@app.route('/write')
def write():
    create()


@app.route('/read/<name>')
def read(name):
    datanode = random.choice(datanodes)
    response = {
        "status": 'success',
        "datanode": datanode
    }
    #return jsonify(response), 200

@app.route('/delete/<name>')
def delete(name):
    pass


@app.route('/copy/<name>')
def copy(name):
    pass


@app.route('/move/<name>')
def move(name):
    pass


@app.route('/diropen')
def diropen():
    pass


@app.route('/dirmake')
def dirmake():
    pass


@app.route('/dirdel')
def dirdel():
    pass


@app.route('/dirread')
def dirread():
    pass


if __name__ == '__main__':
    pass