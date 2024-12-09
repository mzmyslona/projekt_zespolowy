import config
from flask import Flask, jsonify

# Create a Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Secure connection established via Nginx reverse proxy"})

if __name__ == '__main__':
    app.run(host=config.IP, port=config.PORT)
