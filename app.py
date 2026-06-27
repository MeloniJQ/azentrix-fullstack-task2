# app.py - Simple Task Management System
# Run: python app.py
# Access: http://localhost:5000

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name
        }


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_demo = db.Column(db.Boolean, default=False)
    
    tasks = db.relationship('Task', backref='board', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'is_demo': self.is_demo
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, done
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    assigned_to = db.Column(db.String(120))
    due_date = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='task', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'board_id': self.board_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'progress': self.progress,
            'comments_count': len(self.comments),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# AUTHENTICATION HELPERS
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# ============================================================================
# ROUTES - AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('auth.html')


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    # Validation
    if not all([data.get('username'), data.get('email'), data.get('password'), data.get('full_name')]):
        return jsonify({'error': 'All fields required'}), 400
    
    # Check existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()
    
    # Create demo workspace for new user
    create_demo_workspace(user.id)
    
    db.session.commit()
    
    session['user_id'] = user.id
    session['user_name'] = user.full_name
    
    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict(),
        'has_demo': True
    }), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter(
        (User.email == data.get('email')) | (User.username == data.get('email'))
    ).first()
    
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['user_id'] = user.id
    session['user_name'] = user.full_name
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200


# ============================================================================
# ROUTES - BOARDS
# ============================================================================

@app.route('/api/boards', methods=['GET'])
@login_required
def get_boards():
    user_id = session['user_id']
    boards = Board.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in boards]), 200


@app.route('/api/boards', methods=['POST'])
@login_required
def create_board():
    data = request.json
    user_id = session['user_id']
    
    board = Board(
        user_id=user_id,
        name=data.get('name'),
        description=data.get('description', '')
    )
    db.session.add(board)
    db.session.commit()
    
    return jsonify({'board': board.to_dict(), 'message': 'Board created'}), 201


@app.route('/api/boards/<int:board_id>', methods=['DELETE'])
@login_required
def delete_board(board_id):
    board = Board.query.get_or_404(board_id)
    
    if board.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(board)
    db.session.commit()
    
    return jsonify({'message': 'Board deleted'}), 200


# ============================================================================
# ROUTES - TASKS
# ============================================================================

@app.route('/api/boards/<int:board_id>/tasks', methods=['GET'])
@login_required
def get_tasks(board_id):
    board = Board.query.get_or_404(board_id)
    
    if board.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    tasks = Task.query.filter_by(board_id=board_id).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@app.route('/api/boards/<int:board_id>/tasks', methods=['POST'])
@login_required
def create_task(board_id):
    board = Board.query.get_or_404(board_id)
    
    if board.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    task = Task(
        board_id=board_id,
        title=data.get('title'),
        description=data.get('description', ''),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        assigned_to=data.get('assigned_to'),
        due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None
    )
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'task': task.to_dict(), 'message': 'Task created'}), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    board = Board.query.get(task.board_id)
    
    if board.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.assigned_to = data.get('assigned_to', task.assigned_to)
    task.progress = data.get('progress', task.progress)
    
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data['due_date']).date()
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'task': task.to_dict()}), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    board = Board.query.get(task.board_id)
    
    if board.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted'}), 200


# ============================================================================
# ROUTES - COMMENTS
# ============================================================================

@app.route('/api/tasks/<int:task_id>/comments', methods=['GET'])
@login_required
def get_comments(task_id):
    task = Task.query.get_or_404(task_id)
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
    return jsonify([c.to_dict() for c in comments]), 200


@app.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
@login_required
def add_comment(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    comment = Comment(
        task_id=task_id,
        author=session.get('user_name', 'Anonymous'),
        content=data.get('content')
    )
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'comment': comment.to_dict()}), 201


@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200


# ============================================================================
# ROUTES - DEMO WORKSPACE
# ============================================================================

def create_demo_workspace(user_id):
    """Create demo workspace for new users"""
    
    # Create demo board
    board = Board(
        user_id=user_id,
        name='Team Collaboration Demo',
        description='Explore task management with this sample board. Feel free to modify, create, and delete tasks!',
        is_demo=True
    )
    db.session.add(board)
    db.session.flush()
    
    # Demo team members
    team_members = [
        'Sarah Anderson (PM)',
        'Alex Chen (Frontend)',
        'Jordan Smith (Backend)',
        'Casey Miller (QA)'
    ]
    
    # TODO column tasks
    todo_tasks = [
        {
            'title': 'Design Login Page UI/UX',
            'description': 'Create beautiful and intuitive login interface with email and password fields.',
            'priority': 'high',
            'assigned_to': 'Alex Chen (Frontend)',
            'due_days': 5
        },
        {
            'title': 'Create Database Schema',
            'description': 'Design and implement database schema with proper relationships and indexes.',
            'priority': 'high',
            'assigned_to': 'Jordan Smith (Backend)',
            'due_days': 3
        },
        {
            'title': 'Setup Deployment Pipeline',
            'description': 'Configure CI/CD pipeline with GitHub Actions for automated testing and deployment.',
            'priority': 'medium',
            'assigned_to': 'Jordan Smith (Backend)',
            'due_days': 7
        }
    ]
    
    # IN PROGRESS column tasks
    in_progress_tasks = [
        {
            'title': 'Implement JWT Authentication',
            'description': 'Create secure JWT-based authentication system with token generation.',
            'priority': 'high',
            'assigned_to': 'Jordan Smith (Backend)',
            'due_days': 2,
            'progress': 65
        },
        {
            'title': 'Build Drag-and-Drop Kanban Board',
            'description': 'Implement interactive kanban board with smooth drag-and-drop functionality.',
            'priority': 'high',
            'assigned_to': 'Alex Chen (Frontend)',
            'due_days': 4,
            'progress': 45
        }
    ]
    
    # DONE column tasks
    done_tasks = [
        {
            'title': 'Project Planning & Requirements',
            'description': 'Define project scope, features, and technical requirements.',
            'priority': 'high',
            'assigned_to': 'Sarah Anderson (PM)',
            'status': 'done',
            'days_ago': 10
        },
        {
            'title': 'Requirement Analysis & Feature Definition',
            'description': 'Detailed analysis of all project requirements with stakeholder input.',
            'priority': 'medium',
            'assigned_to': 'Sarah Anderson (PM)',
            'status': 'done',
            'days_ago': 8
        }
    ]
    
    # Create TODO tasks
    for task_data in todo_tasks:
        task = Task(
            board_id=board.id,
            title=task_data['title'],
            description=task_data['description'],
            status='todo',
            priority=task_data['priority'],
            assigned_to=task_data.get('assigned_to'),
            due_date=datetime.utcnow().date() + timedelta(days=task_data.get('due_days', 0))
        )
        db.session.add(task)
        db.session.flush()
        
        # Add sample comment
        comment = Comment(
            task_id=task.id,
            author='Team Member',
            content='This looks good! Let me know if you need any help.'
        )
        db.session.add(comment)
    
    # Create IN PROGRESS tasks
    for task_data in in_progress_tasks:
        task = Task(
            board_id=board.id,
            title=task_data['title'],
            description=task_data['description'],
            status='in_progress',
            priority=task_data['priority'],
            assigned_to=task_data.get('assigned_to'),
            due_date=datetime.utcnow().date() + timedelta(days=task_data.get('due_days', 0)),
            progress=task_data.get('progress', 0)
        )
        db.session.add(task)
        db.session.flush()
        
        # Add comments
        comments_text = [
            'Started working on this. Initial implementation in progress.',
            'Need to review requirements before continuing.',
            'Great progress! Keep up the good work.'
        ]
        for comment_text in comments_text[:2]:
            comment = Comment(
                task_id=task.id,
                author='Team Member',
                content=comment_text
            )
            db.session.add(comment)
    
    # Create DONE tasks
    for task_data in done_tasks:
        task = Task(
            board_id=board.id,
            title=task_data['title'],
            description=task_data['description'],
            status=task_data.get('status', 'done'),
            priority=task_data['priority'],
            assigned_to=task_data.get('assigned_to'),
            progress=100
        )
        db.session.add(task)
        db.session.flush()
        
        # Add completion comment
        comment = Comment(
            task_id=task.id,
            author='Team Member',
            content='Completed successfully! Great work everyone.'
        )
        db.session.add(comment)
    
    db.session.commit()


@app.route('/api/reset-demo/<int:board_id>', methods=['POST'])
@login_required
def reset_demo(board_id):
    board = Board.query.get_or_404(board_id)
    
    if board.user_id != session['user_id'] or not board.is_demo:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Delete all tasks
    Task.query.filter_by(board_id=board_id).delete()
    db.session.commit()
    
    # Recreate demo tasks
    create_demo_workspace(session['user_id'])
    
    return jsonify({'message': 'Demo workspace reset'}), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

with app.app_context():
    db.create_all()
    print('✓ Database initialized')


if __name__ == '__main__':
    print('🚀 Starting TaskFlow...')
    print('📍 Access at http://localhost:5000')
    print('💡 Create an account to get started!')
    app.run(debug=True, port=5000)
