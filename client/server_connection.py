from requests import RequestCreator  # Import the RequestCreator class
from user import User, UserIdentity

class ServerConnection:
    def __init__(self, url, port):
        """Constructor for ServerConnection."""
        self.url = url
        self.port = port
        self.request_creator = None  # Initially empty, will be set after login

    def log_in(self, user):
        """Log in the user and set the request_creator instance."""
        # Simulate getting the session_id from an external source (e.g., server response, random generation, etc.)
        session_id = self.get_session_id(user)

        # Create UserIdentity instance with the user and session_id
        user_identity = UserIdentity(user, session_id)

        # Now assign RequestCreator instance with user_identity
        self.request_creator = RequestCreator(user_identity)  # Instantiate RequestCreator with user_identity
        print(f"Logged in as {user_identity.user.username}")

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
