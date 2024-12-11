import config
from server_impl import Server
from flask import Flask, request

# Create a Flask app
app = Flask(__name__)
server = Server()

@app.route('/login', methods = ['POST'])
def login():
    return server.login(request)

@app.route('/')
def home():
    return server.home()

if __name__ == '__main__':
    app.run(host=config.IP, port=config.PORT)
