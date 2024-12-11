from server_requests import RequestCreator  # Import the RequestCreator class
from user import User, UserIdentity

class ServerConnection:
    def __init__(self):
        """Constructor for ServerConnection."""
        self.url = "ToDelete"
        self.request_creator = None  # Initially empty, will be set after login

    def log_in(self, user):
        """Log in the user and set its identity"""
        self.request_creator = RequestCreator()
        response = self.request_creator.send_log_in_request(user)
        print(response)

    def get_session_id(self, user):
        """Simulates acquiring session ID for the user (this can be replaced with actual logic)."""
        # For example, generate a simple session ID (you can replace this with real logic)
        return f"session_for_{user.username}_1234"

    def create_channel(self, channel_name):
        """Create a channel using RequestCreator."""
        if not self.request_creator:
            print("You must log in first.")
            return
        response = self.request_creator.send_create_channel_request(self.url, channel_name)
        print(response.text)  # Handle the response (e.g., print or log it)

    def list_channels(self):
        """List available channels using RequestCreator."""
        if not self.request_creator:
            print("You must log in first.")
            return
        response = self.request_creator.send_list_channels_request(self.url)
        print(response.text)  # Handle the response (e.g., print or log it)

    def add_channel_member(self, channel_name, user_to_add):
        """Add a member to a channel."""
        if not self.request_creator:
            print("You must log in first.")
            return
        response = self.request_creator.send_add_channel_member_request(self.url, channel_name, user_to_add)
        print(response.text)  # Handle the response (e.g., print or log it)

    def remove_channel(self, channel_name):
        """Remove a channel."""
        if not self.request_creator:
            print("You must log in first.")
            return
        response = self.request_creator.send_remove_channel_request(self.url, channel_name)
        print(response.text)  # Handle the response (e.g., print or log it)
