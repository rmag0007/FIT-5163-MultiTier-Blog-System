import requests
import json

# Disable SSL warnings since we're using self-signed cert
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://127.0.0.1:5000"

# Store tokens for use across tests
tokens = {
    "basic": None,
    "premium": None
}
post_id = None
premium_post_id = None

def print_result(test_name, response, expected_status):
    status = "PASS" if response.status_code == expected_status else "FAIL"
    print(f"\n{status} — {test_name}")
    print(f"  Expected: {expected_status} | Got: {response.status_code}")
    try:
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"  Response: {response.text}")

def test_register_basic():
    res = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "password123",
        "tier": "basic"
    }, verify=False)
    print_result("Register Basic Blogger (alice)", res, 201)

def test_register_premium():
    res = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "password123",
        "tier": "premium"
    }, verify=False)
    print_result("Register Premium Blogger (bob)", res, 201)

def test_login_basic():
    res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "alice",
        "password": "password123"
    }, verify=False)
    print_result("Login Basic Blogger (alice)", res, 200)
    if res.status_code == 200:
        tokens["basic"] = res.json().get("token")
        print(f"Token saved for alice")

def test_login_premium():
    res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "bob",
        "password": "password123"
    }, verify=False)
    print_result("Login Premium Blogger (bob)", res, 200)
    if res.status_code == 200:
        tokens["premium"] = res.json().get("token")
        print(f"Token saved for bob")


def test_create_post():
    global post_id
    if not tokens["basic"]:
        print("\nSKIP — Create Post (no token, login failed)")
        return
    res = requests.post(f"{BASE_URL}/api/posts", json={
        "title": "My First Blog Post",
        "content": "This is a test post for analytics tracking."
    }, headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Create Test Post", res, 201)
    if res.status_code == 201:
        post_id = res.json().get("post_id")
        print(f"Post ID saved: {post_id}")


def test_track_activity():
    if not post_id:
        print("\nSKIP — Track Activity (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-abc",
        "event_type": "view",
        "time_spent_seconds": 45,
        "scroll_depth_percent": 60
    }, verify=False)
    print_result("Track Activity Event", res, 201)

def test_invalid_event_type():
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-abc",
        "event_type": "invalid_event",
    }, verify=False)
    print_result("Track Invalid Event Type (should fail)", res, 400)

def test_basic_stats():
    if not tokens["basic"]:
        print("\nSKIP — Basic Stats (no token, login failed)")
        return
    res = requests.get(f"{BASE_URL}/api/dashboard/stats/basic", headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Basic Blogger Accesses Basic Stats", res, 200)

def test_basic_blocked_from_premium():
    if not tokens["basic"]:
        print("\nSKIP — Premium Block Test (no token, login failed)")
        return
    res = requests.get(f"{BASE_URL}/api/dashboard/stats/premium", headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Basic Blogger Blocked from Premium Stats (should be 403)", res, 403)

def test_premium_stats():
    if not tokens["premium"]:
        print("\nSKIP — Premium Stats (no token, login failed)")
        return
    res = requests.get(f"{BASE_URL}/api/dashboard/stats/premium", headers={
        "Authorization": f"Bearer {tokens['premium']}"
    }, verify=False)
    print_result("Premium Blogger Accesses Premium Stats", res, 200)

def test_no_token():
    res = requests.get(f"{BASE_URL}/api/dashboard/stats/basic", verify=False)
    print_result("Access Dashboard Without Token (should be 401)", res, 401)

def test_duplicate_register():
    res = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "password123",
        "tier": "basic"
    }, verify=False)
    print_result("Duplicate Register (should be 409)", res, 409)

def test_wrong_password():
    res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "alice",
        "password": "wrongpassword"
    }, verify=False)
    print_result("Login Wrong Password (should be 401)", res, 401)

def test_track_comment():
    if not post_id:
        print("\nSKIP — Track Comment (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-abc",
        "event_type": "comment",
        "time_spent_seconds": 120,
        "scroll_depth_percent": 80
    }, verify=False)
    print_result("Track Comment Event", res, 201)

def test_track_share():
    if not post_id:
        print("\nSKIP — Track Share (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-xyz",
        "event_type": "share",
        "time_spent_seconds": 30,
        "scroll_depth_percent": 100
    }, verify=False)
    print_result("Track Share Event", res, 201)

def test_track_like():
    if not post_id:
        print("\nSKIP — Track Like (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-def",
        "event_type": "like",
        "time_spent_seconds": 60,
        "scroll_depth_percent": 45
    }, verify=False)
    print_result("Track Like Event", res, 201)

def test_track_invalid_scroll():
    if not post_id:
        print("\n  SKIP — Invalid Scroll (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-abc",
        "event_type": "view",
        "time_spent_seconds": 30,
        "scroll_depth_percent": 150  # invalid, over 100
    }, verify=False)
    print_result("Track Invalid Scroll Depth (should fail)", res, 400)

def test_track_negative_time():
    if not post_id:
        print("\n  SKIP — Negative Time (no post created yet)")
        return
    res = requests.post(f"{BASE_URL}/api/track", json={
        "post_id": post_id,
        "session_id": "test-session-abc",
        "event_type": "view",
        "time_spent_seconds": -10,  # invalid
        "scroll_depth_percent": 50
    }, verify=False)
    print_result("Track Negative Time Spent (should fail)", res, 400)

def test_track_summary():
    if not post_id:
        print("\n  SKIP — Track Summary (no post created yet)")
        return
    res = requests.get(f"{BASE_URL}/api/track/summary/{post_id}", verify=False)
    print_result("Get Activity Summary for Post", res, 200)
    if res.status_code == 200:
        print(f"  Summary: {json.dumps(res.json()['summary'], indent=2)}")

def test_create_premium_post():
    if not tokens["premium"]:
        print("\nSKIP — Create Premium Post (no token)")
        return
    global premium_post_id
    res = requests.post(f"{BASE_URL}/api/posts", json={
        "title": "Bob's Premium Blog Post",
        "content": "A detailed analysis of cryptographic techniques in modern web applications."
    }, headers={
        "Authorization": f"Bearer {tokens['premium']}"
    }, verify=False)
    print_result("Create Premium User Post", res, 201)
    if res.status_code == 201:
        premium_post_id = res.json().get("post_id")
        print(f"  Premium Post ID saved: {premium_post_id} ")

def test_track_premium_post_activity():
    if not premium_post_id:
        print("\nSKIP — Track Premium Post Activity (no post)")
        return
    events = [
        ("view", 120, 90, "session-p1"),
        ("view", 200, 100, "session-p2"),
        ("like", 150, 75, "session-p1"),
        ("comment", 300, 95, "session-p3"),
        ("share", 90, 60, "session-p2"),
    ]
    for event, time, scroll, session in events:
        requests.post(f"{BASE_URL}/api/track", json={
            "post_id": premium_post_id,
            "session_id": session,
            "event_type": event,
            "time_spent_seconds": time,
            "scroll_depth_percent": scroll
        }, verify=False)
    print(f"\nINFO — Tracked 5 events on premium post {premium_post_id}")

def test_premium_stats_with_data():
    if not tokens["premium"]:
        print("\nSKIP — Premium Stats With Data (no token)")
        return
    res = requests.get(f"{BASE_URL}/api/dashboard/stats/premium", headers={
        "Authorization": f"Bearer {tokens['premium']}"
    }, verify=False)
    print_result("Premium Stats With Real Data", res, 200)


def test_get_me():
    if not tokens["basic"]:
        print("\nSKIP — Get Me (no token)")
        return
    res = requests.get(f"{BASE_URL}/api/auth/me", headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Get Current User Profile", res, 200)

def test_get_posts():
    res = requests.get(f"{BASE_URL}/api/posts", verify=False)
    print_result("Get All Posts (public)", res, 200)

def test_get_single_post():
    if not post_id:
        print("\nSKIP — Get Single Post (no post)")
        return
    res = requests.get(f"{BASE_URL}/api/posts/{post_id}", verify=False)
    print_result("Get Single Post by ID", res, 200)

def test_get_nonexistent_post():
    res = requests.get(f"{BASE_URL}/api/posts/99999", verify=False)
    print_result("Get Nonexistent Post (should 404)", res, 404)

def test_update_post():
    if not tokens["basic"] or not post_id:
        print("\nSKIP — Update Post (no token or post)")
        return
    res = requests.put(f"{BASE_URL}/api/posts/{post_id}", json={
        "title": "Updated Post Title",
        "content": "Updated content for testing."
    }, headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Update Own Post", res, 200)

def test_update_post_wrong_user():
    if not tokens["premium"] or not post_id:
        print("\nSKIP — Update Wrong User Post (no token or post)")
        return
    res = requests.put(f"{BASE_URL}/api/posts/{post_id}", json={
        "title": "Trying to hijack alice's post"
    }, headers={
        "Authorization": f"Bearer {tokens['premium']}"
    }, verify=False)
    print_result("Update Another User's Post (should 403)", res, 403)

def test_delete_post_wrong_user():
    if not tokens["premium"] or not post_id:
        print("\nSKIP — Delete Wrong User Post (no token or post)")
        return
    res = requests.delete(f"{BASE_URL}/api/posts/{post_id}", headers={
        "Authorization": f"Bearer {tokens['premium']}"
    }, verify=False)
    print_result("Delete Another User's Post (should 403)", res, 403)

def test_logout():
    if not tokens["basic"]:
        print("\nSKIP — Logout (no token)")
        return
    res = requests.post(f"{BASE_URL}/api/auth/logout", headers={
        "Authorization": f"Bearer {tokens['basic']}"
    }, verify=False)
    print_result("Logout", res, 200)

def test_invalid_email():
    res = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "baduser",
        "email": "notanemail",
        "password": "password123",
        "tier": "basic"
    }, verify=False)
    print_result("Register Invalid Email (should 400)", res, 400)

if __name__ == "__main__":
    print("=" * 50)
    print("  BLOG ANALYTICS API TEST SUITE")
    print("=" * 50)

    print("\n--- REGISTRATION ---")
    test_register_basic()
    test_register_premium()
    test_duplicate_register()
    test_invalid_email()

    print("\n--- AUTH ---")
    test_login_basic()
    test_login_premium()
    test_wrong_password()
    test_get_me()

    print("\n--- POSTS ---")
    test_get_posts()
    test_create_post()
    test_get_single_post()
    test_get_nonexistent_post()
    test_update_post()
    test_update_post_wrong_user()

    print("\n--- PREMIUM USER POSTS ---")
    test_create_premium_post()
    test_track_premium_post_activity()
    test_premium_stats_with_data()

    print("\n--- ACTIVITY TRACKING ---")
    test_track_activity()       # view
    test_track_like()           # like
    test_track_comment()        # comment
    test_track_share()          # share
    test_invalid_event_type()   # invalid event
    test_track_invalid_scroll() # invalid scroll depth
    test_track_negative_time()  # invalid time spent
    test_track_summary()        # summary check

    print("\n--- DASHBOARD ACCESS ---")
    test_no_token()
    test_basic_stats()
    test_basic_blocked_from_premium()
    test_premium_stats()
    test_premium_stats_with_data()

    print("\n--- CLEANUP (delete own post) ---")
    test_delete_post_wrong_user()
    test_logout()

    print("\n" + "=" * 50)
    print("  TESTS COMPLETE")
    print("=" * 50)