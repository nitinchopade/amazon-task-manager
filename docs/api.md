# Amazon Task Manager API Documentation

This document provides details about the API endpoints available in the Amazon Task Manager application.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost/api
```

## Authentication

Currently, the API does not require authentication for demonstration purposes. In a production environment, proper authentication would be implemented.

## Endpoints

### List All Tasks

Retrieves a list of all tasks.

**URL**: `/tasks`

**Method**: `GET`

**Response Format**:

```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "Set up AWS EC2 instance",
      "description": "Launch a new t2.micro EC2 instance for the project",
      "priority": "High",
      "status": "To Do",
      "created_at": "2025-05-03T13:34:15.000000",
      "due_date": null
    },
    {
      "id": 2,
      "title": "Configure S3 bucket",
      "description": "Create and configure S3 bucket for file storage",
      "priority": "Normal",
      "status": "To Do",
      "created_at": "2025-05-03T13:34:15.000000",
      "due_date": null
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved tasks
- `500 Internal Server Error`: Server error

### Get a Specific Task

Retrieves details for a specific task by ID.

**URL**: `/tasks/{task_id}`

**Method**: `GET`

**URL Parameters**:
- `task_id`: The ID of the task to retrieve

**Response Format**:

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Set up AWS EC2 instance",
    "description": "Launch a new t2.micro EC2 instance for the project",
    "priority": "High",
    "status": "To Do",
    "created_at": "2025-05-03T13:34:15.000000",
    "due_date": null
  }
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved task
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

### Health Check

Checks the health status of the application and its database connection.

**URL**: `/health`

**Method**: `GET`

**Response Format**:

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-05-03T13:34:15.000000"
}
```

**Status Codes**:
- `200 OK`: System is healthy
- `500 Internal Server Error`: System is unhealthy

## Error Responses

All API endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

## Future Enhancements

The following API endpoints are planned for future releases:

- `POST /tasks`: Create a new task
- `PUT /tasks/{task_id}`: Update an existing task
- `DELETE /tasks/{task_id}`: Delete a task
- `GET /users`: List all users
- `GET /users/{user_id}`: Get a specific user
- `GET /users/{user_id}/tasks`: Get all tasks for a specific user