"""
Simple example: Insert a user and their recipe
"""

from src.backend.lib.database import Database, row_to_dict


def insert_user_and_recipe():
    """Insert a new user and their recipe into the database."""

    # Initialize database with schema
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

    db = Database()
    db.init_db(schema_sql=schema)
    print("✓ Database initialized\n")

    # Step 1: Insert a new user
    print("=== Inserting User ===")
    username = "chef_mike"
    email = "mike@example.com"
    password = "cooking123"

    db.execute(
        f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
    )
    print(f"✓ User '{username}' inserted")

    # Step 2: Get the user ID of the newly inserted user
    user = db.fetch_one(f"SELECT id, username FROM users WHERE username = '{username}'")
    user_dict = row_to_dict(user)
    user_id = user_dict['id']
    print(f"✓ User ID: {user_id}\n")

    # Step 3: Insert a recipe for this user
    print("=== Inserting Recipe ===")
    recipe_title = "Perfect Pancakes"
    recipe_content = "Mix flour, eggs, and milk. Cook on griddle until golden brown. Serve with maple syrup."

    db.execute(
        f"INSERT INTO recipes (user_id, title, content) VALUES ({user_id}, '{recipe_title}', '{recipe_content}')"
    )
    print(f"✓ Recipe '{recipe_title}' inserted\n")

    # Step 4: Verify the data was inserted correctly
    print("=== Verification ===")
    recipe = db.fetch_one(
        f"SELECT recipes.id, recipes.title, recipes.content, users.username "
        f"FROM recipes JOIN users ON recipes.user_id = users.id "
        f"WHERE recipes.user_id = {user_id}"
    )

    if recipe:
        recipe_dict = row_to_dict(recipe)
        print(f"Recipe ID: {recipe_dict['id']}")
        print(f"Title: {recipe_dict['title']}")
        print(f"Author: {recipe_dict['username']}")
        print(f"Content: {recipe_dict['content']}")

    print("\n" + "=" * 60)
    print("✅ User and recipe successfully inserted!")
    print("=" * 60)


if __name__ == "__main__":
    insert_user_and_recipe()

