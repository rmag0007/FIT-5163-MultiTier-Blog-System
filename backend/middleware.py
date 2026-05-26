"""Request middleware and decorators for authentication and access control.

Provides `authenticate` to validate JWTs and attach user info to the
request, and `require_premium` to gate premium-only endpoints.
"""

import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
from config import Config


def authenticate(f):
    """Decorator that verifies a Bearer JWT and attaches the payload.

    On success `request.user` will contain the token payload (user_id,
    tier, etc.). Returns `401` for missing/invalid/expired tokens.
    """
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
    """Decorator to restrict access to premium-tier users only.

    Assumes `authenticate` has already run and populated `request.user`.
    Returns `403` when the user's tier is not `premium`.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user.get("tier") != "premium":
            return jsonify({"error": "Premium access required"}), 403
        return f(*args, **kwargs)
    return decorated