from flask import Flask

app = Flask(__name__)


@app.route('/create/<name>')
def create(name):
    return write(name)


@app.route('/write/<name>')
def write(name):
    datanode = "ec2-13-59-175-234.us-east-2.compute.amazonaws.com"
    return datanode


@app.route('/read/<name>')
def read(name):
    datanode = "ec2-13-59-175-234.us-east-2.compute.amazonaws.com"
    return datanode


if __name__ == '__main__':
    app.run()
