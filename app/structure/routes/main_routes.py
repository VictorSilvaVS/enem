from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.structure.database.models import (
    Subject, Topic, StudyMaterial, ProgressRecord, StudySession, 
    QuizAttempt, Question, Answer, db
)
from app.structure.auth.auth_manager import admin_required
from datetime import datetime, timedelta
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página inicial do sistema"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Estatísticas gerais para mostrar na página inicial
    total_subjects = Subject.query.filter_by(is_active=True).count()
    total_topics = Topic.query.filter_by(is_active=True).count()
    total_materials = StudyMaterial.query.filter_by(is_active=True).count()
    
    return render_template('main/index.html', 
                         total_subjects=total_subjects,
                         total_topics=total_topics,
                         total_materials=total_materials)

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do usuário"""
    # Buscar progresso do usuário
    user_progress = ProgressRecord.query.filter_by(user_id=current_user.id).all()
    
    # Estatísticas do usuário
    total_study_time = db.session.query(db.func.sum(StudySession.duration_minutes))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    total_quizzes = QuizAttempt.query.filter_by(user_id=current_user.id).count()
    completed_materials = db.session.query(db.func.sum(ProgressRecord.materials_completed))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    # Sessões de estudo recentes
    recent_sessions = StudySession.query.filter_by(user_id=current_user.id)\
        .order_by(StudySession.start_time.desc()).limit(5).all()
    
    # Progresso por área do conhecimento
    subjects = Subject.query.filter_by(is_active=True).all()
    subject_progress = {}
    
    for subject in subjects:
        progress = ProgressRecord.query.filter_by(
            user_id=current_user.id, 
            subject_id=subject.id
        ).first()
        
        if progress:
            subject_progress[subject.name] = progress.progress_percentage
        else:
            subject_progress[subject.name] = 0.0
    
    return render_template('main/dashboard.html',
                         user_progress=user_progress,
                         total_study_time=total_study_time,
                         total_quizzes=total_quizzes,
                         completed_materials=completed_materials,
                         recent_sessions=recent_sessions,
                         subject_progress=subject_progress,
                         subjects=subjects)

@main.route('/subjects')
@login_required
def subjects():
    """Lista todas as disciplinas disponíveis"""
    subjects = Subject.query.filter_by(is_active=True).all()
    return render_template('main/subjects.html', subjects=subjects)

@main.route('/subject/<int:subject_id>')
@login_required
def subject_detail(subject_id):
    """Detalhes de uma disciplina específica"""
    subject = Subject.query.get_or_404(subject_id)
    topics = Topic.query.filter_by(subject_id=subject_id, is_active=True).all()
    
    # Progresso do usuário nesta disciplina
    user_progress = ProgressRecord.query.filter_by(
        user_id=current_user.id, 
        subject_id=subject_id
    ).all()
    
    return render_template('main/subject_detail.html', 
                         subject=subject, 
                         topics=topics,
                         user_progress=user_progress)

@main.route('/topic/<int:topic_id>')
@login_required
def topic_detail(topic_id):
    """Detalhes de um tópico específico"""
    topic = Topic.query.get_or_404(topic_id)
    materials = StudyMaterial.query.filter_by(topic_id=topic_id, is_active=True).all()
    
    # Progresso do usuário neste tópico
    progress = ProgressRecord.query.filter_by(
        user_id=current_user.id, 
        topic_id=topic_id
    ).first()
    
    return render_template('main/topic_detail.html', 
                         topic=topic, 
                         materials=materials,
                         progress=progress)

@main.route('/material/<int:material_id>')
@login_required
def study_material(material_id):
    """Visualizar material de estudo"""
    material = StudyMaterial.query.get_or_404(material_id)
    
    # Iniciar sessão de estudo
    session = StudySession(
        user_id=current_user.id,
        subject_id=material.subject_id,
        topic_id=material.topic_id,
        material_id=material.id,
        start_time=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()
    
    return render_template('main/study_material.html', 
                         material=material, 
                         session_id=session.id)

@main.route('/material/<int:material_id>/complete', methods=['POST'])
@login_required
def complete_material(material_id):
    """Marcar material como concluído"""
    material = StudyMaterial.query.get_or_404(material_id)
    session_id = request.form.get('session_id')
    
    # Finalizar sessão de estudo
    if session_id:
        study_session = StudySession.query.get(session_id)
        if study_session and study_session.user_id == current_user.id:
            study_session.end_time = datetime.utcnow()
            study_session.duration_minutes = int((study_session.end_time - study_session.start_time).total_seconds() / 60)
            study_session.completed = True
            study_session.notes = request.form.get('notes', '')
    
    # Atualizar progresso
    progress = ProgressRecord.query.filter_by(
        user_id=current_user.id,
        subject_id=material.subject_id,
        topic_id=material.topic_id
    ).first()
    
    if not progress:
        progress = ProgressRecord(
            user_id=current_user.id,
            subject_id=material.subject_id,
            topic_id=material.topic_id,
            materials_completed=1,
            total_materials=StudyMaterial.query.filter_by(topic_id=material.topic_id, is_active=True).count(),
            last_studied=datetime.utcnow()
        )
        db.session.add(progress)
    else:
        progress.materials_completed += 1
        progress.last_studied = datetime.utcnow()
    
    # Calcular porcentagem de progresso
    total_materials = StudyMaterial.query.filter_by(topic_id=material.topic_id, is_active=True).count()
    progress.progress_percentage = (progress.materials_completed / total_materials) * 100
    progress.total_materials = total_materials
    
    db.session.commit()
    
    flash('Material concluído com sucesso!', 'success')
    return redirect(url_for('main.topic_detail', topic_id=material.topic_id))

@main.route('/quiz/<int:topic_id>')
@login_required
def start_quiz(topic_id):
    """Iniciar um quiz sobre um tópico"""
    topic = Topic.query.get_or_404(topic_id)
    questions = Question.query.filter_by(topic_id=topic_id, is_active=True).limit(10).all()
    
    if not questions:
        flash('Não há questões disponíveis para este tópico.', 'warning')
        return redirect(url_for('main.topic_detail', topic_id=topic_id))
    
    # Criar tentativa de quiz
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        subject_id=topic.subject_id,
        topic_id=topic_id,
        total_questions=len(questions),
        start_time=datetime.utcnow()
    )
    db.session.add(quiz_attempt)
    db.session.commit()
    
    return render_template('main/quiz.html', 
                         topic=topic, 
                         questions=questions,
                         quiz_attempt_id=quiz_attempt.id)

@main.route('/quiz/<int:quiz_attempt_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_attempt_id):
    """Submeter respostas do quiz"""
    quiz_attempt = QuizAttempt.query.get_or_404(quiz_attempt_id)
    
    if quiz_attempt.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    answers_data = request.get_json()
    correct_answers = 0
    
    for question_id, answer_id in answers_data.items():
        answer = Answer.query.get(answer_id)
        if answer and answer.is_correct:
            correct_answers += 1
    
    # Calcular pontuação
    score = (correct_answers / quiz_attempt.total_questions) * 100
    
    # Atualizar tentativa de quiz
    quiz_attempt.score = score
    quiz_attempt.correct_answers = correct_answers
    quiz_attempt.completed = True
    quiz_attempt.end_time = datetime.utcnow()
    quiz_attempt.time_taken = int((quiz_attempt.end_time - quiz_attempt.start_time).total_seconds())
    
    db.session.commit()
    
    return jsonify({
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': quiz_attempt.total_questions
    })

@main.route('/progress')
@login_required
def progress():
    """Página de progresso detalhado"""
    # Progresso por disciplina
    subjects = Subject.query.filter_by(is_active=True).all()
    progress_data = {}
    
    for subject in subjects:
        progress = ProgressRecord.query.filter_by(
            user_id=current_user.id, 
            subject_id=subject.id
        ).all()
        
        if progress:
            total_progress = sum(p.progress_percentage for p in progress) / len(progress)
            progress_data[subject.name] = {
                'progress': total_progress,
                'topics': progress
            }
        else:
            progress_data[subject.name] = {
                'progress': 0.0,
                'topics': []
            }
    
    # Estatísticas gerais
    total_study_time = db.session.query(db.func.sum(StudySession.duration_minutes))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    total_quizzes = QuizAttempt.query.filter_by(user_id=current_user.id).count()
    average_quiz_score = db.session.query(db.func.avg(QuizAttempt.score))\
        .filter_by(user_id=current_user.id, completed=True).scalar() or 0
    
    return render_template('main/progress.html',
                         progress_data=progress_data,
                         total_study_time=total_study_time,
                         total_quizzes=total_quizzes,
                         average_quiz_score=average_quiz_score)

@main.route('/search')
@login_required
def search():
    """Busca por materiais e tópicos"""
    query = request.args.get('q', '')
    if not query:
        return render_template('main/search.html', results=[])
    
    # Buscar em materiais
    materials = StudyMaterial.query.filter(
        StudyMaterial.title.contains(query) | 
        StudyMaterial.content.contains(query)
    ).filter_by(is_active=True).limit(10).all()
    
    # Buscar em tópicos
    topics = Topic.query.filter(
        Topic.name.contains(query) | 
        Topic.description.contains(query)
    ).filter_by(is_active=True).limit(10).all()
    
    results = {
        'materials': materials,
        'topics': topics
    }
    
    return render_template('main/search.html', results=results, query=query)

# Rotas administrativas
@main.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Dashboard administrativo"""
    total_users = User.query.count()
    total_subjects = Subject.query.count()
    total_materials = StudyMaterial.query.count()
    total_questions = Question.query.count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_subjects=total_subjects,
                         total_materials=total_materials,
                         total_questions=total_questions)
