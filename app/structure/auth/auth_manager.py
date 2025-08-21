from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import flash, redirect, url_for, request
from functools import wraps
from app.structure.database.models import User, db
from datetime import datetime
import jwt
import os
from datetime import datetime, timedelta

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('Você precisa fazer login para acessar esta página.', 'warning')
    return redirect(url_for('auth.login'))

def init_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Você precisa de privilégios de administrador.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def generate_token(user_id, expires_in=3600):
    """Gera um token JWT para o usuário"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, os.environ.get('SECRET_KEY', 'dev-secret'), algorithm='HS256')

def verify_token(token):
    """Verifica um token JWT"""
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev-secret'), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def update_last_login(user):
    """Atualiza o último login do usuário"""
    user.last_login = datetime.utcnow()
    db.session.commit()

def create_user(username, email, password, first_name, last_name, is_admin=False):
    """Cria um novo usuário de forma segura"""
    if User.query.filter_by(username=username).first():
        raise ValueError('Nome de usuário já existe')
    
    if User.query.filter_by(email=email).first():
        raise ValueError('Email já está em uso')
    
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return user

def authenticate_user(username, password):
    """Autentica um usuário"""
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password) and user.is_active:
        update_last_login(user)
        return user
    
    return None
