# Hogwarts House Points System - Documentation

This document provides comprehensive documentation for the Hogwarts House Points System. For quick setup instructions, please refer to the [Getting Started](../README.md#getting-started) section in the main README.

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Database Schema](#database-schema)
4. [API Endpoints](#api-endpoints)
5. [Development Setup](#development-setup)
6. [Production Deployment](#production-deployment)
7. [Common Tasks](#common-tasks)
8. [Troubleshooting](#troubleshooting)

## Introduction

The Hogwarts House Points System is a web application designed to track and manage house points at Hogwarts School of Witchcraft and Wizardry. It allows teachers to award or deduct points from houses, with the ability to attribute points to specific students or to entire houses.

### Key Features

* **House Points Dashboard**: Visual representation of current house standings
* **Points Management**: Award or deduct points with reasons and teacher attribution
* **Student Attribution**: Points can be awarded to specific students or entire houses
* **Transaction History**: Complete log of all point changes with filtering options
* **API Access**: Both REST and GraphQL APIs for integration options

## System Architecture

The application follows a modern microservices architecture with separate frontend and backend components:

### Frontend

* **Technology**: React with TypeScript
* **State Management**: Apollo Client for GraphQL data fetching
* **Styling**: Tailwind CSS for responsive design
* **Features**: 
  * Interactive house points dashboard
  * Point award/deduction forms
  * Transaction history with filtering
  * Student directory

### Backend

* **Technology**: Python with FastAPI
* **API**: Dual REST and GraphQL (Strawberry) endpoints
* **ORM**: SQLAlchemy for database interactions
* **Migration**: Alembic for database schema migrations
* **Features**:
  * House points management endpoints
  * User authentication and authorization
  * Data validation with Pydantic
  * Comprehensive API documentation with Swagger/OpenAPI

### Database

* **Technology**: PostgreSQL
* **Management**: Adminer for database visualization and management
* **Schema**: Relational database with tables for houses, students, teachers, and point transactions

### Deployment

* **Containerization**: Docker for consistent environments
* **Orchestration**: Docker Compose for multi-container management
* **Development/Production**: Separate configurations for development and production environments

## Database Schema

The database consists of four main tables:

### Wizards (Students)

```sql
CREATE TABLE wizards (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    house ENUM('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin') NOT NULL,
    wand VARCHAR NOT NULL,
    patronus VARCHAR
);
```

### Teachers

```sql
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    house ENUM('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin')
);
```

### House Points

```sql
CREATE TABLE house_points (
    id SERIAL PRIMARY KEY,
    house ENUM('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin') NOT NULL,
    points INTEGER NOT NULL,
    reason VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id),
    wizard_id INTEGER REFERENCES wizards(id)
);
```

### Entity Relationships

* **House Points to Teachers**: Many-to-one relationship (each point transaction is associated with one teacher)
* **House Points to Wizards**: Many-to-one relationship (points can be associated with one student or NULL for house-wide points)
* **Teachers to Houses**: Many-to-one relationship (teachers can be associated with a house as Head of House)
* **Wizards to Houses**: Many-to-one relationship (each student belongs to one house)

## API Endpoints

### REST API

#### House Points Endpoints

* `GET /api/house-points/`: Get all house point transactions with filtering options
  * Query Parameters:
    * `house`: Filter by house name
    * `min_points`: Filter by minimum points value
    * `awarded_by`: Filter by teacher name
    * `student`: Filter by student name

* `GET /api/house-points/{transaction_id}`: Get a specific point transaction

* `POST /api/house-points/`: Create a new point transaction
  * Request Body:
    ```json
    {
      "house": "Gryffindor",
      "points": 10,
      "reason": "Excellent work in Transfiguration class",
      "awarded_by": "Minerva McGonagall",
      "student_name": "Harry Potter"  // Optional - NULL for house-wide points
    }
    ```

* `GET /api/house-points/standings`: Get current house standings

### GraphQL API

GraphQL endpoint: `/graphql`

#### Example Queries

**Get House Standings:**
```graphql
query {
  houseStandings {
    house
    points
  }
}
```

**Get Point Transactions:**
```graphql
query {
  pointTransactions(house: "Gryffindor") {
    id
    house
    points
    reason
    awardedBy {
      name
    }
    wizard {
      name
    }
    timestamp
  }
}
```

**Add Points:**
```graphql
mutation {
  awardPoints(
    house: "Gryffindor", 
    points: 10, 
    reason: "Answering correctly in class", 
    teacherId: 2, 
    wizardId: 1
  ) {
    id
    house
    points
  }
}
```

## Development Setup

### Prerequisites

* Docker and Docker Compose
* Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hogwarts.git
   cd hogwarts
   ```

2. **Configure environment variables:**
   Create a `.env` file in the project root with the following content:
   ```
   # Database Configuration
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=hogwarts

   # Database URL for backend connection
   DATABASE_URL=postgresql://postgres:postgres@postgres-hogwarts-dev:5432/hogwarts

   # Frontend configuration
   REACT_APP_API_URL=http://localhost:8000/graphql
   ```

3. **Start the development environment:**
   ```bash
   docker-compose -f dev.docker-compose.yml up -d
   ```

4. **Access the application:**
   * Frontend: http://localhost:3000
   * Backend API Docs: http://localhost:8000/docs
   * GraphQL Playground: http://localhost:8000/graphql
   * Adminer: http://localhost:8080

### Development Workflow

1. **Make code changes** in the `frontend/` or `backend/` directories
2. **Test your changes** using the APIs and frontend
3. **Create database migrations** when changing the schema:
   ```bash
   # Inside the backend container
   docker-compose -f dev.docker-compose.yml exec backend-hogwarts-dev alembic revision --autogenerate -m "Description of the change"
   docker-compose -f dev.docker-compose.yml exec backend-hogwarts-dev alembic upgrade head
   ```

## Production Deployment

### Setup Instructions

1. **Configure production environment variables:**
   Create a `.env.prod` file with secure credentials.

2. **Deploy with Docker Compose:**
   ```bash
   docker-compose -f prod.docker-compose.yml up -d
   ```

3. **Database Migrations:**
   ```bash
   docker-compose -f prod.docker-compose.yml exec backend-hogwarts-prod alembic upgrade head
   ```

4. **Access Adminer in production** (when needed):
   ```bash
   docker-compose -f prod.docker-compose.yml --profile admin up -d adminer-hogwarts-prod
   ```

### Security Considerations

* Use strong, unique passwords for the database
* Restrict the CORS settings in production
* Enable Adminer only when needed
* Configure a firewall to restrict access to ports
* Use HTTPS for all production traffic

## Common Tasks

### Adding a New Student

1. **Using Adminer:**
   * Log in to Adminer (http://localhost:8080)
   * Navigate to the `wizards` table
   * Click "New item" and fill in the student details

2. **Using the API:**
   ```graphql
   mutation {
     createWizard(
       name: "Luna Lovegood", 
       house: "Ravenclaw", 
       wand: "Unknown", 
       patronus: "Hare"
     ) {
       id
       name
     }
   }
   ```

### Awarding Points to a Student

1. **Using the Frontend:**
   * Navigate to the Points Award form
   * Select the house, enter points and reason
   * Select the student (optional)
   * Select the teacher awarding the points
   * Submit the form

2. **Using the REST API:**
   ```http
   POST /api/house-points/
   Content-Type: application/json

   {
     "house": "Gryffindor",
     "points": 10,
     "reason": "Excellent spell casting",
     "awarded_by": "Filius Flitwick",
     "student_name": "Hermione Granger"
   }
   ```

### Viewing House Standings

1. **Using the Frontend:**
   * Navigate to the dashboard to see current standings

2. **Using the API:**
   ```http
   GET /api/house-points/standings
   ```

### Resetting the Database

If you need to start fresh with a clean database:

```bash
# Stop containers and remove volumes
docker-compose -f dev.docker-compose.yml down -v

# Start containers again
docker-compose -f dev.docker-compose.yml up -d
```

The system will automatically initialize with sample data.

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. **Check the credentials** in your `.env` file match the ones expected by the database
2. **Ensure service names match** in the `DATABASE_URL` environment variable and docker-compose file
3. **Check container logs**:
   ```bash
   docker-compose -f dev.docker-compose.yml logs postgres-hogwarts-dev
   docker-compose -f dev.docker-compose.yml logs backend-hogwarts-dev
   ```

### Docker Container Networking

Remember that containers communicate with each other using their service names:

* **Correct** (for container-to-container): `postgres-hogwarts-dev`
* **Incorrect** (for container-to-container): `localhost`

Example:
```
# Correct (for backend container connecting to database container)
DATABASE_URL=postgresql://postgres:postgres@postgres-hogwarts-dev:5432/hogwarts

# Correct (for connecting from your local machine)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hogwarts
```

### API Response Errors

If you encounter API errors:

1. **Check the API documentation** at `/docs` for correct request format
2. **Validate JSON request bodies** when using POST/PUT methods
3. **Inspect the logs** for detailed error information

### Common Error Messages

* **"Role does not exist"**: Database username is incorrect
* **"Database does not exist"**: Database name is incorrect
* **"Connection refused"**: Service is not running or network issue
* **"could not translate host name"**: Container name mismatch in DATABASE_URL