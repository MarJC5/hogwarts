# Hogwarts House Points Management System

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Accessing the Application](#accessing-the-application)
- [Database Management](#database-management-with-adminer)
- [Development Tools](#development-tools)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
- [Additional Documentation](#additional-documentation)

## Project Overview

This project is a web application for Hogwarts teachers to manage house points. It allows teachers to view current points, award or deduct points from houses, and view transaction history.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hogwarts.git
   cd hogwarts
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

3. Start the development environment:
   ```bash
   docker-compose -f dev.docker-compose.yml up -d
   ```

4. Initialize the database:
   ```bash
   make init-db
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - GraphQL API: http://localhost:8000/graphql
   - Adminer: http://localhost:8080

### Stopping the Environment
```bash
docker-compose -f dev.docker-compose.yml down
```

## Key Features

1. **House Points Dashboard**
   - Visual display of current points for all houses
   - House-themed colors and styling

2. **Points Management**
   - Award or deduct points with specific amounts
   - Record reasons for point changes
   - Track which teacher made the changes
   - Optionally attribute points to specific students
   - Support both individual student achievements and house-wide awards

3. **Transaction History**
   - Complete log of all point changes
   - Filter history by house, teacher, points value, or student
   - See timestamp, teacher, reason, and point value

## Development Setup

This project uses Docker Compose for development to ensure a consistent environment across different systems.

### Environment Setup

1. The project uses environment variables for configuration. Copy the example file and adjust as needed:
   ```bash
   cp .env.example .env
   ```

2. Key environment variables:
   - `POSTGRES_USER`: Database username
   - `POSTGRES_PASSWORD`: Database password
   - `POSTGRES_DB`: Database name
   - `DATABASE_URL`: Full connection string for the database

### Running Services

The development environment includes:

- **PostgreSQL**: The database (port 5432)
- **Backend**: FastAPI with GraphQL (port 8000)
- **Frontend**: Next.js development server (port 3000)
- **Adminer**: Database management UI (port 8080)

Use Makefile commands to streamline development tasks:

```bash
# View all available commands
make help

# Start the development environment
make dev-up

# View logs
make logs

# Reset the database
make reset-db
```

## Accessing the Application

Once the development environment is running, you can access various components:

### Frontend Application
- **URL**: [http://localhost:3000](http://localhost:3000)
- **Description**: The main web application for viewing and managing house points

### GraphQL API
- **URL**: [http://localhost:8000/graphql](http://localhost:8000/graphql)
- **Description**: Interactive GraphQL playground for testing queries and mutations

### API Documentation
- **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Description**: OpenAPI/Swagger documentation for REST endpoints

### Database Management (Adminer)
- **URL**: [http://localhost:8080](http://localhost:8080)
- **Login Details**:
  - System: PostgreSQL
  - Server: postgres-hogwarts-dev
  - User: postgres (or your configured POSTGRES_USER)
  - Password: postgres (or your configured POSTGRES_PASSWORD)
  - Database: hogwarts (or your configured POSTGRES_DB)

## Technology Stack

### Frontend
- **React**: Component-based UI library
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Apollo Client**: GraphQL client for React

### Backend
- **Python**: Core programming language
- **Strawberry GraphQL**: Type-first GraphQL library
- **FastAPI**: High-performance web framework
- **SQLAlchemy**: SQL toolkit and ORM

### Database
- **PostgreSQL**: Robust relational database
- **Adminer**: Lightweight database management tool

### Deployment
- **Docker**: Containerization for consistent environments
- **Docker Compose**: Multi-container orchestration

## Why This Stack?

### Strawberry GraphQL
- Type-safe schema definition using Python type hints
- Integration with FastAPI for high performance
- Familiar to your existing projects

### PostgreSQL
- Production-grade database with excellent data integrity
- Transaction support for reliable point management
- Easily scalable if the application grows

### Docker Compose
- One-command setup (`docker-compose up`)
- Consistent environment across different systems
- Easy to extend with additional services if needed

## Demo

*Live demonstration of:*
1. Viewing house points
2. Adding points to a house
3. Deducting points from a house
4. Viewing transaction history
5. Filtering transaction history by house

## Implementation Details (Non-Technical)

The application follows a modern web architecture where:

1. The frontend and backend are separate applications that communicate via API
2. The database stores all house information and point transactions
3. Docker containers package everything together for easy deployment

This approach makes the application:
- Easy to set up
- Easy to maintain
- Easy to extend with new features

## Database Management with Adminer

Adminer is included as part of the project deployment to easily inspect and manage the database.

### Accessing Adminer
- **Development**: Visit [http://localhost:8080](http://localhost:8080) when running the development environment
- **Production**: Adminer is disabled by default for security. Enable it when needed with:
  ```
  docker-compose -f prod.docker-compose.yml --profile admin up -d adminer-hogwarts-prod
  ```

### Login Details
- **System**: PostgreSQL
- **Server**: postgres-hogwarts-dev (development) or postgres-hogwarts-prod (production)
- **Username**: Use the value from your environment variables (POSTGRES_USER)
- **Password**: Use the value from your environment variables (POSTGRES_PASSWORD)
- **Database**: Use the value from your environment variables (POSTGRES_DB)

### What You Can Do With Adminer
- View the database schema
- Execute SQL queries
- Import and export data
- Manage tables, views, and relationships
- Monitor database performance

### Security Note
For production environments, it's recommended to:
1. Use strong, unique passwords
2. Only enable Adminer when needed
3. Configure a firewall to restrict access to the Adminer port

## Development Tools

The project includes several tools to make development easier:

### Makefile Commands

Run `make help` to see all available commands. Some useful ones include:

- `make dev-up`: Start the development environment
- `make dev-down`: Stop the development environment
- `make logs`: Show logs for all containers
- `make backend-shell`: Open a shell in the backend container
- `make fix-db-config`: Fix database configuration in .env file
- `make reset-db`: Reset the database and reinitialize with test data
- `make adminer`: Open Adminer in the default browser
- `make init-db`: Initialize database with test data
- `make migrate`: Run database migrations
- `make backup-db`: Backup the database

### Adminer Database Management

Adminer is included for easy database administration:

- Access at http://localhost:8080 when running the development environment
- Visually explore and edit database tables
- Execute SQL queries
- Import and export data

### Scripts

- `setup.sh`: Quick setup script for new developers
- `restart.sh`: Restart the application with a clean database

## Common Issues and Troubleshooting

### Database Connection Issues
If you encounter database connection errors like "could not translate host name to address", check:

1. The hostname in your `DATABASE_URL` environment variable matches exactly with the service name in your docker-compose file
2. All services are running with `docker-compose ps`
3. Your .env file has the correct configuration

Example of correct configuration:
```
# In .env file
DATABASE_URL=postgresql://postgres:postgres@postgres-hogwarts-dev:5432/hogwarts

# In docker-compose.yml
services:
  postgres-hogwarts-dev:  # This service name must match the hostname in DATABASE_URL
    image: postgres:14
    # ...
```

### Docker Networking and Container Communication

When working with Docker containers:

1. **Service-to-service communication**: Always use the service name defined in docker-compose.yml as the hostname:
   ```
   # Correct (for backend container connecting to database container)
   DATABASE_URL=postgresql://postgres:postgres@postgres-hogwarts-dev:5432/hogwarts
   ```

2. **Host-to-container communication**: Use localhost with the exposed port:
   ```
   # Correct (for connecting to database from your local machine)
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hogwarts
   ```

3. **Never use localhost for container-to-container communication**:
   ```
   # INCORRECT (will not work for container-to-container)
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hogwarts
   ```

This is because each container has its own network namespace, and "localhost" inside a container refers to the container itself, not the host machine or other containers.

### Accessing the Database
You can access the PostgreSQL database in several ways:
1. Using Adminer web interface at http://localhost:8080
2. Direct connection to PostgreSQL on port 5432 (using localhost from your machine)
3. Through your application's ORM tools and migrations

## Additional Documentation

For more detailed information about specific aspects of the project, refer to these additional documentation files:

- [Backend Documentation](backend/README.md) - Backend structure, API endpoints, and database models
- [Frontend Documentation](frontend/README.md) - Frontend components, Apollo client setup, and example code
- [Detailed Setup Guide](doc/SETUP.md) - Advanced setup instructions and development workflow
- [Comprehensive Documentation](doc/DOCUMENTATION.md) - Complete system documentation including architecture, schema, and deployment
- [Coding Challenge](doc/CODING-CHALLENGE.md) - Original coding challenge requirements and objectives