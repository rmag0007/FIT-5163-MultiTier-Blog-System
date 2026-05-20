import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()

# Run this once to generate a key, paste it in .env
if __name__ == "__main__":
    print(Fernet.generate_key().decode())