# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-03

### Added
- Initial release of Amazon Task Manager
- Task creation, editing, and deletion functionality
- Task prioritization (Low, Normal, High, Urgent)
- Task status tracking (To Do, In Progress, Done)
- User registration and authentication
- Amazon-themed UI with responsive design
- API endpoints for task management
- Health check endpoint
- Comprehensive error handling and logging
- Docker and Docker Compose configuration
- PostgreSQL database integration
- Nginx as reverse proxy
- Unit tests with pytest

### Fixed
- Dependency conflict between Flask 2.2.3 and Werkzeug by pinning Werkzeug to version 2.2.3

## [0.1.0] - 2025-04-30

### Added
- Project scaffolding
- Initial Docker configuration
- Basic Flask application structure