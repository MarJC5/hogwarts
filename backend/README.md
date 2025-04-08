# Hogwarts Backend

This is the backend for the Hogwarts House Points System, built with FastAPI, SQLAlchemy, and Strawberry GraphQL.

## Overview

The backend provides a GraphQL API for managing the Hogwarts house points system, including:
- Managing wizards (students) and teachers
- Awarding and deducting house points
- Viewing point transactions and analytics
- Calculating house cup standings

For general project setup, please refer to the main [README.md](../README.md) in the project root.

## Directory Structure

```
backend/
├── app/                    # Main application package
│   ├── api/                # API layer
│   │   ├── __init__.py     
│   │   └── schema.py       # GraphQL schema and resolvers
│   ├── database/           # Database layer
│   │   ├── __init__.py     
│   │   └── db.py           # Database connection and session management
│   ├── models/             # Data models
│   │   ├── __init__.py     
│   │   └── models.py       # SQLAlchemy models
│   ├── utils/              # Utility functions
│   │   ├── __init__.py     
│   │   └── helpers.py      # Helper functions
│   ├── __init__.py         
│   └── main.py             # FastAPI application entry point
├── migrations/             # Alembic database migrations
│   ├── versions/           # Migration versions
│   │   ├── __init__.py     
│   │   └── initial_migration.py  # Initial database schema
│   ├── __init__.py         
│   ├── env.py              # Alembic environment
│   └── script.py.mako      # Alembic script template
├── Dockerfile.dev          # Development Docker configuration
├── Dockerfile.prod         # Production Docker configuration
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Python dependencies
├── run.py                  # Application runner script
└── README.md               # This file
```

## Backend-Specific Setup

If you prefer to run the backend directly without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server using the run.py script:
   ```bash
   # Basic usage
   python run.py
   
   # With custom options
   python run.py --host 127.0.0.1 --port 8080 --reload --env dev
   ```

3. Or run directly with Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## GraphQL API

The GraphQL API is exposed at `/graphql` and includes:

- **Queries**:
  - `wizards`: List all wizards
  - `wizard(id)`: Get a specific wizard
  - `teachers`: List all teachers
  - `teacher(id)`: Get a specific teacher
  - `house_points(house)`: Get house points, optionally filtered by house
  - `house_totals`: Get current house cup standings
  - `points_history`: Get detailed history of point changes
  - `points_history_grouped`: Get aggregated analytics on points

- **Mutations**:
  - `create_wizard`: Add a new wizard
  - `create_teacher`: Add a new teacher
  - `award_house_points`: Award points to a house
  - `deduct_house_points`: Deduct points from a house

## GraphQL Explorer

When running the application, you can access the GraphQL Explorer UI at:
`http://localhost:8000/graphql`

This provides an interactive environment to explore and test the API.

## Database Migrations

Alembic is used for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Run migrations
alembic upgrade head
``` 