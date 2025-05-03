import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'amazon-task-manager-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://amazon:password@db:5432/taskdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='owner', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='Normal')  # Low, Normal, High, Urgent
    status = db.Column(db.String(20), default='To Do')  # To Do, In Progress, Done
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Forms
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'), 
        ('Normal', 'Normal'), 
        ('High', 'High'), 
        ('Urgent', 'Urgent')
    ])
    status = SelectField('Status', choices=[
        ('To Do', 'To Do'), 
        ('In Progress', 'In Progress'), 
        ('Done', 'Done')
    ])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[], render_kw={"type": "date"})
    submit = SubmitField('Save Task')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                          error_code=404, 
                          error_message="Page Not Found", 
                          error_description="The page you're looking for doesn't exist."), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal server error: {str(error)}")
    logger.error(traceback.format_exc())
    return render_template('error.html', 
                          error_code=500, 
                          error_message="Internal Server Error", 
                          error_description="Something went wrong on our end. Please try again later."), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', 
                          error_code=403, 
                          error_message="Forbidden", 
                          error_description="You don't have permission to access this resource."), 403

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error.html', 
                          error_code=400, 
                          error_message="Bad Request", 
                          error_description="The server could not understand your request."), 400

# Routes
@app.route('/')
def index():
    try:
        # For demo purposes, we'll show all tasks without authentication
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An error occurred while loading tasks. Please try again.', 'danger')
        return render_template('index.html', tasks=[])

@app.route('/tasks')
def tasks():
    try:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template('tasks.html', tasks=tasks)
    except SQLAlchemyError as e:
        logger.error(f"Database error in tasks route: {str(e)}")
        db.session.rollback()
        flash('A database error occurred. Please try again.', 'danger')
        return render_template('tasks.html', tasks=[])
    except Exception as e:
        logger.error(f"Error in tasks route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'danger')
        return render_template('tasks.html', tasks=[])

@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    try:
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                status=form.status.data,
                due_date=form.due_date.data,
                # For demo, we'll assign to a default user or first user
                user_id=1
            )
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks'))
        return render_template('task_form.html', form=form, title='New Task')
    except SQLAlchemyError as e:
        logger.error(f"Database error in new_task route: {str(e)}")
        db.session.rollback()
        flash('A database error occurred while creating the task. Please try again.', 'danger')
        return render_template('task_form.html', form=form, title='New Task')
    except Exception as e:
        logger.error(f"Error in new_task route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'danger')
        return render_template('task_form.html', form=form, title='New Task')

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            task.priority = form.priority.data
            task.status = form.status.data
            task.due_date = form.due_date.data
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks'))
        return render_template('task_form.html', form=form, title='Edit Task')
    except SQLAlchemyError as e:
        logger.error(f"Database error in edit_task route: {str(e)}")
        db.session.rollback()
        flash('A database error occurred while updating the task. Please try again.', 'danger')
        return render_template('task_form.html', form=form, title='Edit Task')
    except Exception as e:
        logger.error(f"Error in edit_task route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('tasks'))

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('tasks'))
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_task route: {str(e)}")
        db.session.rollback()
        flash('A database error occurred while deleting the task. Please try again.', 'danger')
        return redirect(url_for('tasks'))
    except Exception as e:
        logger.error(f"Error in delete_task route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('tasks'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now registered!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)
    except SQLAlchemyError as e:
        logger.error(f"Database error in register route: {str(e)}")
        db.session.rollback()
        flash('A database error occurred during registration. Please try again.', 'danger')
        return render_template('register.html', title='Register', form=form)
    except Exception as e:
        logger.error(f"Error in register route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'danger')
        return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            flash('You have been logged in!', 'success')
            return redirect(url_for('tasks'))
        return render_template('login.html', title='Sign In', form=form)
    except Exception as e:
        logger.error(f"Error in login route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An error occurred during login. Please try again.', 'danger')
        return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    # In a real app, we would handle proper logout with session management
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# API endpoints with error handling
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify({
            'success': True,
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority,
                    'status': task.status,
                    'created_at': task.created_at.isoformat(),
                    'due_date': task.due_date.isoformat() if task.due_date else None
                } for task in tasks
            ]
        })
    except Exception as e:
        logger.error(f"API error in get_tasks: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'An error occurred while fetching tasks',
            'message': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'created_at': task.created_at.isoformat(),
                'due_date': task.due_date.isoformat() if task.due_date else None
            }
        })
    except SQLAlchemyError as e:
        logger.error(f"Database error in api_get_task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500
    except Exception as e:
        logger.error(f"API error in get_task: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'An error occurred while fetching the task',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.cli.command("init-db")
def init_db():
    """Initialize the database with sample data."""
    try:
        db.create_all()
        
        # Create a default user if none exists
        if User.query.count() == 0:
            default_user = User(username='amazon_user', email='user@amazon.com')
            default_user.set_password('password')
            db.session.add(default_user)
            
            # Add some sample tasks
            tasks = [
                Task(title='Set up AWS EC2 instance', 
                     description='Launch a new t2.micro EC2 instance for the project',
                     priority='High', status='To Do', user_id=1),
                Task(title='Configure S3 bucket', 
                     description='Create and configure S3 bucket for file storage',
                     priority='Normal', status='To Do', user_id=1),
                Task(title='Deploy Lambda function', 
                     description='Create a Lambda function for processing incoming data',
                     priority='Urgent', status='In Progress', user_id=1),
                Task(title='Set up CloudWatch alarms', 
                     description='Configure CloudWatch alarms for monitoring resources',
                     priority='Normal', status='To Do', user_id=1),
                Task(title='Create IAM roles', 
                     description='Define IAM roles and policies for secure access',
                     priority='High', status='In Progress', user_id=1),
            ]
            db.session.add_all(tasks)
            db.session.commit()
            print('Database initialized with sample data.')
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Error initializing database: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')