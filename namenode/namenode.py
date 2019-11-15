from flask import Flask

app = Flask(__name__)
datanode = "ec2-13-59-175-234.us-east-2.compute.amazonaws.com"


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


if __name__ == '__main__':
    app.run()
