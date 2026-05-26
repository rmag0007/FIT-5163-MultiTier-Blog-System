"""Authentication routes for the blog analytics application.

This module exposes endpoints for registering, logging in, and
managing the authenticated user's profile. Sensitive data such as
email addresses are stored encrypted and passwords are hashed.
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from utils.encryption import encrypt, decrypt
from config import Config
from middleware import authenticate
import re

auth_bp = Blueprint("auth", __name__)

def is_valid_email(email: str) -> bool:
    """Return True when the provided string is a plausible email.

    This uses a simple regex to validate common email formats; it is
    intentionally permissive for test/demo purposes and not a full
    production-grade validator.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@auth_bp.route("/register", methods=["POST"])
def register():
    """Create a new user account.

    Expects JSON with `username`, `email`, `password` and an optional
    `tier` (basic|premium). Passwords are hashed before storing and
    the email is encrypted to protect PII at rest.
    """
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    tier = data.get("tier", "basic")

    if not all([username, email, password]):
        return jsonify({"error": "All fields required"}), 400

    if tier not in ["basic", "premium"]:
        return jsonify({"error": "Tier must be basic or premium"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    password_hash = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()
    email_encrypted = encrypt(email)

    user = User(
        username=username,
        email_encrypted=email_encrypted,
        password_hash=password_hash,
        tier=tier
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a JWT token on success."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(
        password.encode(), user.password_hash.encode()
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "username": user.username,
        "tier": user.tier,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }, Config.JWT_SECRET, algorithm="HS256")

    return jsonify({
        "token": token,
        "tier": user.tier,
        "username": user.username,
        "user_id": user.id
    })


@auth_bp.route("/me", methods=["GET"])
@authenticate
def get_me():
    """Return the currently authenticated user's public profile.

    The email value is decrypted on the fly for the response; only
    limited profile fields are returned to avoid exposing unnecessary
    data.
    """
    user = User.query.get(request.user["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": decrypt(user.email_encrypted),
        "tier": user.tier,
        "created_at": str(user.created_at)
    })


@auth_bp.route("/me", methods=["PUT"])
@authenticate
def update_me():
    """Allow the authenticated user to update username or email.

    Username uniqueness is enforced; emails are stored encrypted.
    """
    data = request.get_json()
    user = User.query.get(request.user["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "username" in data:
        existing = User.query.filter_by(
            username=data["username"]
        ).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Username already taken"}), 409
        user.username = data["username"]

    if "email" in data:
        user.email_encrypted = encrypt(data["email"])

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})


@auth_bp.route("/password", methods=["PUT"])
@authenticate
def update_password():
    """Change the authenticated user's password.

    The current password must be provided and verified before the
    new password is accepted and re-hashed.
    """
    data = request.get_json()
    current = data.get("current_password")
    new = data.get("new_password")

    if not all([current, new]):
        return jsonify({"error": "Current and new password required"}), 400

    if len(new) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    user = User.query.get(request.user["user_id"])
    if not bcrypt.checkpw(current.encode(), user.password_hash.encode()):
        return jsonify({"error": "Current password is incorrect"}), 401

    user.password_hash = bcrypt.hashpw(
        new.encode(), bcrypt.gensalt()
    ).decode()
    db.session.commit()
    return jsonify({"message": "Password updated successfully"})


@auth_bp.route("/logout", methods=["POST"])
@authenticate
def logout():
    """Logout endpoint (stateless).

    Since JWTs are stateless the server cannot revoke tokens here; the
    frontend should remove the token from storage to complete logout.
    """
    return jsonify({"message": "Logged out successfully"})