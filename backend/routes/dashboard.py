from flask import Blueprint, jsonify, request
from extensions import db
from models import ActivityLog, Post
from middleware import authenticate, require_premium
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/stats/basic", methods=["GET"])
@authenticate
def basic_stats():
    # Only show stats for posts owned by the logged-in blogger
    user_id = request.user["user_id"]
    posts = Post.query.filter_by(author_id=user_id).all()
    post_ids = [p.id for p in posts]

    stats = []
    for post in posts:
        views = ActivityLog.query.filter_by(post_id=post.id, event_type="view").count()
        likes = ActivityLog.query.filter_by(post_id=post.id, event_type="like").count()
        stats.append({
            "post_id": post.id,
            "title": post.title,
            "total_views": views,
            "total_likes": likes,
        })

    return jsonify(stats)


@dashboard_bp.route("/stats/premium", methods=["GET"])
@authenticate
@require_premium  # This is the key security gate
def premium_stats():
    user_id = request.user["user_id"]
    posts = Post.query.filter_by(author_id=user_id).all()

    stats = []
    for post in posts:
        logs = ActivityLog.query.filter_by(post_id=post.id).all()

        avg_time = db.session.query(
            func.avg(ActivityLog.time_spent_seconds)
        ).filter_by(post_id=post.id).scalar() or 0

        avg_scroll = db.session.query(
            func.avg(ActivityLog.scroll_depth_percent)
        ).filter_by(post_id=post.id).scalar() or 0

        # Time series: group views by date
        time_series = db.session.query(
            func.date(ActivityLog.timestamp),
            func.count(ActivityLog.id)
        ).filter_by(post_id=post.id, event_type="view")\
         .group_by(func.date(ActivityLog.timestamp)).all()

        country_breakdown = db.session.query(
            ActivityLog.country,
            func.count(ActivityLog.id)
        ).filter_by(post_id=post.id).group_by(ActivityLog.country).all()

        stats.append({
            "post_id": post.id,
            "title": post.title,
            "total_views": len([l for l in logs if l.event_type == "view"]),
            "total_likes": len([l for l in logs if l.event_type == "like"]),
            "total_comments": len([l for l in logs if l.event_type == "comment"]),
            "total_shares": len([l for l in logs if l.event_type == "share"]),
            "avg_time_spent_seconds": round(float(avg_time), 2),
            "avg_scroll_depth_percent": round(float(avg_scroll), 2),
            "time_series": [{"date": str(row[0]), "views": row[1]} for row in time_series],
            "country_breakdown": [{"country": row[0], "count": row[1]} for row in country_breakdown],
        })

    return jsonify(stats)