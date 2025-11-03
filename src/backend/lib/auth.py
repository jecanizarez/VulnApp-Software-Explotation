"""
Authentication module with JWT support.
"""
import jwt
from src.backend.lib.database import row_to_dict

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "super_secret_key_no_salt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Security scheme
security = HTTPBearer()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing user data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token string

    Returns:
        Dict: Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Get the current authenticated user from the JWT token.

    Args:
        credentials: HTTP Bearer credentials containing the JWT token

    Returns:
        Dict: User information from the token

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload.get("user_id"):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return payload


def require_role(required_role: str):
    """
    Decorator to require a specific role for accessing an endpoint.

    Args:
        required_role: Role required to access the endpoint (e.g., 'admin', 'user')

    Returns:
        Function that checks if the user has the required role
    """
    def role_checker(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
        user = get_current_user(credentials)

        if user.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {required_role}"
            )

        return user

    return role_checker


def require_admin(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Require admin role for accessing an endpoint.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Dict: User information if user is admin

    Raises:
        HTTPException: If user is not admin
    """
    user = get_current_user(credentials)

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    WARNING: This is intentionally insecure - passwords are stored in plain text!

    Args:
        plain_password: Password to verify
        hashed_password: Stored password (actually plain text in this vulnerable app)

    Returns:
        bool: True if passwords match
    """
    # Intentionally vulnerable: direct comparison, no hashing
    return plain_password == hashed_password


def authenticate_user(db, username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user by username and password.
    WARNING: This uses SQL injection vulnerable queries!

    Args:
        db: Database instance
        username: Username to authenticate
        password: Password to verify

    Returns:
        Dict: User information if authentication succeeds, None otherwise
    """
    # Intentionally vulnerable SQL query (no parameterization)
    query = f"SELECT id, username, email, password, role FROM users WHERE username = '{username}'"
    user = db.fetch_one(query)

    if not user:
        return None

    user_dict = row_to_dict(user)

    # Verify password (plain text comparison - intentionally insecure)
    if not verify_password(password, user_dict.get("password", "")):
        return None

    # Remove password from returned data
    user_dict.pop("password", None)
    return user_dict


def create_user_token(user: Dict[str, Any]) -> str:
    """
    Create a JWT token for a user.

    Args:
        user: User dictionary containing id, username, and role

    Returns:
        str: JWT access token
    """
    token_data = {
        "user_id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role", "user")
    }

    access_token = create_access_token(data=token_data)
    return access_token

