import datetime

from . import db

class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime,default=datetime.datetime.utcnow,unique=True)
    size = db.Column(db.Integer)
    dir_id = db.Column(db.Integer, db.ForeignKey('directory.id'))

    def __init__(self, name, timestamp, size):
        self.name = name
        self.timestamp = timestamp
        self.size = size

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp,
            'size': self.size
        }
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(128), unique=True)
    files = db.relationship('Files', lazy='dynamic')


