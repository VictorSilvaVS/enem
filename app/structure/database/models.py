from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from app.structure.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relacionamentos
    study_sessions = db.relationship('StudySession', backref='user', lazy=True, cascade='all, delete-orphan')
    progress_records = db.relationship('ProgressRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}>'

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    area = db.Column(db.String(50), nullable=False)  # Linguagens, Ciências Humanas, etc.
    color = db.Column(db.String(7), default='#007bff')  # Cor hex para UI
    icon = db.Column(db.String(50), default='book')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    topics = db.relationship('Topic', backref='subject', lazy=True, cascade='all, delete-orphan')
    study_materials = db.relationship('StudyMaterial', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5
    estimated_hours = db.Column(db.Float, default=1.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    study_materials = db.relationship('StudyMaterial', backref='topic', lazy=True, cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='topic', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Topic {self.name}>'

class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    material_type = db.Column(db.String(50), nullable=False)  # text, video, pdf, etc.
    file_path = db.Column(db.String(255))  # Para arquivos
    url = db.Column(db.String(500))  # Para links externos
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    difficulty_level = db.Column(db.Integer, default=1)
    estimated_time = db.Column(db.Integer, default=15)  # em minutos
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StudyMaterial {self.title}>'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # multiple_choice, true_false, essay
    difficulty_level = db.Column(db.Integer, default=1)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}>'

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    explanation = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    
    def __repr__(self):
        return f'<Answer {self.id}>'

class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('study_materials.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<StudySession {self.id}>'

class ProgressRecord(db.Model):
    __tablename__ = 'progress_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    progress_percentage = db.Column(db.Float, default=0.0)
    materials_completed = db.Column(db.Integer, default=0)
    total_materials = db.Column(db.Integer, default=0)
    last_studied = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProgressRecord {self.id}>'

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    time_taken = db.Column(db.Integer)  # em segundos
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizAttempt {self.id}>'

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer)  # em segundos
    
    def __repr__(self):
        return f'<UserAnswer {self.id}>'
