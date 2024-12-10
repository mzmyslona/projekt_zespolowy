from flask import jsonify
from tools import Tools
from database import Database

class Server:
    def __init__(self):
        self.active_sessions = dict()
        self.db = Database()

    def login(self, request):
        username = request.json['username']
        if username in self.active_sessions:
            result, message = True, "Warning! You have already active session."
        else:
            password = Tools.hash(request.json['password'])
            result, message = self.db.check_credentials(username, password)
            if result:
                self.active_sessions[username] = Tools.generate_sessionID(username, password)
        return jsonify({"success": result,
                        "message": message,
                        "session_id": self.active_sessions.get(username, "")})

    def signup(self, request):
        result, message = self.db.sign_up_user(request.json['username'], request.json['email'], Tools.hash(request.json['password']))
        return jsonify({"success": result,
                        "message": message})

    def home(self):
        return jsonify({"message": "Secure connection established."})
