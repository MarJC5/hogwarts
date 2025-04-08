# Development Setup Guide

This guide explains how to use the development Docker Compose setup to create and develop your React application without having Node.js installed locally. For basic setup instructions, please refer to the [Getting Started](../README.md#getting-started) section in the main README.

## Table of Contents
- [Initial Setup](#initial-setup)
- [Creating a New React App](#creating-a-new-react-app)
- [Development Workflow](#development-workflow)
- [Accessing the Application](#accessing-the-application)
- [Stopping the Development Environment](#stopping-the-development-environment)
- [Advanced Configuration](#advanced-configuration)

## Initial Setup

1. Create the project directories:
```bash
mkdir -p hogwarts/backend hogwarts/frontend
cd hogwarts
```

2. Copy all the backend files into the `backend` directory.

3. Start the development environment with:
```bash
docker-compose -f dev.docker-compose.yml up -d postgres backend node
```

## Creating a New React App

1. Enter the Node.js container to create a new React app:
```bash
docker-compose -f dev.docker-compose.yml exec node sh
```

2. Inside the container, create a new React app:
```bash
# Clear the directory if needed
rm -rf *

# Create a Next.js project with shadcn for components based on tailwindcss
npx shadcn@latest init

# Install additional dependencies
npm install @apollo/client graphql

# Exit the container when done
exit
```

3. Now update the frontend code with the components we've created.

4. Start the frontend development server:
```bash
docker-compose -f dev.docker-compose.yml up -d frontend-dev
```

## Development Workflow

### Backend Development
- Edit Python files in the `backend` directory using your preferred editor
- Changes will be automatically detected and the server will reload

### Frontend Development
- Edit React files in the `frontend` directory using your preferred editor
- Changes will be automatically detected and the app will reload

### Interacting with the Node Container
To run npm commands or other Node.js operations:
```bash
docker-compose -f dev.docker-compose.yml exec node sh
```

This gives you an interactive shell where you can run:
```bash
npm install some-package
npm run build
# etc.
```

## Accessing the Application

- Frontend: http://localhost:3000
- GraphQL API: http://localhost:8000/graphql

## Stopping the Development Environment

```bash
docker-compose -f dev.docker-compose.yml down
```

## Notes

1. The `node` service is for running one-off commands like creating a new React app or installing dependencies.

2. The `frontend-dev` service is for running the development server with hot reloading.

3. Both `node` and `frontend-dev` share the same volume, so changes made in one are reflected in the other.

4. If you need to completely reset the database, you can run:
```bash
docker-compose -f dev.docker-compose.yml down -v
```