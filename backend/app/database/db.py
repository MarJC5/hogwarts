from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Check if running in Docker (environment variable set in Docker Compose)
IN_DOCKER = os.getenv("IN_DOCKER", "false").lower() == "true"

# Use PostgreSQL when in Docker, SQLite when running locally
if IN_DOCKER:
    # When running in Docker, use the service name from docker-compose.yml as the hostname
    # This is essential for container-to-container communication
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres-hogwarts-dev:5432/hogwarts")
else:
    # Use SQLite for local development without Docker
    DATABASE_URL = "sqlite:///./hogwarts_local.db"
    
    # If you want to use PostgreSQL locally (outside Docker), you would use:
    # DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hogwarts"

# For SQLite, we need to add this parameter
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 