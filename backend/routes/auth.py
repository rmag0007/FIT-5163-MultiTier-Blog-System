import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from app import db
from models import User
from utils.encryption import encrypt
from config import Config

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    tier = data.get("tier", "basic")  # default to basic

    if not all([username, email, password]):
        return jsonify({"error": "All fields required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
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

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "username": user.username,
        "tier": user.tier,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }, Config.JWT_SECRET, algorithm="HS256")

    return jsonify({"token": token, "tier": user.tier})