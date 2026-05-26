"""Public CRUD endpoints for blog posts.

Provides simple create/read/update/delete operations. Creation and
mutating operations require authentication and enforce ownership.
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models import Post
from middleware import authenticate

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/posts", methods=["GET"])
def get_posts():
    """Get all posts — public, no auth needed"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "author_id": p.author_id,
        "created_at": str(p.created_at)
    } for p in posts])


@posts_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    """Get a single post by ID — public, no auth needed"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "created_at": str(post.created_at)
    })


@posts_bp.route("/posts", methods=["POST"])
@authenticate
def create_post():
    """Create a new post — requires login"""
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not all([title, content]):
        return jsonify({"error": "Title and content required"}), 400

    if len(title) > 200:
        return jsonify({"error": "Title must be under 200 characters"}), 400

    post = Post(
        title=title,
        content=content,
        author_id=request.user["user_id"]
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "Post created",
        "post_id": post.id
    }), 201


@posts_bp.route("/posts/<int:post_id>", methods=["PUT"])
@authenticate
def update_post(post_id):
    """Edit a post — only the author can edit their own post"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Ownership check — security point
    if post.author_id != request.user["user_id"]:
        return jsonify({"error": "You can only edit your own posts"}), 403

    data = request.get_json()
    if "title" in data:
        if len(data["title"]) > 200:
            return jsonify({"error": "Title must be under 200 characters"}), 400
        post.title = data["title"]

    if "content" in data:
        post.content = data["content"]

    db.session.commit()
    return jsonify({"message": "Post updated successfully"})


@posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@authenticate
def delete_post(post_id):
    """Delete a post — only the author can delete their own post"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Ownership check — security point
    if post.author_id != request.user["user_id"]:
        return jsonify({"error": "You can only delete your own posts"}), 403

    # Delete related activity logs first to avoid foreign key violation
    from models import ActivityLog
    ActivityLog.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"})