import json
from flask import request, jsonify
from . import app
from .app import db
from .app import app
from .app.models import Files
import requests

db.create_all()

@app.route('/files', methods=['GET'])
def fetch():
    files = Files.query.all()
    all_files = []
    for file in files:
        new_file = {
            "file_path": file.file_path,
            "name": file.name,
            "timestamp":file.timestamp
        }
        all_files.append(new_file)

    response = {
        "status": "success",
        "files": all_files
    }

    return jsonify(response), 200

@app.route('/files', methods=['POST'])
def get_file(filename):
    fail_response = {
        'status': 'fail',
        'message': 'File does not exist'
    }
    try:
        file_object = Files.query.filter_by(name=filename).first()
        if not file_object:
            return jsonify(fail_response), 404
        else:
            file_object = file_object.to_dict()
            file_path = file_object['file_path']
            r = requests.get(f"{file_path}/{filename}")
            return r.content, r.status_code
    except ValueError:
        return jsonify(fail_response), 404


@app.route('/files', methods=['POST'])
def create_file():
    if 'user_file' not in request.files:
        return "No file attached", 400
    file = request.files["user_file"]
    # fs = random.choice(file_servers)
    r = requests.post(f"{fs}/files", files={"user_file": (file.filename, file)})
    return json.dumps("Added"), 200

@app.route('/remove/<file_path>', methods=['DELETE'])
def remove(file_path):
    Files.query.filter_by(file_path=file_path).delete()
    db.session.commit()
    return json.dumps("Deleted"), 200

@app.route('/rename/<file_path>', methods=['PATCH'])
def rename(file_path):
    data = request.get_json()
    new_name = data['name']
    file_to_update = Files.query.filter_by(file_path=file_path).all()[0]
    file_to_update.name = new_name
    db.session.commit()
    return json.dums("Edited"), 200