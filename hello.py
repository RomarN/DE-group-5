from flask import Flask

app = Flask(__name__)


@app.route('/<name>', methods=['PUT'])
def hello_world(name):
    return 'Hello, {}!'.format(name)


@app.route('/<name>', methods=['POST'])
def hello(name):
    return 'HELLO, {}!'.format(name)