import unittest
import json
from app import app, db
from app import User, Task

class TaskManagerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(username='test_user', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            
            # Create test tasks
            task1 = Task(
                title='Test Task 1',
                description='Description for test task 1',
                priority='High',
                status='To Do',
                user_id=1
            )
            task2 = Task(
                title='Test Task 2',
                description='Description for test task 2',
                priority='Normal',
                status='In Progress',
                user_id=1
            )
            db.session.add_all([task1, task2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amazon Task Manager', response.data)

    def test_tasks_page(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task 1', response.data)
        self.assertIn(b'Test Task 2', response.data)

    def test_new_task(self):
        response = self.client.post('/task/new', data={
            'title': 'New Test Task',
            'description': 'Description for new test task',
            'priority': 'Urgent',
            'status': 'To Do'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Test Task', response.data)
        self.assertIn(b'Task created successfully', response.data)

    def test_edit_task(self):
        response = self.client.post('/task/1/edit', data={
            'title': 'Updated Test Task',
            'description': 'Updated description',
            'priority': 'Low',
            'status': 'Done'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Test Task', response.data)
        self.assertIn(b'Task updated successfully', response.data)

    def test_delete_task(self):
        response = self.client.post('/task/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task deleted successfully', response.data)
        self.assertNotIn(b'Test Task 1', response.data)

    def test_api_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['tasks']), 2)

    def test_api_get_task(self):
        response = self.client.get('/api/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['task']['title'], 'Test Task 1')

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_404_error(self):
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()