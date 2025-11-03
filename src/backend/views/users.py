from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.backend.lib.database import rows_to_dict_list, row_to_dict, db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users():
    """Get all users."""
    try:
        rows = db.fetch_all("SELECT id, username, email, created_at FROM users")
        users = rows_to_dict_list(rows)
        return {"users": users}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.post("/")
async def create_user(username: str, email: str, password: str):
    """Create a new user."""
    try:
        query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        db.execute(query)
        return {"message": "User created successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get a specific user by ID."""
    try:
        row = db.fetch_all(
            f"SELECT id, username, email, created_at FROM users WHERE id = {user_id}"
        )
        if row:
            user = rows_to_dict_list(row)
            return {"user": user}
        return JSONResponse(
            status_code=404,
            content={"error": "User not found"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
