# Hogwarts House Points Management System Makefile
# Make commands to simplify development and deployment workflows

.PHONY: help dev-up dev-down prod-up prod-down logs backend-shell frontend-shell db-shell clean init-frontend restart status fix-db-config reset-db adminer prod-adminer init-db migrate backup-db

# Default target when make is called without arguments
help:
	@echo "Hogwarts House Points Management System"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  help               Show this help message"
	@echo "  dev-up             Start development environment"
	@echo "  dev-down           Stop development environment"
	@echo "  prod-up            Start production environment"
	@echo "  prod-down          Stop production environment"
	@echo "  logs               Show logs for all containers"
	@echo "  logs-backend       Show logs for backend container"
	@echo "  logs-frontend      Show logs for frontend container"
	@echo "  backend-shell      Open a shell in the backend container"
	@echo "  frontend-shell     Open a shell in the frontend container"
	@echo "  db-shell           Open a psql shell to the database"
	@echo "  clean              Remove all containers and volumes"
	@echo "  init-frontend      Initialize the frontend project"
	@echo "  restart            Restart all containers"
	@echo "  status             Show status of all containers"
	@echo "  fix-db-config      Fix database configuration in .env file"
	@echo "  reset-db           Reset the database and reinitialize with test data"
	@echo "  adminer            Open Adminer in the default browser"
	@echo "  prod-adminer       Start Adminer in production mode"
	@echo "  init-db            Initialize database with test data"
	@echo "  migrate            Run database migrations"
	@echo "  backup-db          Backup the database"

# Development environment commands
dev-up:
	docker-compose -f dev.docker-compose.yml up -d
	@echo "Access the application at:"
	@echo "- Frontend: http://localhost:3000"
	@echo "- API Docs: http://localhost:8000/docs"
	@echo "- GraphQL: http://localhost:8000/graphql"
	@echo "- Adminer: http://localhost:8080"

dev-down:
	docker-compose -f dev.docker-compose.yml down

# Production environment commands
prod-up:
	docker-compose -f prod.docker-compose.yml up -d

prod-down:
	docker-compose -f prod.docker-compose.yml down

# Log commands
logs:
	docker-compose -f dev.docker-compose.yml logs -f

logs-backend:
	docker-compose -f dev.docker-compose.yml logs -f backend-hogwarts-dev

logs-frontend:
	docker-compose -f dev.docker-compose.yml logs -f frontend-hogwarts-dev

# Shell access
backend-shell:
	docker-compose -f dev.docker-compose.yml exec backend-hogwarts-dev /bin/bash

frontend-shell:
	docker-compose -f dev.docker-compose.yml exec frontend-hogwarts-dev /bin/sh

db-shell:
	@echo "Connecting to database..."
	@source .env && docker-compose -f dev.docker-compose.yml exec postgres-hogwarts-dev psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

# Cleanup
clean:
	docker-compose -f dev.docker-compose.yml down -v
	docker-compose -f prod.docker-compose.yml down -v
	
# Initialize frontend project
init-frontend:
	docker-compose -f dev.docker-compose.yml run --rm frontend-hogwarts-dev sh -c "npx create-react-app . --template typescript"

# Restart containers
restart:
	docker-compose -f dev.docker-compose.yml restart

# Show status of running containers
status:
	docker-compose -f dev.docker-compose.yml ps

# Fix database configuration
fix-db-config:
	@echo "Fixing database configuration in .env file..."
	@sed -i.bak 's/DATABASE_URL=.*/DATABASE_URL=postgresql:\/\/postgres:postgres@postgres-hogwarts-dev:5432\/hogwarts/' .env
	@sed -i.bak 's/POSTGRES_USER=.*/POSTGRES_USER=postgres/' .env
	@sed -i.bak 's/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=postgres/' .env
	@sed -i.bak 's/POSTGRES_DB=.*/POSTGRES_DB=hogwarts/' .env
	@echo "Database configuration fixed. You should restart the application with 'make restart'."

# Reset the database
reset-db: clean dev-up
	@echo "Database has been reset with fresh data."
	@echo "You can access Adminer at http://localhost:8080 to verify."

# Open Adminer in the default browser
adminer:
	@echo "Opening Adminer in your default browser..."
	@python -m webbrowser "http://localhost:8080"
	@echo "Login with:"
	@echo "System: PostgreSQL"
	@echo "Server: postgres-hogwarts-dev"
	@source .env && echo "Username: $${POSTGRES_USER}"
	@source .env && echo "Password: $${POSTGRES_PASSWORD}"
	@source .env && echo "Database: $${POSTGRES_DB}"

# Start Adminer in production
prod-adminer:
	docker-compose -f prod.docker-compose.yml --profile admin up -d adminer-hogwarts-prod
	@echo "Adminer is now running at http://localhost:8080"

# Initialize database with test data
init-db:
	docker-compose -f dev.docker-compose.yml exec backend-hogwarts-dev python -m app.database.init_db
	@echo "Database initialized with test data."

# Run database migrations
migrate:
	docker-compose -f dev.docker-compose.yml exec backend-hogwarts-dev alembic upgrade head
	@echo "Database migrations have been applied."

# Backup the database
backup-db:
	@mkdir -p backups
	@source .env && docker-compose -f dev.docker-compose.yml exec postgres-hogwarts-dev pg_dump -U $${POSTGRES_USER} $${POSTGRES_DB} > backups/hogwarts-$$(date +%Y%m%d-%H%M%S).sql
	@echo "Database backup created in backups/ directory." 