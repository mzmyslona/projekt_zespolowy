from flask import jsonify
from tools import Tools
from database import Database

class Server:
    def __init__(self):
        self.active_sessions = dict()
        self.db = Database()

    def login(self, request):
        result, message = self.db.check_credentials(request.json['username'], request.json['password'])
        return jsonify({"success": result,
                        "message": message})

    def signup(self, request):
        result, message = self.db.sign_up_user(request.json['username'], request.json['email'], request.json['password'])
        return jsonify({"success": result,
                        "message": message})

    def home(self):
        return jsonify({"message": "Secure connection established."})
