# Architecture Overview

This document provides an overview of the Amazon Task Manager application architecture.

## System Architecture

The Amazon Task Manager is built using a containerized microservices architecture with the following components:

```
                   ┌─────────────┐
                   │    Client   │
                   │   Browser   │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │    Nginx    │
                   │ Web Server  │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │    Flask    │
                   │ Application │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ PostgreSQL  │
                   │  Database   │
                   └─────────────┘
```

### Components

1. **Client**: Web browser that interacts with the application
2. **Nginx**: Web server that handles HTTP requests and serves static files
3. **Flask Application**: Python web application that processes business logic
4. **PostgreSQL Database**: Persistent storage for application data

## Container Architecture

The application is containerized using Docker with the following services:

1. **Web Container (amazon-tasks-web)**:
   - Flask application
   - Gunicorn WSGI server
   - Application logic and API endpoints

2. **Database Container (amazon-tasks-db)**:
   - PostgreSQL database
   - Persistent volume for data storage
   - Initialization scripts

3. **Nginx Container (amazon-tasks-nginx)**:
   - Reverse proxy
   - Static file serving
   - SSL termination (in production)

## Data Model

### Entity Relationship Diagram

```
┌───────────────┐       ┌───────────────┐
│     User      │       │     Task      │
├───────────────┤       ├───────────────┤
│ id            │       │ id            │
│ username      │       │ title         │
│ email         │◄──────┤ description   │
│ password_hash │       │ created_at    │
│ created_at    │       │ due_date      │
└───────────────┘       │ priority      │
                        │ status        │
                        │ user_id       │
                        │ updated_at    │
                        └───────────────┘
```

### Database Schema

#### User Table

| Column        | Type         | Constraints       |
|---------------|--------------|-------------------|
| id            | Integer      | Primary Key       |
| username      | String(64)   | Unique, Not Null  |
| email         | String(120)  | Unique, Not Null  |
| password_hash | String(128)  |                   |
| created_at    | DateTime     | Default: now()    |

#### Task Table

| Column        | Type         | Constraints                |
|---------------|--------------|----------------------------|
| id            | Integer      | Primary Key                |
| title         | String(100)  | Not Null                   |
| description   | Text         |                            |
| created_at    | DateTime     | Default: now()             |
| due_date      | DateTime     | Nullable                   |
| priority      | String(20)   | Default: 'Normal'          |
| status        | String(20)   | Default: 'To Do'           |
| user_id       | Integer      | Foreign Key (User.id)      |
| updated_at    | DateTime     | Default: now(), on update  |

## Code Organization

```
amazon-task-manager/
├── app/                      # Flask application
│   ├── static/               # Static files
│   │   ├── css/              # CSS stylesheets
│   │   ├── js/               # JavaScript files
│   │   └── html/             # Static HTML files
│   ├── templates/            # HTML templates
│   ├── app.py                # Main application file
│   ├── Dockerfile            # Docker configuration
│   ├── requirements.txt      # Python dependencies
│   └── tests.py              # Unit tests
├── init-scripts/             # Database initialization
├── nginx/                    # Nginx configuration
│   └── conf.d/               # Server blocks
├── logs/                     # Application logs
└── docker-compose.yml        # Container orchestration
```

## Request Flow

1. User sends a request to the application
2. Nginx receives the request and forwards it to the Flask application
3. Flask processes the request:
   - Routes the request to the appropriate handler
   - Performs business logic
   - Interacts with the database as needed
   - Renders templates or returns API responses
4. Response flows back through Nginx to the user

## Authentication Flow

1. User submits login credentials
2. Flask validates the credentials against the database
3. If valid, a session is created for the user
4. Subsequent requests include the session information

## Error Handling

The application implements comprehensive error handling:

1. **Application Errors**:
   - Custom error pages for HTTP errors (404, 500, etc.)
   - Detailed logging of exceptions
   - User-friendly error messages

2. **Database Errors**:
   - Transaction rollback on errors
   - Connection retry logic
   - Detailed error logging

3. **API Errors**:
   - Consistent JSON error responses
   - Appropriate HTTP status codes
   - Detailed error messages for debugging

## Monitoring and Logging

1. **Application Logs**:
   - Structured logging with timestamps and severity levels
   - Error tracebacks for debugging
   - Request/response logging

2. **Health Checks**:
   - `/health` endpoint for monitoring
   - Database connection verification
   - System status reporting