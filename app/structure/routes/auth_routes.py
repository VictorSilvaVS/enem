from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.structure.forms.auth_forms import (
    LoginForm, RegistrationForm, ChangePasswordForm, 
    ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
)
from app.structure.auth.auth_manager import authenticate_user, create_user
from app.structure.database.models import User, db
from urllib.parse import urlparse

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            flash(f'Bem-vindo de volta, {user.first_name}!', 'success')
            return redirect(next_page)
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            flash('Conta criada com sucesso! Agora você pode fazer login.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('auth/register.html', title='Registro', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        # Verificar se o email já está em uso por outro usuário
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Este email já está em uso por outro usuário.', 'danger')
        else:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='Perfil', form=form)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Senha atual incorreta.', 'danger')
    
    return render_template('auth/change_password.html', title='Alterar Senha', form=form)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Aqui você implementaria o envio de email
            # Por enquanto, apenas mostra uma mensagem
            flash('Se o email existir em nossa base de dados, você receberá instruções para redefinir sua senha.', 'info')
        else:
            # Não revelar se o email existe ou não por segurança
            flash('Se o email existir em nossa base de dados, você receberá instruções para redefinir sua senha.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', title='Reset de Senha', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Aqui você implementaria a verificação do token
    # Por enquanto, apenas mostra o formulário
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Implementar a lógica de reset de senha
        flash('Sua senha foi redefinida com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Redefinir Senha', form=form)

@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    # Implementar confirmação de senha antes de deletar
    password = request.form.get('password')
    if current_user.check_password(password):
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash('Sua conta foi deletada com sucesso.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Senha incorreta. Conta não foi deletada.', 'danger')
        return redirect(url_for('auth.profile'))
