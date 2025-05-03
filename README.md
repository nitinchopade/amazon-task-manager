# Amazon Task Manager

![Amazon Task Manager](https://img.shields.io/badge/Amazon-Task%20Manager-FF9900?style=for-the-badge&logo=amazon&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.2.3-blue?style=flat-square&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)

An Amazon-themed task management application built with Flask and PostgreSQL, running in Docker containers. This project demonstrates DevOps best practices including containerization, database integration, and error handling.

## 📋 Features

- **Task Management**: Create, read, update, and delete tasks
- **Task Prioritization**: Categorize tasks as Low, Normal, High, or Urgent
- **Status Tracking**: Monitor task status (To Do, In Progress, Done)
- **User Authentication**: Register and login to manage your tasks
- **Amazon-themed UI**: Familiar orange and dark blue color scheme
- **API Endpoints**: Integration with other services
- **Health Monitoring**: Health check endpoint for system status
- **Error Handling**: Comprehensive error handling and logging
- **Containerized**: Fully dockerized application with PostgreSQL database

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Containerization**: Docker & Docker Compose
- **ORM**: SQLAlchemy
- **Forms**: Flask-WTF
- **Authentication**: Flask-Login (simulated for demo)
- **Testing**: Pytest & Pytest-Flask

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- Git (to clone the repository)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amazon-task-manager.git
   cd amazon-task-manager
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Initialize the database (first time only):
   ```bash
   docker-compose exec web flask init-db
   ```

4. Access the application:
   - Web UI: http://localhost
   - API: http://localhost/api/tasks
   - Health check: http://localhost/health

### Default Login

- **Username**: amazon_user
- **Password**: password

## 📁 Project Structure

```
amazon-task-manager/
├── app/                      # Flask application
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── css/              # CSS stylesheets
│   │   ├── js/               # JavaScript files
│   │   └── html/             # Static HTML files for error pages
│   ├── templates/            # HTML templates
│   ├── app.py                # Main application file
│   ├── Dockerfile            # Docker configuration for Flask app
│   ├── requirements.txt      # Python dependencies
│   └── tests.py              # Unit tests
├── init-scripts/             # PostgreSQL initialization scripts
├── nginx/                    # Nginx configuration
│   └── conf.d/               # Nginx server blocks
├── logs/                     # Application logs
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # Project documentation
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks` | GET | List all tasks |
| `/api/tasks/<id>` | GET | Get a specific task |
| `/health` | GET | Health check endpoint |

## 🔒 Security Features

- Password hashing
- Form CSRF protection
- Input validation
- Non-root user in Docker containers
- Database connection pooling
- Secure headers with Nginx

## 🧪 Testing

Run the tests with:

```bash
docker-compose exec web pytest
```

## 🔧 Troubleshooting

### Common Issues

1. **Container Restarting**: If the web container keeps restarting, check for dependency version conflicts in requirements.txt.

2. **Database Connection Issues**: Ensure the database container is healthy before accessing the application.

3. **Missing Tables**: If you see "relation does not exist" errors, run the init-db command:
   ```bash
   docker-compose exec web flask init-db
   ```

### Logs

View container logs with:

```bash
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

## 🛠️ Development

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

3. Set environment variables:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export DATABASE_URL=postgresql://amazon:password@localhost:5432/taskdb
   ```

4. Run the application:
   ```bash
   flask run
   ```

### Adding Dependencies

When adding new Python packages, update the requirements.txt file and rebuild the container:

```bash
docker-compose build web
docker-compose up -d
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS for design inspiration
- Flask and PostgreSQL communities
- Docker for containerization technology

## 📧 Contact

For questions or feedback, please open an issue on GitHub or contact the project maintainer.

---

Made with ❤️ by [Your Name]