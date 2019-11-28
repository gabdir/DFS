import datetime

from . import db

class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.String(256))
    name = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime,default=datetime.datetime.utcnow,unique=True)

    def __init__(self, file_path, name, timestamp):
        self.file_path = file_path
        self.name = name
        self.timestamp = timestamp

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'name': self.name,
            'file_path': self.file_path,
            'timestamp': self.timestamp
        }


