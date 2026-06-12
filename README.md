# Secure Multi-Tier Blog Activity Analytics System

A full-stack blog platform with security-focused user activity tracking and tiered analytics access based on blogger privilege levels.

Built for FIT5163 — Introduction to Cryptography for Cybersecurity, Monash University, S1 2026.

---

## Group Members

| Name | Student ID |
|------|------------|
| Rishi Magavi | 36425230 |
| Sujal Jain | 36754161 |
| Adwait Gadre | 36647918 |
| Luke Phillips | 32511760 |

---

## Project Structure
blog-analytics/

├── backend/

│   ├── app.py                  # Flask app entry point

│   ├── config.py               # Environment variable loading

│   ├── extensions.py           # SQLAlchemy instance

│   ├── models.py               # Database models

│   ├── middleware.py           # JWT auth + tier enforcement

│   ├── routes/

│   │   ├── auth.py             # /api/auth — register, login, profile

│   │   ├── posts.py            # /api/posts — full CRUD

│   │   ├── track.py            # /api/track — activity logging

│   │   └── dashboard.py        # /api/dashboard — tiered analytics

│   ├── utils/

│   │   └── encryption.py       # Fernet encrypt/decrypt + geolocation

│   └── requirements.txt

│

├── frontend/

│   ├── src/

│   │   ├── api/

│   │   │   └── client.js       # Axios instance with JWT interceptor

│   │   ├── components/

│   │   │   ├── Blog/

│   │   │   │   ├── BlogHome.jsx

│   │   │   │   └── BlogPost.jsx

│   │   │   └── Dashboard/

│   │   │       ├── BasicDashboard.jsx

│   │   │       └── PremiumDashboard.jsx

│   │   ├── pages/

│   │   │   ├── Login.jsx

│   │   │   ├── Register.jsx

│   │   │   ├── Dashboard.jsx

│   │   │   ├── CreatePost.jsx

│   │   │   └── BlogPostPage.jsx

│   │   ├── App.jsx

│   │   └── main.jsx

│   ├── vite.config.js

│   └── package.json

│

├── .env                        # Never committed — shared privately

├── .gitignore

└── README.md

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19 + Vite |
| Backend | Python + Flask |
| Database | PostgreSQL via Supabase |
| ORM | SQLAlchemy |
| Auth | JWT — PyJWT with HMAC-SHA256 |
| Password Hashing | bcrypt |
| Encryption | Fernet — AES-128-CBC + HMAC-SHA256 |
| HTTPS | mkcert locally trusted certificates |

---

## Security Features

| Feature | Implementation | Protects Against |
|---------|---------------|-----------------|
| Password hashing | bcrypt with salt | Rainbow table attacks, brute force |
| PII encryption | Fernet (AES-128-CBC + HMAC-SHA256) | Database breach exposure |
| Authentication | JWT with 1hr expiry (HMAC-SHA256) | Token forgery, replay attacks |
| Secure transmission | HTTPS via mkcert certificates | Network interception |
| DB connection | sslmode=require | Transit interception to Supabase |
| Tier enforcement | Backend decorator — @require_premium | Privilege escalation |
| Input validation | Whitelist + boundary checks | Injection, malformed data |
| IP geolocation | Server-side via ip-api.com | Client location spoofing |

---

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | No | Register blogger |
| POST | /api/auth/login | No | Login, returns JWT |
| GET | /api/auth/me | JWT | Get current user profile |
| PUT | /api/auth/me | JWT | Update profile |
| PUT | /api/auth/password | JWT | Change password |
| POST | /api/auth/logout | JWT | Logout |

### Posts
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/posts | No | Get all posts |
| GET | /api/posts/:id | No | Get single post |
| POST | /api/posts | JWT | Create post |
| PUT | /api/posts/:id | JWT | Edit own post |
| DELETE | /api/posts/:id | JWT | Delete own post |

### Tracking
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/track | No | Log activity event |
| GET | /api/track/summary/:id | No | Get event counts for post |

### Dashboard
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/dashboard/stats/basic | JWT (any tier) | Views and likes per post |
| GET | /api/dashboard/stats/premium | JWT (premium only) | Full analytics |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- mkcert (for HTTPS)
- Supabase project with connection string

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd blog-analytics
```

### 2. Configure Environment Variables
Create a `.env` file in the `backend/` directory — get values from your group privately:
DATABASE_URL=postgresql://postgres.xxx:password@host:5432/postgres?sslmode=require

JWT_SECRET=your-long-random-secret

ENCRYPTION_KEY=your-fernet-key

FLASK_ENV=development

To generate a fresh Fernet key:
```bash
cd backend
python utils/encryption.py
```

### 3. Generate HTTPS Certificates

```bash
# Install local CA (run once)
mkcert -install

# Backend cert
cd backend
mkcert 127.0.0.1 localhost

# Frontend cert
cd frontend
mkcert localhost
```

### 4. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                  # Starts on https://127.0.0.1:5000
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev                    # Starts on https://localhost:5173
```

### 6. Accept Certificates in Browser
On first run, visit both URLs and accept the certificate:
- `https://127.0.0.1:5000/api/posts`
- `https://localhost:5173`

---

## Database Tables

Tables are managed directly via the Supabase SQL Editor — not auto-generated. Run this SQL to create them:

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email_encrypted TEXT NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    tier VARCHAR(20) NOT NULL DEFAULT 'basic',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) NOT NULL,
    session_id VARCHAR(100),
    event_type VARCHAR(50),
    time_spent_seconds INTEGER DEFAULT 0,
    scroll_depth_percent INTEGER DEFAULT 0,
    ip_encrypted TEXT,
    country VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## How Tiered Access Works

Readers browse the blog anonymously. Activity is tracked silently via `/api/track`. Bloggers log in and receive a JWT containing their tier.

- **Basic bloggers** — see total views and likes per post
- **Premium bloggers** — see full analytics including avg time spent, avg scroll depth, views over time, and country breakdown
- Calling a premium endpoint with a basic token returns **HTTP 403 Forbidden**
- Tier enforcement happens on the **backend**, not just the UI

---

## Notes

- Never commit `.env` — it is listed in `.gitignore`
- Never commit `*.pem` certificate files — also in `.gitignore`
- The `test_api.py` file is excluded from version control
- All group members connect to the same Supabase database via the shared connection string