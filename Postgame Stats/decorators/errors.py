from urllib import request

from flask import jsonify
from werkzeug.exceptions import HTTPException


def require_json(func):
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Expected application/json'}), 400
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            return jsonify({'error asdfasdf': e.description}), e.code
        except Exception as e:
            return jsonify({'error': 'Internal server error hello TF'}), 500

    wrapper.__name__ = func.__name__
    return wrapper
