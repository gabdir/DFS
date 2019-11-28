import datetime

from . import db

class Files(db.Model):
    file_path = db.Column(db.String(256),primary_key=True)
    name = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime,default=datetime.datetime.utcnow,unique=True)


