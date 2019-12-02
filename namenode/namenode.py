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
from client.client import SERVER_STORAGE

db.create_all()

datanodes = ["ec2-52-15-157-220.us-east-2.compute.amazonaws.com"]


def check_main_dir():
    if Directory.query.filter_by(path="").first() is None:
        root = Directory(path="")
        db.session.add(root)
        db.session.commit()


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
        "message": f'Number of rows deleted {num_files_deleted},number of dirs deleted {num_dirs_deleted}',
        "datanodes": datanodes
    }
    print(num_files_deleted, num_dirs_deleted)
    check_main_dir()
    return json.dumps(response), 200


@app.route('/info/<name>')
def info(name):
    """
        :return: Response(json, 200) where json contains information about file
    """

    file = File.query.filter_by(name=name).first()
    print(file)
    if not file:
        response = {
            "datanodes": datanodes,
            "message": 'File not exist'
        }
        return json.dumps(response), 400
    else:
        response = {
            "datanodes": datanodes,
            "timestamp": str(file.timestamp),
            "size": file.size,
            "message": f"File `{name}`. Created: `{str(file.timestamp)}`. Size: `{file.size}`"
        }
        print(response)
        return json.dumps(response), 200


@app.route('/write/<name>')
def write(name):
    dir_path = request.headers.get('dir_path')
    size = request.headers.get('size')
    dir_id = Directory.query.filter_by(path=dir_path).first().id
    response = {
        "datanodes": datanodes
    }
    if File.query.filter_by(name=name, dir_id=dir_id).first():
        # print(File.query.filter_by(name=name, dir_id=dir_id).first())
        return json.dumps(response), 400
    file = File(name=name, size=size, dir_id=dir_id)
    db.session.add(file)
    db.session.commit()

    return json.dumps(response), 200


@app.route('/read/<name>')
def read(name):
    """
    :return: Response(json, 200) where json["datanode"] contains the active datanode
    """

    dir_path = request.headers.get('dir_path')
    dir_id = Directory.query.filter_by(path=dir_path).first().id
    datanode = random.choice(datanodes)
    response = {
        "datanode": datanode
    }

    if not File.query.filter_by(name=name, dir_id=dir_id).first():
        return json.dumps(response), 400

    return json.dumps(response), 200


@app.route('/delete/<name>')
def delete(name):
    query = File.query.filter_by(name=name)
    if query.first():
        query.delete()
        db.session.commit()
        response = {
            "datanodes": datanodes,
            "message": 'Deleted'
        }
        return json.dumps(response), 200
    else:
        response = {
            "datanodes": datanodes,
            "message": f'file {name} does not exist'
        }
        return json.dumps(response), 400


@app.route('/copy/<name>')
def copy(name):
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    write(name)


@app.route('/move/<name>')
def move(name):
    """
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    file = File.query.filter_by(name=name).all()[0]
    fail_response = {
        "datanodes": datanodes,
        "message": 'File not exist'
    }
    if not file:
        return json.dumps(fail_response), 400
    dir_to_move = request.headers.get('dir_to_move')
    dir = Directory.query.filter_by(path=dir_to_move).all()[0]
    fail_response_dir = {
        "datanodes": datanodes,
        "message": 'Directory is not exist'
    }
    if not dir:
        return json.dumps(fail_response_dir), 400
    dir_id = dir.id
    file.dir_id = dir_id

    response = {
        "datanodes": datanodes,
        "message": "Moved to directory"
    }

    return json.dumps(response), 200


@app.route('/diropen')
def diropen():
    """
    Does nothing
    :return:
    """
    datanode = random.choice(datanodes)
    response = {
        "datanode": datanode,
    }
    dir_path = request.headers.get('dir_path')
    if not Directory.query.filter_by(path=dir_path).first():
        return json.dumps(response), 400

    return json.dumps(response), 200


@app.route('/dirmake/<name>')
def dirmake(name):
    """
    Creates directory in DB
    :return: Response(json, 200) where json["datanodes"] contains the list of active datanodes
    """
    fail_response = {
        "datanodes": datanodes,
        "message": 'Directory does not exist'
    }
    dir_path = request.headers.get('dir_path')
    dir = Directory.query.filter_by(path=dir_path).all()[0]
    if not dir:
        return json.dumps(fail_response), 400
    if dir_path == "":
        path = name
    else:
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
    dir_path = request.headers.get('dir_path')
    dir = Directory.query.filter_by(path=dir_path).all()[0]
    fail_response = {
        "datanodes": datanodes,
        "message": 'Directory is not exist'
    }
    if not dir:
        return json.dumps(fail_response), 400
    else:
        Directory.query.filter_by(path=dir_path).delete()
        response = {
            "datanodes": datanodes,
            "message": 'Directory was deleted'
        }
    return json.dumps(response), 200


@app.route('/dirread')
def dirread():
    dir_path = request.headers.get('dir_path')
    datanode = random.choice(datanodes)
    response = {
        "datanode": datanode,
    }
    if not Directory.query.filter_by(path=dir_path).all()[0]:
        return json.dumps(response), 400

    return json.dumps(response), 200


if __name__ == '__main__':
    print(bool(Directory.query.filter_by(path="").first()))
    check_main_dir()
    app.run("127.0.0.2")
