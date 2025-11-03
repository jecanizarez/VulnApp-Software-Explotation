"""
Database module for SQLite3 operations.
Provides connection management and utility functions for database operations.
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any


class Database:
    """SQLite3 Database manager class."""

    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file (default: ":memory:" for in-memory database)
        """
        self.db_path = db_path
        self.is_memory = db_path == ":memory:"
        self._conn = None  # Persistent connection for in-memory databases
        if not self.is_memory:
            self._ensure_db_directory()

    def _ensure_db_directory(self):
        """Ensure the directory for the database file exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection.

        Returns:
            sqlite3.Connection: Database connection object
        """
        # For in-memory databases, maintain a persistent connection
        if self.is_memory:
            if self._conn is None:
                self._conn = sqlite3.connect(self.db_path)
                self._conn.row_factory = sqlite3.Row
            return self._conn

        # For file-based databases, create a new connection each time
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    @contextmanager
    def connection(self):
        """
        Context manager for database connections.
        Automatically commits and closes the connection.

        Usage:
            with db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
        """
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            # Only close file-based database connections
            # Keep in-memory connections open
            if not self.is_memory:
                conn.close()

    def execute(self, query: str) -> sqlite3.Cursor:
        """
        Execute a single query and return the cursor.

        Args:
            query: SQL query to execute

        Returns:
            sqlite3.Cursor: Cursor object with results
        """
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """
        Execute a query multiple times with different parameters.

        Args:
            query: SQL query to execute
            params_list: List of parameter tuples
        """
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)

    def fetch_one(self, query: str) -> Optional[sqlite3.Row]:
        """
        Fetch a single row from the database.

        Args:
            query: SQL query to execute

        Returns:
            sqlite3.Row or None: Single row result or None if not found
        """
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchone()

    def fetch_all(self, query: str) -> List[sqlite3.Row]:
        """
        Fetch all rows from the database.

        Args:
            query: SQL query to execute

        Returns:
            List[sqlite3.Row]: List of row results
        """
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def init_db(self, schema_file: Optional[str] = None, schema_sql: Optional[str] = None):
        """
        Initialize the database with a schema.

        Args:
            schema_file: Path to SQL file with schema
            schema_sql: SQL string with schema (used if schema_file is None)
        """
        if schema_file:
            with open(schema_file, 'r') as f:
                schema_sql = f.read()

        if schema_sql:
            with self.connection() as conn:
                cursor = conn.cursor()
                cursor.executescript(schema_sql)

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name: Name of the table to check

        Returns:
            bool: True if table exists, False otherwise
        """
        query = f"""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='{table_name}'
        """
        result = self.fetch_one(query)
        return result is not None

    def drop_table(self, table_name: str):
        """
        Drop a table from the database.

        Args:
            table_name: Name of the table to drop
        """
        with self.connection() as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")

    def reset_database(self):
        """Remove the database file to start fresh (only for file-based databases)."""
        if not self.is_memory and os.path.exists(self.db_path):
            os.remove(self.db_path)


def get_db() -> Database:
    """
    Get the global database instance.

    Returns:
        Database: Global database instance
    """
    return db


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Convert a sqlite3.Row to a dictionary.

    Args:
        row: sqlite3.Row object

    Returns:
        Dict: Dictionary representation of the row
    """
    if row is None:
        return {}
    return dict(row)


def rows_to_dict_list(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """
    Convert a list of sqlite3.Row objects to a list of dictionaries.

    Args:
        rows: List of sqlite3.Row objects

    Returns:
        List[Dict]: List of dictionary representations
    """
    return [dict(row) for row in rows]


# Get database path from environment or use in-memory database by default
db_path = os.getenv("DATABASE_PATH", ":memory:")
db = Database(db_path)
