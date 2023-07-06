import hashlib
from rest_framework import exceptions
import jwt

def encode_password(password):
    # Encode the password using SHA256 hash algorithm
    encoded_password = hashlib.sha256(password.encode()).hexdigest()
    print(encode_password)
    return encoded_password

def verify_password(password, encoded_password):
    # Verify if the provided password matches the encoded password
    return hashlib.sha256(password.encode()).hexdigest() == encoded_password

def create_jwt_token(payload):
    jwt_token = jwt.encode(
				{'payload': payload},'secret',algorithm='HS256')
    return jwt_token


def create_jwt_token_user(payload):
    jwt_token = jwt.encode(
				{'payload': payload},'secret',algorithm='HS256')
    return jwt_token