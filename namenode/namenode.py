import json
from flask import request, jsonify
from app import db
from app import app
from app.models import File, Directory
from app import models
import requests

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
    #return jsonify(response), 404

@app.route('/info/<name>')
def info(name):
    
    response = {
        "datanodes": datanodes,

    }

@app.route('/create/<name>')
def create(name):
    return write(name)


@app.route('/write/<name>')
def write(name):
    pass


@app.route('/read/<name>')
def read(name):
    pass


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
    init()