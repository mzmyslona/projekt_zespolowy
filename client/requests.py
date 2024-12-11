import requests
from user import User  # Assuming User class is in user.py

class RequestCreator:
    """Class that contains methods for sending requests and applying decorators."""

    def __init__(self, user_identity):
        """Initialize with user_identity."""
        if not user_identity:
            raise ValueError("User identity must be provided for request creator.")
        self.user_identity = user_identity

    def authorization(self, func):
        """Authorization decorator that adds 'authorization' field to the dictionary."""
        def wrapper(*args, **kwargs):
            args_dict = func(*args, **kwargs)  # Get the dictionary from the original function
            if not self.user_identity:
                print("Authorization failed: No valid user identity.")
                return None
            # Extend the dictionary with user identity for authorization
            args_dict['authorization'] = {
                'username': self.user_identity.user.username,
                'session_id': self.user_identity.session_id
            }
            print(f"Authorization successful: {self.user_identity.user.username} ({self.user_identity.session_id}) is authorized.")
            return args_dict  # Return the modified dictionary
        return wrapper

    def send(self, http_method):
        """Send decorator that sends the dictionary arguments to the specified HTTP request method."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Get the dictionary of arguments with authorization field
                args_dict = func(*args, **kwargs)
                if not args_dict:
                    return None
                print(f"Sending request with {http_method} method")
                # Sending data to server using the specified HTTP method
                url = args_dict.get("url")
                if http_method == 'GET':
                    response = requests.get(url, params=args_dict)
                elif http_method == 'POST':
                    response = requests.post(url, json=args_dict)
                elif http_method == 'DELETE':
                    response = requests.delete(url, json=args_dict)
                else:
                    print("Unsupported HTTP method")
                    return None
                # Check for response
                if response.status_code == 200:
                    print("Request successful.")
                else:
                    print(f"Request failed with status code {response.status_code}")
                return response  # Return the response from the request
            return wrapper
        return decorator

    @authorization
    @send('POST')  # Example of sending with POST method
    def send_create_channel_request(self, url, channel_name):
        """Creates a new channel using parameters passed."""
        args_dict = {
            'url': url,
            'channel_name': channel_name
        }
        print(f"Creating channel {channel_name}...")
        return args_dict

    @authorization
    @send('GET')  # Example of sending with GET method
    def send_list_channels_request(self, url):
        """Lists all available channels."""
        args_dict = {
            'url': url
        }
        print("Listing channels...")
        return args_dict

    @authorization
    @send('POST')  # Example of sending with POST method
    def send_add_channel_member_request(self, url, channel_name, user_to_add):
        """Adds a member to a channel."""
        args_dict = {
            'url': url,
            'channel_name': channel_name,
            'user_to_add': user_to_add.username  # Store only the username
        }
        print(f"Adding {user_to_add.username} to channel {channel_name}...")
        return args_dict

    @authorization
    @send('DELETE')  # Example of sending with DELETE method
    def send_remove_channel_request(self, url, channel_name):
        """Removes a channel."""
        args_dict = {
            'url': url,
            'channel_name': channel_name
        }
        print(f"Removing channel {channel_name}...")
        return args_dict
