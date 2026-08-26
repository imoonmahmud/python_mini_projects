from functools import wraps
import jwt
from flask import request

SECRET_KEY = 'imoonmahmud'

def validate_register(data):
    required_fields = ('username', 'password')

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    not_string = [field for field in required_fields if not isinstance(data[field], str)]
    if not_string:
        raise ValueError(f"{', '.join(not_string)} field(s) must be string.")

    if len(data['password']) < 8:
        raise ValueError('Password must be at least 8 characters long.')


def validate_create_expense(data):
    required_fields = ('title', 'amount')

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    if not isinstance(data['amount'], int):
        raise ValueError(f"'amount' must be number")

    if not isinstance(data['title'], str):
        raise ValueError(f"'title' must be text")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token missing'}, 401

        # allow "Bearer <token>" or a bare token
        if token.startswith('Bearer '):
            token = token.split(' ', 1)[1]

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401
        return f(data['user'], *args, **kwargs)
    return decorated_function