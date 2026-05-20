from flask import Blueprint, request, jsonify
from app import db
from models import ActivityLog
from utils.encryption import encrypt

track_bp = Blueprint("track", __name__)

@track_bp.route("/track", methods=["POST"])
def track():
    data = request.get_json()

    # Basic input validation
    required = ["post_id", "event_type", "session_id"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    allowed_events = ["view", "like", "comment", "share"]
    if data["event_type"] not in allowed_events:
        return jsonify({"error": "Invalid event type"}), 400

    ip_raw = request.remote_addr or "unknown"
    ip_encrypted = encrypt(ip_raw)

    log = ActivityLog(
        post_id=data["post_id"],
        session_id=data["session_id"],
        event_type=data["event_type"],
        time_spent_seconds=data.get("time_spent_seconds", 0),
        scroll_depth_percent=data.get("scroll_depth_percent", 0),
        ip_encrypted=ip_encrypted,
        country=data.get("country", "unknown")
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Event tracked"}), 201