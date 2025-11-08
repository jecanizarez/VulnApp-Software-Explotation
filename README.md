# BakeApp - Baking Recipe Platform

A baking recipe sharing web application built with FastAPI and SQLite3 for security testing and exploitation learning.

## 🚀 Quick Start

```bash
# Using Docker (recommended)
docker-compose up --build

# Access the Backend Documentation
open http://localhost:8000/docs

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
│   └── frontend/
│       ├── css/              # CSS stylesheets
│       ├── js/               # JavaScript files
│       └── index.html       # Main HTML file
│   └── backend/
│       ├── main.py              # Main FastAPI application
│       ├── lib/
│       │   └── database.py      # SQLite3 database utilities
│       ├── controllers/         # API route controllers
│       ├── models/              # Data models
│       └── views/               # Response views
├── docker-compose.yml           # Docker compose configuration
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── examples.py                  # Example usage of the database module
└── README.md                   # This file
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

### Users
- `GET /users` - Get all users (returns id, username, email, created_at)
   ```bash
  - Parameters: `username`, `email`, `password`
   docker-compose down

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

### Login Credentials for Testing
You can use these credentials to test authentication exploits:
- `admin / admin123`
- `john_doe / password123`
- `jane_smith / qwerty456`
- `bob_wilson / letmein`
- `alice_jones / Pass@123`

### Sample SQL Injection Tests

**Extract all users:**
```bash
curl "http://localhost:8000/users/1%20OR%201=1--"
```

**Union-based injection (if you add more vulnerable endpoints):**
```sql
1 UNION SELECT username, password, email FROM users--
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
