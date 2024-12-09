from os import path, pardir
ROOT_DIR = path.abspath(path.join(path.dirname(__file__), pardir))
SERVER_URL = "https://139.59.145.2"
SERVER_CERT = path.join(ROOT_DIR, "setup", "cert.pem")
