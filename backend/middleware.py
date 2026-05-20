import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
from config import Config

def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Missing token"}), 401
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            request.user = payload  # Attach user info to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def require_premium(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user.get("tier") != "premium":
            return jsonify({"error": "Premium access required"}), 403
        return f(*args, **kwargs)
    return decorated