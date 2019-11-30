import json
from flask import request, jsonify
from app import db
from app import app
from app.models import File, Directory
from app import models
import requests
from random import choice
from os import listdir, mkdir, system
from instances import get_instances
from shutil import rmtree
from client.client import SERVER_STORAGE

db.create_all()

datanodes = ["ec2-3-134-80-70.us-east-2.compute.amazonaws.com"]

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
    try:
        num_files_deleted = db.session.query(File).delete()
        num_dirs_deleted = db.session.query(Directory).delete()
        db.session.commit()
    except:
        db.session.rollback()
    response = {
        "status": 'success',
        "message": f'Number of rows deleted {num_files_deleted},number of dirs deleted {num_dirs_deleted}',
        "datanodes": datanodes
    }
    print(num_files_deleted, num_dirs_deleted)
    return json.dumps(response), 200


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
            "size": file.size
        }
    return json.dumps(response), 200

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
        "status": 'success',
        "message": 'Added',
        "datanodes": datanodes
    }
    return json.dumps(response), 200

@app.route('/write/<name>')
def write(name):
    create(name)


@app.route('/read/<name>')
def read(name):
    """
    :return: Response(json, 200) where json["datanode"] contains the active datanode
    """
    datanode = choice_datanode()
    response = {
        "status": 'success',
        "datanode": datanode
    }
    return json.dumps(response), 200

@app.route('/delete/<name>')
def delete(name):
    File.query.filter_by(name=name).delete()
    db.session.commit()
    response = {
        "datanodes": datanodes,
        "message": 'Deleted'
    }
    return json.dumps(response), 200


@app.route('/copy/<name>')
def copy(name):
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    create(name)



@app.route('/move/<name>')
def move(name):
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    file = File.query.filter_by(name=name).all()[0]
    if not file:
        return json.dumps(datanodes), 400
    dir_to_move = request.headers.get('dir_to_move')
    dir = Directory.query.filter_by(path=dir_to_move).all()[0]
    if not dir:
        return json.dumps(datanodes), 400
    dir_id = dir.id
    file.dir_id = dir_id

    return json.dumps(datanodes), 400

@app.route('/diropen')
def diropen():
    """
    Does nothing
    :return:
    """
    response = {
        "datanodes": datanodes
    }
    return json.dumps(response), 200


@app.route('/dirmake/<name>')
def dirmake(name):
    """
    Creates directory in DB
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    fail_response = {
        "status": 'fail',
        "message": 'Directory does not exist'
    }
    dir_path = request.headers.get('dir_path')
    dir = Directory.query.filter_by(path=dir_path).all()[0]
    if not dir:
        return json.dumps(fail_response), 400
    path = dir_path + '/' + name
    new_dir = Directory(path=path)
    db.session.add(new_dir)
    db.session.commit()
    response = {
        "datanodes": datanodes,
        "message": 'Directory was made'
    }

    return json.dumps(response), 200

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
    if not Directory.query.filter_by(path=""):
        root = Directory(path="")
        db.session.add(root)
        db.session.commit()
    app.run()