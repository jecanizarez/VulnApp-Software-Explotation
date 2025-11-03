from fastapi import APIRouter, Body, Depends
from starlette.responses import JSONResponse

from src.backend.lib.auth import authenticate_user, create_user_token, get_current_user
from src.backend.lib.database import db

router = APIRouter()


@router.post("/login")
async def login(username: str = Body("username"), password: str = Body("password")):
    """
    Login endpoint - authenticate user and return JWT token.

    Args:
        username: Username (form field)
        password: Password (form field)

    Returns:
        JSON with access_token and user information
    """
    try:
        user = authenticate_user(db, username, password)

        if not user:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid username or password"}
            )

        # Create JWT token
        access_token = create_user_token(user)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.get("id"),
                "username": user.get("username"),
                "email": user.get("email"),
                "role": user.get("role", "user")
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    Requires valid JWT token in Authorization header.

    Returns:
        User information from JWT token
    """
    return {
        "user": current_user
    }
