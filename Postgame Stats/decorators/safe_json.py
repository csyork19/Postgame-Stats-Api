from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import BadRequest


def safe_json(required_fields=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json(force=True)
                if required_fields:
                    for field in required_fields:
                        if field not in data:
                            return jsonify({"error": f"Missing field: {field}"}), 400
                return f(data, *args, **kwargs)
            except BadRequest:
                return jsonify({"error": "Invalid JSON"}), 400
            except Exception as e:
                return jsonify({"error": "Internal server error"}), 500

        return wrapper

    return decorator
