import os

import psycopg2
from psycopg2.extras import DictCursor

# PostgreSQL client configuration
postgres_client = psycopg2.connect(
    dsn=os.getenv("DATABASE_URL", "postgres://nsfw:nsfw@localhost:5433/nsfw"),
    cursor_factory=DictCursor
)
postgres_client.autocommit = True

def get_db():
    """Get database connection"""
    return postgres_client

def get_cursor():
    """Get database cursor"""
    return postgres_client.cursor()
