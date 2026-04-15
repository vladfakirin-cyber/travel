"""
auth.py - Авторизация и аутентификация
"""

import hashlib
import secrets

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_session_token(username: str) -> str:
    return secrets.token_urlsafe(32)

def get_current_user(session_token: str = None):
    if session_token and session_token in SESSIONS:
        return SESSIONS[session_token]
    return None

def remove_session(session_token: str):
    if session_token in SESSIONS:
        del SESSIONS[session_token]

# Глобальное хранилище сессий
SESSIONS = {}