from functools import wraps
from flask import request, jsonify


def with_json(required_fields=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            if required_fields:
                for f_name in required_fields:
                    if f_name not in data:
                        return jsonify({"error": f"Missing required field: {f_name}"}), 400
            return f(data, *args, **kwargs)

        return wrapper

    return decorator
