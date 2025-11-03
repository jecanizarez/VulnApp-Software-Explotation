# BakeApp - Baking Recipe Platform

A baking recipe sharing web application built with FastAPI and SQLite3 for security testing and exploitation learning.

## 🚀 Quick Start

```bash
# Using Docker (recommended)
docker-compose up --build

# Access the application
open http://localhost:8000/docs

# View all users with dummy data
curl http://localhost:8000/users
```

The application automatically loads with dummy data including 5 users and 5 posts, ready for security testing!

## Features

- FastAPI web framework
- **In-memory SQLite3 database** (no persistence between restarts - perfect for testing)
- RESTful API endpoints
- Docker support for easy deployment
- Optional file-based persistent storage

## Project Structure

```
BakeApp/
├── src/
│   └── backend/
│       ├── main.py              # Main FastAPI application
│       ├── lib/
│       │   └── database.py      # SQLite3 database utilities
│       ├── controllers/         # API route controllers
│       ├── models/              # Data models
│       └── views/               # Response views
├── data/                        # Database storage (created at runtime)
├── docker-compose.yml           # Docker compose configuration
├── Dockerfile                   # Docker image definition
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```


user = db.fetch_one(f"SELECT * FROM users WHERE username = '{username}'")

## Database Module (`database.py`)

The database module provides a comprehensive SQLite3 wrapper with **in-memory database by default**.

# Use context manager for transactions
- **In-Memory Database**: Data stored in RAM by default (resets on restart)
- **Connection Management**: Context managers for automatic commit/rollback
- **Query Helpers**: Methods for common operations (fetch_one, fetch_all, execute)
- **Schema Initialization**: Load schema from SQL files or strings
- **Row Factory**: Automatic conversion to dictionaries for easy JSON serialization
- **Utility Functions**: Table existence checks, table dropping, database reset
- **Optional Persistence**: Can be configured to use file-based storage

### Usage Examples

```python
from src.backend.lib.database import Database, get_db, row_to_dict

# Get the global in-memory database instance
db = get_db()

# Or create a file-based database
db_file = Database("app.db")

# Initialize with schema
schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL
);
"""
db.init_db(schema_sql=schema)

# Insert data
db.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("john", "john@example.com"))

# Fetch single row
user = db.fetch_one("SELECT * FROM users WHERE username = ?", ("john",))
print(row_to_dict(user))

# Fetch all rows
all_users = db.fetch_all("SELECT * FROM users")

# Use context manager
with db.connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

## Quick Start

### Using Docker (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
### General
- `GET /` - Root endpoint, returns welcome message
- `GET /health` - Health check endpoint, returns database status

### Users
- `GET /users` - Get all users (returns id, username, email, created_at)
   ```bash
  - Parameters: `username`, `email`, `password`
  - ⚠️ Vulnerable to SQL injection
   docker-compose down
  - ⚠️ Vulnerable to SQL injection

### Example Requests

**Get all users:**
```bash
curl http://localhost:8000/users
```

**Create a user:**
```bash
curl -X POST "http://localhost:8000/users?username=testuser&email=test@example.com&password=test123"
```

**Get specific user:**
```bash
curl http://localhost:8000/users/1
```

**SQL Injection Example (Educational Purpose):**
```bash
# Extract all data from users table
curl "http://localhost:8000/users/1%20OR%201=1"

# This becomes: SELECT ... WHERE id = 1 OR 1=1
```

## Testing with Dummy Data

The application comes preloaded with dummy data for immediate testing:

### Login Credentials for Testing
You can use these credentials to test authentication exploits:
- `admin / admin123`
- `john_doe / password123`
- `jane_smith / qwerty456`
- `bob_wilson / letmein`
- `alice_jones / Pass@123`

### Sample SQL Injection Tests

**Basic injection to bypass authentication:**
```bash
# Username: admin' OR '1'='1
# This would bypass login if authentication were implemented
```

**Extract all users:**
```bash
curl "http://localhost:8000/users/1%20OR%201=1--"
```

**Union-based injection (if you add more vulnerable endpoints):**
```sql
1 UNION SELECT username, password, email FROM users--
```

### Running the Examples

Test the database functionality:
```bash
python examples.py
```

This will demonstrate:
- Database initialization with schema
- Dummy data insertion
- Query operations
- SQL injection vulnerabilities
   ```

### Enable Persistent File-Based Database

To use a persistent database instead of in-memory:

1. **Edit `docker-compose.yml`** and uncomment the lines:
   ```yaml
   volumes:
     - ./data:/data
   environment:
     - DATABASE_PATH=/data/app.db
   ```

2. **Restart the application:**
   ```bash
   docker-compose down && docker-compose up --build
   ```

⚠️ **WARNING**: This application contains INTENTIONAL security vulnerabilities for educational purposes.

### Known Vulnerabilities:
1. **SQL Injection**: All database queries use string concatenation instead of parameterized queries
2. **Plain Text Passwords**: User passwords are stored in plain text
3. **No Input Validation**: User inputs are not sanitized or validated
4. **No Authentication**: No authentication or authorization mechanisms
5. **No Rate Limiting**: No protection against brute force attacks

### Usage Guidelines:
- ✅ Use ONLY in isolated, controlled environments
- ✅ Use for learning security testing and exploitation techniques
- ✅ Use for practicing SQL injection attacks safely
- ❌ Do NOT deploy in production
- ❌ Do NOT expose to the internet
- ❌ Do NOT use with real user data

## Learning Objectives

This application is designed to help you:
- Understand how SQL injection vulnerabilities work
- Practice identifying security flaws in web applications
- Learn proper mitigation techniques by seeing what NOT to do
- Test security tools and scanning techniques in a safe environment

1. **Install dependencies:**
   ```bash
   pip install poetry
   poetry install
   ```

2. **Run the application:**
   ```bash
   uvicorn src.backend.main:app --reload
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /users` - Get all users
- `POST /users` - Create a new user
- `GET /users/{user_id}` - Get user by ID

## Environment Variables

- `DATABASE_PATH` - Path to SQLite database file (default: `:memory:` for in-memory database)
  - Use `:memory:` for in-memory database (no persistence)
  - Use a file path like `/data/app.db` for persistent storage
- `PYTHONUNBUFFERED` - Enable Python output buffering (default: `1`)

## Security Notes

⚠️ **Warning**: This is a vulnerable application designed for educational purposes. Do NOT deploy this in production or expose it to the internet.

## License

Educational use only.


