#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do sistema de estudos ENEM
"""

from main import create_app
from app.structure.database import db
from app.structure.database.models import User, Subject, Topic, StudyMaterial, Question, Answer

def init_database():
    """Inicializa o banco de dados"""
    print("🔧 Inicializando o banco de dados...")
    
    # Criar aplicação Flask
    app = create_app()
    
    with app.app_context():
        # Verificar se as tabelas já existem
        print("📋 Verificando tabelas...")
        try:
            # Tentar fazer uma consulta simples para verificar se as tabelas existem
            User.query.first()
            print("✅ Tabelas já existem!")
        except:
            print("📋 Criando tabelas...")
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se já existem dados
        user_count = User.query.count()
        if user_count > 0:
            print(f"⚠️  Banco de dados já contém {user_count} usuários. Pulando população inicial.")
            return
        
        print("📊 Populando banco de dados com dados iniciais...")
        
        # Criar usuário administrador
        admin = User(
            username='admin',
            email='admin@enem.com',
            first_name='Administrador',
            last_name='Sistema',
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Criar usuário de teste
        test_user = User(
            username='teste',
            email='teste@enem.com',
            first_name='Usuário',
            last_name='Teste',
            is_admin=False,
            is_active=True
        )
        test_user.set_password('teste123')
        db.session.add(test_user)
        
        # Criar áreas de conhecimento
        areas = {
            'linguagens': 'Linguagens, Códigos e suas Tecnologias',
            'humanas': 'Ciências Humanas e suas Tecnologias',
            'natureza': 'Ciências da Natureza e suas Tecnologias',
            'matematica': 'Matemática e suas Tecnologias'
        }
        
        subjects_data = {
            'linguagens': [
                {'name': 'Língua Portuguesa', 'description': 'Gramática, Literatura e Interpretação de Texto'},
                {'name': 'Língua Estrangeira', 'description': 'Inglês ou Espanhol'},
                {'name': 'Arte', 'description': 'História da Arte e Movimentos Artísticos'},
                {'name': 'Educação Física', 'description': 'Esportes e Atividades Físicas'},
                {'name': 'Tecnologias da Informação', 'description': 'Informática e Redes Sociais'}
            ],
            'humanas': [
                {'name': 'História', 'description': 'História Geral e do Brasil'},
                {'name': 'Geografia', 'description': 'Geografia Geral e do Brasil'},
                {'name': 'Filosofia', 'description': 'Filosofia Antiga e Contemporânea'},
                {'name': 'Sociologia', 'description': 'Sociologia e Antropologia'}
            ],
            'natureza': [
                {'name': 'Biologia', 'description': 'Biologia Celular e Evolução'},
                {'name': 'Física', 'description': 'Mecânica, Termologia e Eletricidade'},
                {'name': 'Química', 'description': 'Química Geral e Orgânica'}
            ],
            'matematica': [
                {'name': 'Matemática', 'description': 'Álgebra, Geometria e Trigonometria'}
            ]
        }
        
        subjects = {}
        for area_key, area_name in areas.items():
            for subject_info in subjects_data[area_key]:
                subject = Subject(
                    name=subject_info['name'],
                    area=area_name,
                    description=subject_info['description']
                )
                db.session.add(subject)
                db.session.flush()  # Para obter o ID
                subjects[subject_info['name']] = subject
        
        # Criar tópicos para cada matéria
        topics_data = {
            'Língua Portuguesa': [
                'Gramática Normativa', 'Interpretação de Texto', 'Literatura Brasileira',
                'Literatura Portuguesa', 'Produção Textual', 'Figuras de Linguagem'
            ],
            'História': [
                'História Antiga', 'História Medieval', 'História Moderna',
                'História Contemporânea', 'História do Brasil', 'História da América'
            ],
            'Geografia': [
                'Geografia Física', 'Geografia Humana', 'Geografia Econômica',
                'Geografia Política', 'Geografia do Brasil', 'Geografia Mundial'
            ],
            'Matemática': [
                'Álgebra', 'Geometria Plana', 'Geometria Espacial', 'Trigonometria',
                'Funções', 'Estatística', 'Probabilidade'
            ],
            'Biologia': [
                'Biologia Celular', 'Genética', 'Evolução', 'Ecologia',
                'Fisiologia Humana', 'Botânica', 'Zoologia'
            ],
            'Física': [
                'Mecânica', 'Termologia', 'Óptica', 'Eletricidade',
                'Magnetismo', 'Ondas', 'Física Moderna'
            ],
            'Química': [
                'Química Geral', 'Química Inorgânica', 'Química Orgânica',
                'Físico-Química', 'Química Ambiental', 'Bioquímica'
            ]
        }
        
        topics = {}
        for subject_name, topic_list in topics_data.items():
            if subject_name in subjects:
                subject = subjects[subject_name]
                for topic_name in topic_list:
                    topic = Topic(
                        name=topic_name,
                        subject_id=subject.id,
                        description=f'Conteúdo sobre {topic_name}'
                    )
                    db.session.add(topic)
                    db.session.flush()
                    topics[f"{subject_name} - {topic_name}"] = topic
        
        # Criar materiais de estudo
        study_materials = []
        for topic_key, topic in topics.items():
            material = StudyMaterial(
                title=f'Material de Estudo - {topic.name}',
                content=f'Conteúdo detalhado sobre {topic.name}. Este material inclui conceitos fundamentais, exemplos práticos e exercícios resolvidos.',
                topic_id=topic.id,
                subject_id=topic.subject_id,
                material_type='text',
                difficulty_level=2,
                estimated_time=30
            )
            db.session.add(material)
            study_materials.append(material)
        
        # Criar questões de exemplo
        questions_data = [
            {
                'question': 'Qual é a função sintática da palavra "rapidamente" na frase "Ele correu rapidamente"?',
                'options': ['Sujeito', 'Predicado', 'Adjunto Adverbial', 'Complemento Nominal'],
                'correct_answer': 2,
                'explanation': 'A palavra "rapidamente" é um adjunto adverbial de modo, pois modifica o verbo "correu" indicando como a ação foi realizada.',
                'subject': 'Língua Portuguesa'
            },
            {
                'question': 'Em que ano o Brasil se tornou independente de Portugal?',
                'options': ['1808', '1822', '1889', '1891'],
                'correct_answer': 1,
                'explanation': 'O Brasil se tornou independente de Portugal em 7 de setembro de 1822, com o Grito do Ipiranga.',
                'subject': 'História'
            },
            {
                'question': 'Qual é a capital do Brasil?',
                'options': ['Rio de Janeiro', 'São Paulo', 'Brasília', 'Salvador'],
                'correct_answer': 2,
                'explanation': 'Brasília é a capital federal do Brasil desde 1960, quando foi inaugurada.',
                'subject': 'Geografia'
            },
            {
                'question': 'Qual é o resultado de 2x + 3 = 11?',
                'options': ['x = 3', 'x = 4', 'x = 5', 'x = 6'],
                'correct_answer': 1,
                'explanation': '2x + 3 = 11 → 2x = 11 - 3 → 2x = 8 → x = 4',
                'subject': 'Matemática'
            },
            {
                'question': 'Qual organela é responsável pela produção de energia na célula?',
                'options': ['Núcleo', 'Mitocôndria', 'Retículo Endoplasmático', 'Complexo de Golgi'],
                'correct_answer': 1,
                'explanation': 'A mitocôndria é a organela responsável pela produção de energia através da respiração celular.',
                'subject': 'Biologia'
            }
        ]
        
        for q_data in questions_data:
            if q_data['subject'] in subjects:
                # Encontrar um tópico da matéria para associar a questão
                subject = subjects[q_data['subject']]
                topic = Topic.query.filter_by(subject_id=subject.id).first()
                
                if topic:
                    question = Question(
                        question_text=q_data['question'],
                        question_type='multiple_choice',
                        difficulty_level=1,
                        topic_id=topic.id,
                        subject_id=subject.id
                    )
                    db.session.add(question)
                    db.session.flush()
                    
                    # Criar opções de resposta
                    for i, option_text in enumerate(q_data['options']):
                        answer = Answer(
                            answer_text=option_text,
                            question_id=question.id,
                            is_correct=(i == q_data['correct_answer']),
                            explanation=q_data['explanation'] if i == q_data['correct_answer'] else None
                        )
                        db.session.add(answer)
        
        # Commit das alterações
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"📊 Dados criados:")
        print(f"   - {User.query.count()} usuários")
        print(f"   - {Subject.query.count()} matérias")
        print(f"   - {Topic.query.count()} tópicos")
        print(f"   - {StudyMaterial.query.count()} materiais de estudo")
        print(f"   - {Question.query.count()} questões")
        print(f"   - {Answer.query.count()} respostas")

if __name__ == '__main__':
    init_database()
