import hashlib
import time
import re

class Tools:
    @staticmethod
    def hash(password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    @staticmethod
    def generate_sessionID(username, sha_password):
        # Generate a base string combining username, password hash, and current timestamp
        current_timestamp = str(int(time.time()))  # Current timestamp in seconds
        base_string = f"{username}{sha_password}{current_timestamp}"

        # Create SHA-256 hash of the base string
        session_hash = hashlib.sha256(base_string.encode()).hexdigest()

        # Extract the first 32 alphanumeric lowercase characters
        alphanumeric_hash = re.sub(r'[^a-z0-9]', '', session_hash)[:32]
        return alphanumeric_hash

