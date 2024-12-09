import config
import requests

try:
    # Send a GET request to the server
    response = requests.get(config.SERVER_URL, verify=False)
    print(f"Response from server: {response.json()}")
except requests.exceptions.SSLError as e:
    print(f"SSL error: {e}")
except Exception as e:
    print(f"Error: {e}")
