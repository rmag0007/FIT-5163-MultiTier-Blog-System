"""Configuration loaded from environment variables.

Wraps environment values used across the application. Ensure a
`.env` file or environment has `DATABASE_URL`, `JWT_SECRET` and
`ENCRYPTION_KEY` set before running the server.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET")
    # ENCRYPTION_KEY should be a Fernet-compatible key stored in env
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()