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

print(datanodes[0])
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


@app.route('/create/<name>')
def create(name):

    dir_path = request.headers.get('dir_path')
    size = request.headers.get('size')
    dir_id = Directory.query.filter_by(path=dir_path).first().id
    if File.query.filter_by(name=name, dir_id=dir_id).first():
        print(File.query.filter_by(name=name, dir_id=dir_id).first())
        return jsonify(datanodes), 400
    file = File(name=name, size=size, dir_id=dir_id)
    db.session.add(file)
    db.session.commit()

    response = {
        # "status": 'success',
        "message": 'Added',
        "datanodes": datanodes
    }
    # print(jsonify(datanodes))
    return json.dumps(response), 200
    # return jsonify(response),200


@app.route('/write/<name>')
def write(name):
    return datanodes[0]
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
def delete():
    # data = request.get_json()
    # id = data['id']
    # File.query.filter_by(id=id).delete()
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



if __name__ == '__main__':
    if not Directory.query.filter_by(path=""):
        root = Directory(path="")
        db.session.add(root)
        db.session.commit()
    app.run()