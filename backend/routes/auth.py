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
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@auth_bp.route("/register", methods=["POST"])
def register():
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
        "username": user.username
    })


@auth_bp.route("/me", methods=["GET"])
@authenticate
def get_me():
    """Get current logged in user profile"""
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
    """Update current user's username or email"""
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
    """Change current user password"""
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
    """
    JWT logout — tokens are stateless so we just confirm on server side.
    Frontend is responsible for deleting the token from localStorage.
    """
    return jsonify({"message": "Logged out successfully"})