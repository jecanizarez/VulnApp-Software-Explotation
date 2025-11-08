"""
Example usage of the database module.
This file demonstrates various ways to use the database.py utilities.
"""
from src.backend.lib.database import Database, row_to_dict


def main():
    """Main function to demonstrate database usage."""
    print("=" * 60)
    print("VulnApp Database Example")
    print("=" * 60)

    # Create users and recipes tables
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """

    # Initialize database (in-memory by default)
    db = Database()
    db.init_db(schema_sql=schema)
    print("✓ Database schema initialized")

    # Insert dummy users
    dummy_users = [
        ("admin", "admin@vulnapp.com", "admin123", "admin"),
        ("john_doe", "john@example.com", "password123", "user"),
        ("jane_smith", "jane@example.com", "qwerty456", "user"),
        ("bob_wilson", "bob@example.com", "letmein", "user"),
        ("alice_jones", "alice@example.com", "Pass@123", "user"),
    ]

    for username, email, password, role in dummy_users:
        try:
            db.execute(f"INSERT INTO users (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')")
        except:
            pass  # Ignore if user already exists

    print(f"✓ Inserted {len(dummy_users)} users")

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

    print(f"✓ Inserted {len(dummy_recipes)} recipes")

    # Query all users and display results
    print("\n=== All Users ===")
    users = db.fetch_all("SELECT id, username, email FROM users")
    for user in users:
        user_dict = row_to_dict(user)
        print(f"  [{user_dict['id']}] {user_dict['username']} - {user_dict['email']}")

    # Query all recipes and display results
    print("\n=== All Recipes ===")
    recipes = db.fetch_all("SELECT recipes.id, users.username, recipes.title FROM recipes JOIN users ON recipes.user_id = users.id")
    for recipe in recipes:
        recipe_dict = row_to_dict(recipe)
        print(f"  [{recipe_dict['id']}] {recipe_dict['title']} by {recipe_dict['username']}")

    # Demonstrate SQL injection vulnerability
    print("\n=== SQL Injection Demonstration ===")
    print("Normal query: SELECT * FROM users WHERE id = 1")
    user = db.fetch_one("SELECT * FROM users WHERE id = 1")
    if user:
        user_dict = row_to_dict(user)
        print(f"  Result: {user_dict['username']}")

    id = "1 OR 1=1"  # Malicious input
    print(f"\nInjected query: SELECT * FROM users WHERE {id}")
    users_injected = db.fetch_all(f"SELECT * FROM users WHERE {id}")
    print(f"  Result: Retrieved {len(users_injected)} users (all of them!)")

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  - Database type: {'In-Memory' if db.is_memory else 'File-based'}")
    print(f"  - Total users: {len(dummy_users)}")
    print(f"  - Total recipes: {len(dummy_recipes)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

