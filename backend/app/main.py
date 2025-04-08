from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.api.schema import schema
from app.database.db import engine, Base
from app.routes.house_points import router as house_points_router
import app.models.models
import platform
import time
import os
from datetime import datetime
import logging
from app.database.init_db import init_test_data
from app.database.db import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize database with test data
try:
    db = next(get_db())
    init_test_data(db)
    db.close()
    logger.info("Database initialization completed during startup")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

# API metadata
API_VERSION = "1.0.0"
API_TITLE = "Hogwarts House Points API"
API_DESCRIPTION = """
# Hogwarts House Points System API

This API provides access to the Hogwarts House Points System, allowing users to:
- View and manage house points
- Track students and their assigned houses
- Record point additions and deductions
- Generate reports on house standings

## API Endpoints

- **/graphql**: GraphQL API for complex queries and mutations
- **/api/house-points**: REST API for house points
- **/docs**: Swagger UI documentation (this page)
- **/redoc**: ReDoc alternative documentation
- **/health**: Health check endpoint

## Authentication

Some endpoints may require authentication. Please refer to the specific endpoint documentation.
"""
START_TIME = time.time()

# Create FastAPI app with additional metadata
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "General",
            "description": "General endpoints providing API information",
        },
        {
            "name": "Monitoring",
            "description": "Endpoints for monitoring the API health and status",
        },
        {
            "name": "GraphQL",
            "description": "GraphQL interface for complex queries and mutations",
        },
        {
            "name": "House Points",
            "description": "REST API endpoints for managing house points",
        },
    ],
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section by default
        "deepLinking": True,             # Enable deep linking for better navigation
        "displayRequestDuration": True,  # Show request duration
        "filter": True,                  # Enable filtering operations
        "showExtensions": True,          # Show schema extensions
        "showCommonExtensions": True,    # Show schema common extensions
        "syntaxHighlight.theme": "monokai"  # Code highlighting theme
    }
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Include the house points router
app.include_router(house_points_router)

@app.get("/", tags=["General"], summary="API Root", 
         description="Returns basic information about the API")
def read_root():
    """
    Root endpoint that returns basic API information
    
    Returns:
        dict: A dictionary containing API metadata and documentation links
    """
    # Create a simplified description without newlines for the response
    simplified_description = (
        "Hogwarts House Points System API - Manage house points, track students, "
        "record points, and generate house standings reports."
    )
    
    return {
        "message": "Welcome to Hogwarts API",
        "version": API_VERSION,
        "title": API_TITLE,
        "description": simplified_description,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "graphql": "/graphql",
        },
        "endpoints": [
            {"path": "/graphql", "description": "GraphQL API for complex queries and mutations"},
            {"path": "/api/house-points", "description": "REST API for house points"},
            {"path": "/docs", "description": "Swagger UI documentation"},
            {"path": "/redoc", "description": "ReDoc alternative documentation"},
            {"path": "/health", "description": "Health check endpoint"}
        ]
    }

@app.get("/health", tags=["Monitoring"], summary="Health Check", 
         description="Check the health status of the API")
def health_check():
    """
    Health check endpoint for monitoring and status verification
    
    Returns:
        dict: Health status information including uptime and system details
    """
    # Calculate uptime
    uptime_seconds = time.time() - START_TIME
    
    # Environment info
    environment = os.getenv("APP_ENV", "development")
    in_docker = os.getenv("IN_DOCKER", "false").lower() == "true"
    
    return {
        "status": "healthy",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": uptime_seconds,
        "environment": environment,
        "system_info": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "in_docker": in_docker,
        },
    } 