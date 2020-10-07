from flask import Flask
from locust import HttpUser, task, between

server_port = 5000
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run('127.0.0.1',port=server_port)