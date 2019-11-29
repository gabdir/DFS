import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), os.path.pardir, 'db.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
