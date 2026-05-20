# Secure Multi-Tier Blog Activity Analytics System

A comprehensive blog platform with a security-focused user activity tracking system 
that provides tiered access to analytics data based on blogger privilege levels.

Built for FIT5163 Group Assignment — Monash University, S1 2026.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Supabase account (free tier is sufficient)

### Clone the Repository
```bash
git clone <your-repo-url>
cd blog-analytics
```

###  Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                   # Starts HTTPS server on https://localhost:5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev                     # Starts on http://localhost:5173
```


### Configure Environment Variables -- NOT YET DONE!
Create a `.env` file in the root directory — get the values from your group privately:
DATABASE_URL=postgresql://your-supabase-connection-string
JWT_SECRET=your-very-long-random-secret-key
ENCRYPTION_KEY=your-32-byte-fernet-key
FLASK_ENV=development

## Environment Notes
- Never commit `.env` to version control — it is listed in `.gitignore`
- All group members share the same Supabase database via the connection string
- The `db.create_all()` call in `app.py` automatically creates tables on first run
---