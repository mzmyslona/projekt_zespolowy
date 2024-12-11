import requests
import config
import json
from user import User

class RequestSendException(Exception):
    pass

class RequestCreator:
    """Class that contains methods for sending requests and applying decorators."""

    def __init__(self):
        self.user_identity = None

    def authorization(func):
        """Authorization decorator that adds 'authorization' field to the dictionary."""
        def wrapper(*args, **kwargs):
            args_dict = func(*args, **kwargs)  # Get the dictionary from the original function
            if not (isinstance(args_dict, dict) and len(args_dict) > 0):
                raise RequestSendException("Invalid arguments for request.")
            if not self.user_identity:
                raise RequestSendException("Cannot authorize user. User identity was not set up yet.")

            # Extend the dictionary with user identity for authorization
            args_dict['data']['session_id'] = self.user_identity.session_id
            return args_dict  # Return the modified dictionary
        return wrapper

    def send(http_method):
        """Send decorator that sends the dictionary arguments to the specified HTTP request method."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Get the dictionary of arguments with authorization field
                args_dict = func(*args, **kwargs)
                print(f"Sending request with {http_method} method")

                # Sending data to server using the specified HTTP method
                url = args_dict.get("url")
                try:
                    if http_method == 'GET':
                        response = requests.get(url, params=args_dict['data'], verify=False)
                    elif http_method == 'POST':
                        response = requests.post(url, json=args_dict['data'], verify=False)
                    elif http_method == 'DELETE':
                        response = requests.delete(url, json=args_dict['data'], verify=False)
                    else:
                        raise RequestSendException("Cannot authorize user. User identity was not set up yet.")
                    return response  # Return the response from the request
                except BaseException as e:
                    raise RequestSendException(e.message)
            return wrapper
        return decorator

    def set_user_identity(user_identity):
        self.user_identity = user_identity

    @send('POST')
    def send_log_in_request(self, user):
        user_data = { 'username': user.username,
                      'password': user.password }
        args_dict = { 'url': f'{config.SERVER_URL}/login',
                      'data': user_data }
        return args_dict

    @authorization
    @send('POST')  # Example of sending with POST method
    def send_create_channel_request(self, url, channel_name):
        args_dict = {
            'url': url,
        }
        return args_dict

    @authorization
    @send('GET')  # Example of sending with GET method
    def send_list_channels_request(self, url):
        args_dict = {
            'url': url
        }
        return args_dict

    @authorization
    @send('POST')  # Example of sending with POST method
    def send_add_channel_member_request(self, url, channel_name, user_to_add):
        args_dict = {
            'url': url,
        }
        return args_dict

    @authorization
    @send('DELETE')  # Example of sending with DELETE method
    def send_remove_channel_request(self, url, channel_name):
        args_dict = {
            'url': url,
        }
        return args_dict
