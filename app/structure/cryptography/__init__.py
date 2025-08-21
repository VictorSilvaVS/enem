import bcrypt
from jose import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Use environment variable in production

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(user_id: int) -> str:
    """Create a JWT token for user authentication."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None
