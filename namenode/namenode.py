import json
from flask import request, jsonify
from app import db
from app import app
from app.models import File, Directory
from app import models
from instances import get_instances
from os import system, mkdir, listdir
from random import choice
from client.client import SERVER_STORAGE
import requests
import random
from shutil import rmtree

db.create_all()

datanodes = ["ec2-52-14-232-104.us-east-2.compute.amazonaws.com"]


def choice_datanode():
    return choice(datanodes)


def check_datanode_failure():
    global datanodes
    old_datanodes = set(datanodes)
    new_datanodes = set(get_instances())  # currently available datanodes

    if old_datanodes == new_datanodes:  # nothing was changed
        return
    difference = new_datanodes - old_datanodes
    src = choice_datanode()
    if "storage" in listdir():
        rmtree("storage")
    mkdir("storage")
    system(f'scp -i "my_key.pem" -r ubuntu@{src}:{SERVER_STORAGE} storage')
    for trg in difference:
        system(f'scp -i "my_key.pem" -r storage/storage ubuntu@{trg}:/home/ubuntu')
    datanodes = new_datanodes


@app.route('/init')
def init():
    """
    Clears DB
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
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
    """
        :return: Response(json, 200) where json contains information about file
    """
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

@app.route('/create/<name>')
def create(name):
    return write(name)

@app.route('/write')
def write():
    create()


@app.route('/read/<name>')
def read(name):
    """
    :return: Response(json, 200) where json["datanode"] contains the active datanode
    """
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
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    pass


@app.route('/move/<name>')
def move(name):
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    pass


@app.route('/diropen')
def diropen():
    """
    Does nothing
    :return:
    """
    pass


@app.route('/dirmake')
def dirmake():
    """
    Creates directory in DB
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    pass


@app.route('/dirdel')
def dirdel():
    """
    Deletes directory in DB
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    pass


@app.route('/dirread')
def dirread():
    pass


if __name__ == '__main__':
    pass
