import datetime

from . import db


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=True)
    size = db.Column(db.Integer)
    dir_id = db.Column(db.Integer, db.ForeignKey('directory.id'))

    def __init__(self, name, size, dir_id=None):
        self.name = name
        self.size = size
        if dir_id is not None:
            self.dir_id = dir_id

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp,
            'size': self.size
        }

    def __repr__(self):
        return f"<File {self.id} `{self.name}` ({self.size})>"


class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(128), unique=True)
    files = db.relationship('File', lazy='dynamic')

    def __repr__(self):
        return f"<Dir {self.id} {self.path}>"
