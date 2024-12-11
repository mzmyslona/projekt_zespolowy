from flask import jsonify
from tools import Tools

class Server:
    def __init__(self):
        self.active_sessions = dict()
        self.datab

    def login(self, request):
        login_data = request.json

        return jsonify({"message": "Login invoked"})

    def home(self):
        return jsonify({"message": "Secure connection established."})
