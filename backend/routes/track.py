from flask import Blueprint, request, jsonify
from extensions import db
from models import ActivityLog
from utils.encryption import encrypt, get_country_from_ip

track_bp = Blueprint("track", __name__)

ALLOWED_EVENTS = ["view", "like", "comment", "share"]

@track_bp.route("/track", methods=["POST"])
def track():
    """Record anonymous activity events for a blog post."""
    data = request.get_json()

    # Require all keys needed to identify and classify the event.
    required = ["post_id", "event_type", "session_id"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    if data["event_type"] not in ALLOWED_EVENTS:
        return jsonify({"error": f"Invalid event type. Must be one of: {ALLOWED_EVENTS}"}), 400

    try:
        post_id = int(data["post_id"])
    except (ValueError, TypeError):
        return jsonify({"error": "post_id must be an integer"}), 400

    # Use default values when optional analytics fields are omitted.
    time_spent = data.get("time_spent_seconds", 0)
    scroll_depth = data.get("scroll_depth_percent", 0)

    if not isinstance(time_spent, (int, float)) or time_spent < 0:
        return jsonify({"error": "time_spent_seconds must be a non-negative number"}), 400

    if not isinstance(scroll_depth, (int, float)) or not (0 <= scroll_depth <= 100):
        return jsonify({"error": "scroll_depth_percent must be between 0 and 100"}), 400

    # Resolve the client IP on the server and store it only in encrypted form.
    ip_raw = request.remote_addr or "unknown"
    country = get_country_from_ip(ip_raw)
    ip_encrypted = encrypt(ip_raw)

    log = ActivityLog(
        post_id=post_id,
        session_id=data["session_id"],
        event_type=data["event_type"],
        time_spent_seconds=int(time_spent),
        scroll_depth_percent=int(scroll_depth),
        ip_encrypted=ip_encrypted,
        country=country,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "Event tracked",
        "event_type": data["event_type"],
        "post_id": post_id
    }), 201


@track_bp.route("/track/summary/<int:post_id>", methods=["GET"])
def track_summary(post_id):
    """Return aggregate counts for each event type on a given post."""
    counts = {}
    for event in ALLOWED_EVENTS:
        counts[event] = ActivityLog.query.filter_by(
            post_id=post_id,
            event_type=event
        ).count()

    return jsonify({
        "post_id": post_id,
        "summary": counts
    }), 200