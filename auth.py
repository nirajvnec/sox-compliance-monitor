"""Simple Authentication - Login with username/password and get access token."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import hashlib
import secrets

auth_router = APIRouter()

# ==================== Sample Users (In real app, use a database) ====================

USERS = {
    "admin": {
        "username": "admin",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
    },
    "viewer": {
        "username": "viewer",
        "password_hash": hashlib.sha256("viewer123".encode()).hexdigest(),
        "role": "viewer",
    },
}

# ==================== Token Storage (In real app, use Redis or database) ====================

active_tokens = {}

# This tells Swagger UI to show a lock icon and login form
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==================== Helper Functions ====================

def verify_password(username: str, password: str) -> bool:
    """Check if username and password are correct."""
    if username not in USERS:
        return False
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return USERS[username]["password_hash"] == password_hash


def create_token(username: str) -> str:
    """Create a simple access token."""
    token = secrets.token_hex(32)
    active_tokens[token] = {
        "username": username,
        "role": USERS[username]["role"],
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
    }
    return token


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Validate token and return current user. Used as a dependency."""
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_data = active_tokens[token]

    # Check if token has expired
    expires_at = datetime.fromisoformat(user_data["expires_at"])
    if datetime.now() > expires_at:
        del active_tokens[token]
        raise HTTPException(status_code=401, detail="Token has expired")

    return user_data


# ==================== Auth Routes ====================

@auth_router.post("/auth/login", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username and password to get an access token.

    Sample accounts:
    - admin / admin123
    - viewer / viewer123
    """
    if not verify_password(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": form_data.username,
        "role": USERS[form_data.username]["role"],
        "message": "Login successful!",
    }


@auth_router.get("/auth/me", tags=["Authentication"])
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current logged-in user details. Requires authentication."""
    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "token_created": current_user["created_at"],
        "token_expires": current_user["expires_at"],
    }
