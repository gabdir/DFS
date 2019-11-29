from flask import Flask

app = Flask(__name__)
datanode = "ec2-3-134-80-70.us-east-2.compute.amazonaws.com"


@app.route('/create/<name>')
def create(name):
    return write(name)


@app.route('/write/<name>')
def write(name):
    return datanode


@app.route('/read/<name>')
def read(name):
    return datanode


@app.route('/delete/<name>')
def delete(name):
    return datanode


@app.route('/info/<name>')
def info(name):
    return datanode


@app.route('/copy/<name>')
def copy(name):
    return datanode


@app.route('/move/<name>')
def move(name):
    return datanode


@app.route('/diropen')
def diropen():
    return datanode


@app.route('/dirmake')
def dirmake():
    return datanode


@app.route('/dirdel')
def dirdel():
    return datanode


@app.route('/dirread')
def dirread():
    return datanode


@app.route('/init')
def init():
    return datanode


if __name__ == '__main__':
    app.run()
