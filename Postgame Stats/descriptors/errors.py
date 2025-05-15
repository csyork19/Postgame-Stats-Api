from flask import jsonify
from werkzeug.exceptions import HTTPException


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            return jsonify({'error': e.description}), e.code
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500

    wrapper.__name__ = func.__name__
    return wrapper
