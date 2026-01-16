"""Database connection helper."""
import os


def get_postgres_connection_string() -> str:
    """Get PostgreSQL connection string from environment variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "gtvision")
    user = os.getenv("DB_USER", "gtvision")
    password = os.getenv("DB_PASSWORD", "gtvision_password")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"
