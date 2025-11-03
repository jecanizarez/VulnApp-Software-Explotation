"""
Main FastAPI application module.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.backend.lib.database import db
from src.backend.views.users import router as users_router
from src.backend.views.auth import router as auth_router
from src.backend.views.recipes import router as recipes_router
import uvicorn

from src.backend.lib.auth import (
    require_admin
)

# Initialize FastAPI app
app = FastAPI(
    title="BakeApp",
    description="Baking Recipe Sharing Platform for Security Testing",
    version="0.1.0"
)

# Add CORS middleware to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(recipes_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to BakeApp", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# Authentication Endpoints
# ============================================================================


@app.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(require_admin)):
    """
    Admin-only endpoint.
    Requires valid JWT token with admin role.

    Returns:
        Admin dashboard data
    """
    return {
        "message": "Welcome to the admin dashboard",
        "admin": current_user.get("username"),
        "role": current_user.get("role")
    }



@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # Create users and recipes tables
    schema = """
             CREATE TABLE IF NOT EXISTS users \
             ( \
                 id \
                 INTEGER \
                 PRIMARY \
                 KEY \
                 AUTOINCREMENT, \
                 username \
                 TEXT \
                 NOT \
                 NULL \
                 UNIQUE, \
                 email \
                 TEXT \
                 NOT \
                 NULL, \
                 password \
                 TEXT \
                 NOT \
                 NULL, \
                 role \
                 TEXT \
                 DEFAULT \
                 'user', \
                 created_at \
                 TIMESTAMP \
                 DEFAULT \
                 CURRENT_TIMESTAMP
             );

             CREATE TABLE IF NOT EXISTS recipes \
             ( \
                 id \
                 INTEGER \
                 PRIMARY \
                 KEY \
                 AUTOINCREMENT, \
                 user_id \
                 INTEGER \
                 NOT \
                 NULL, \
                 title \
                 TEXT \
                 NOT \
                 NULL, \
                 content \
                 TEXT \
                 NOT \
                 NULL, \
                 created_at \
                 TIMESTAMP \
                 DEFAULT \
                 CURRENT_TIMESTAMP, \
                 FOREIGN \
                 KEY \
             ( \
                 user_id \
             ) REFERENCES users \
             ( \
                 id \
             )
                 ); \
             """
    db.init_db(schema_sql=schema)

    # Insert dummy data
    dummy_users = [
        ("admin", "admin@vulnapp.com", "admin123", "admin"),
        ("john_doe", "john@example.com", "password123", "user"),
        ("jane_smith", "jane@example.com", "qwerty456", "user"),
        ("bob_wilson", "bob@example.com", "letmein", "user"),
        ("alice_jones", "alice@example.com", "Pass@123", "user"),
    ]

    for username, email, password, role in dummy_users:
        try:
            db.execute(
                f"INSERT INTO users (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')")
        except:
            pass  # Ignore if user already exists

    # Insert dummy recipes
    dummy_recipes = [
        (1, "Classic Chocolate Cake", "A delicious chocolate cake recipe with rich frosting."),
        (1, "SQL Injection Guide", "Learn how SQL injection works with this example app."),
        (2, "My First Recipe", "Hello everyone! This is my first recipe on this platform."),
        (3, "Healthy Salad Bowl", "A nutritious salad with fresh vegetables and dressing."),
        (4, "Quick Pasta Recipe", "Easy pasta dish that takes only 15 minutes to prepare."),
    ]

    for user_id, title, content in dummy_recipes:
        try:
            db.execute(f"INSERT INTO recipes (user_id, title, content) VALUES ({user_id}, '{title}', '{content}')")
        except:
            pass  # Ignore if recipe already exists

    if db.is_memory:
        print(f"✓ Database initialized in MEMORY (no persistence)")
        print("  Data will be lost when the application restarts")
        print(f"✓ Inserted {len(dummy_users)} dummy users and {len(dummy_recipes)} dummy recipes")
    else:
        print(f"✓ Database initialized at '' (persistent storage)")
        print(f"  Data will persist across restarts")
        print(f"✓ Inserted dummy data (if not exists)")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



