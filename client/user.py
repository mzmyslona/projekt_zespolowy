class User:
    def __init__(self, username, password, email=""):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"

class UserIdentity:
    def __init__(self, user, session_id):
        """Initialize with user (User object) and session_id."""
        self.user = user  # User object
        self.session_id = session_id  # Session ID (string)
