"""Encryption helpers for small-scale PII protection.

Uses Fernet symmetric encryption to protect sensitive strings such
as user emails and client IPs stored in the database. Also provides a
small helper to perform a best-effort country lookup for an IP.
"""

import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import requests as http_requests

load_dotenv()


def get_fernet():
    """Return a Fernet instance configured from the environment.

    Raises a ValueError when `ENCRYPTION_KEY` is not set so callers
    fail fast in development.
    """
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in .env")
    return Fernet(key.encode())


def encrypt(value: str) -> str:
    """Encrypt and return a UTF-8 string safe for storage."""
    return get_fernet().encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    """Decrypt a stored string back to plaintext."""
    return get_fernet().decrypt(value.encode()).decode()


def get_country_from_ip(ip: str) -> str:
    """Lookup of an IP's country using a free external API.

    This function is defensive: it avoids looking up localhost addresses
    and uses a short timeout to avoid blocking the request path.
    """
    try:
        # Don't look up localhost IPs
        if ip in ("127.0.0.1", "localhost", "::1"):
            return "localhost"
        response = http_requests.get(
            f"http://ip-api.com/json/{ip}?fields=country",
            timeout=3  # don't hang if the service is slow
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("country", "unknown")
    except Exception:
        return "unknown"
    return "unknown"

# Run this once to generate a key, paste it in .env
if __name__ == "__main__":
    print("Generated key (paste this as ENCRYPTION_KEY in your .env):")
    print(Fernet.generate_key().decode())