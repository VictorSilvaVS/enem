from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.structure.database.models import User

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
        DataRequired(message='Nome de usuário é obrigatório'),
        Length(min=3, max=80, message='Nome de usuário deve ter entre 3 e 80 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
        DataRequired(message='Nome de usuário é obrigatório'),
        Length(min=3, max=80, message='Nome de usuário deve ter entre 3 e 80 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido'),
        Length(max=120, message='Email deve ter no máximo 120 caracteres')
    ])
    first_name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    last_name = StringField('Sobrenome', validators=[
        DataRequired(message='Sobrenome é obrigatório'),
        Length(min=2, max=50, message='Sobrenome deve ter entre 2 e 50 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=8, message='Senha deve ter pelo menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('password', message='Senhas devem ser iguais')
    ])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nome de usuário já está em uso. Escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já está registrado. Use outro email.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[
        DataRequired(message='Senha atual é obrigatória')
    ])
    new_password = PasswordField('Nova Senha', validators=[
        DataRequired(message='Nova senha é obrigatória'),
        Length(min=8, message='Nova senha deve ter pelo menos 8 caracteres')
    ])
    confirm_new_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='Confirmação de nova senha é obrigatória'),
        EqualTo('new_password', message='Senhas devem ser iguais')
    ])
    submit = SubmitField('Alterar Senha')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    submit = SubmitField('Solicitar Reset de Senha')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[
        DataRequired(message='Nova senha é obrigatória'),
        Length(min=8, message='Nova senha deve ter pelo menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='Confirmação de nova senha é obrigatória'),
        EqualTo('password', message='Senhas devem ser iguais')
    ])
    submit = SubmitField('Redefinir Senha')

class ProfileForm(FlaskForm):
    first_name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    last_name = StringField('Sobrenome', validators=[
        DataRequired(message='Sobrenome é obrigatório'),
        Length(min=2, max=50, message='Sobrenome deve ter entre 2 e 50 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido'),
        Length(max=120, message='Email deve ter no máximo 120 caracteres')
    ])
    bio = TextAreaField('Biografia', validators=[
        Length(max=500, message='Biografia deve ter no máximo 500 caracteres')
    ])
    submit = SubmitField('Atualizar Perfil')
