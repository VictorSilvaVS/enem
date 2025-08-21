#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais do sistema ENEM
"""

from main import create_app
from app.structure.database import db
from app.structure.database.models import (
    User, Subject, Topic, StudyMaterial, Question, Answer
)
from app.structure.auth.auth_manager import create_user
from datetime import datetime

def populate_database():
    app = create_app()
    
    with app.app_context():
        # Inicializar banco de dados
        db.create_all()
        
        # Limpar dados existentes
        print("Limpando dados existentes...")
        Answer.query.delete()
        Question.query.delete()
        StudyMaterial.query.delete()
        Topic.query.delete()
        Subject.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Criar usuário administrador
        print("Criando usuário administrador...")
        try:
            admin_user = create_user(
                username='admin',
                email='admin@enem.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                is_admin=True
            )
            print(f"Usuário admin criado: {admin_user.username}")
        except ValueError as e:
            print(f"Erro ao criar admin: {e}")
        
        # Criar usuário de teste
        print("Criando usuário de teste...")
        try:
            test_user = create_user(
                username='teste',
                email='teste@enem.com',
                password='teste123',
                first_name='Usuário',
                last_name='Teste'
            )
            print(f"Usuário teste criado: {test_user.username}")
        except ValueError as e:
            print(f"Erro ao criar usuário teste: {e}")
        
        # Criar disciplinas
        print("Criando disciplinas...")
        subjects_data = [
            {
                'name': 'Português',
                'description': 'Língua Portuguesa e Literatura',
                'area': 'Linguagens',
                'color': '#3498db',
                'icon': 'language'
            },
            {
                'name': 'Matemática',
                'description': 'Matemática e suas tecnologias',
                'area': 'Matemática',
                'color': '#27ae60',
                'icon': 'calculator'
            },
            {
                'name': 'História',
                'description': 'História e suas tecnologias',
                'area': 'Ciências Humanas',
                'color': '#f39c12',
                'icon': 'landmark'
            },
            {
                'name': 'Geografia',
                'description': 'Geografia e suas tecnologias',
                'area': 'Ciências Humanas',
                'color': '#e67e22',
                'icon': 'globe'
            },
            {
                'name': 'Filosofia',
                'description': 'Filosofia e suas tecnologias',
                'area': 'Ciências Humanas',
                'color': '#9b59b6',
                'icon': 'brain'
            },
            {
                'name': 'Sociologia',
                'description': 'Sociologia e suas tecnologias',
                'area': 'Ciências Humanas',
                'color': '#34495e',
                'icon': 'users'
            },
            {
                'name': 'Física',
                'description': 'Física e suas tecnologias',
                'area': 'Ciências da Natureza',
                'color': '#e74c3c',
                'icon': 'atom'
            },
            {
                'name': 'Química',
                'description': 'Química e suas tecnologias',
                'area': 'Ciências da Natureza',
                'color': '#1abc9c',
                'icon': 'flask'
            },
            {
                'name': 'Biologia',
                'description': 'Biologia e suas tecnologias',
                'area': 'Ciências da Natureza',
                'color': '#2ecc71',
                'icon': 'dna'
            }
        ]
        
        subjects = {}
        for subject_data in subjects_data:
            subject = Subject(**subject_data)
            db.session.add(subject)
            db.session.flush()  # Para obter o ID
            subjects[subject.name] = subject
            print(f"Disciplina criada: {subject.name}")
        
        # Criar tópicos para cada disciplina
        print("Criando tópicos...")
        topics_data = {
            'Português': [
                {'name': 'Gramática', 'description': 'Regras gramaticais e estrutura da língua', 'difficulty_level': 2},
                {'name': 'Interpretação de Texto', 'description': 'Compreensão e análise textual', 'difficulty_level': 3},
                {'name': 'Literatura', 'description': 'Movimentos literários e obras importantes', 'difficulty_level': 3},
                {'name': 'Redação', 'description': 'Técnicas de produção textual', 'difficulty_level': 4}
            ],
            'Matemática': [
                {'name': 'Álgebra', 'description': 'Equações, inequações e funções', 'difficulty_level': 3},
                {'name': 'Geometria', 'description': 'Geometria plana e espacial', 'difficulty_level': 3},
                {'name': 'Trigonometria', 'description': 'Funções trigonométricas', 'difficulty_level': 4},
                {'name': 'Estatística', 'description': 'Análise de dados e probabilidade', 'difficulty_level': 2}
            ],
            'História': [
                {'name': 'História do Brasil', 'description': 'História brasileira desde a colonização', 'difficulty_level': 3},
                {'name': 'História Geral', 'description': 'História mundial e civilizações', 'difficulty_level': 3},
                {'name': 'História Contemporânea', 'description': 'História recente e atualidades', 'difficulty_level': 2}
            ],
            'Geografia': [
                {'name': 'Geografia Física', 'description': 'Clima, relevo e vegetação', 'difficulty_level': 2},
                {'name': 'Geografia Humana', 'description': 'População, urbanização e economia', 'difficulty_level': 3},
                {'name': 'Geografia do Brasil', 'description': 'Características geográficas do Brasil', 'difficulty_level': 2}
            ],
            'Física': [
                {'name': 'Mecânica', 'description': 'Movimento, forças e energia', 'difficulty_level': 4},
                {'name': 'Termodinâmica', 'description': 'Calor, temperatura e gases', 'difficulty_level': 3},
                {'name': 'Eletricidade', 'description': 'Circuitos elétricos e magnetismo', 'difficulty_level': 4},
                {'name': 'Ondas', 'description': 'Ondas mecânicas e eletromagnéticas', 'difficulty_level': 3}
            ],
            'Química': [
                {'name': 'Química Geral', 'description': 'Estrutura atômica e ligações', 'difficulty_level': 3},
                {'name': 'Química Orgânica', 'description': 'Compostos orgânicos e reações', 'difficulty_level': 4},
                {'name': 'Química Inorgânica', 'description': 'Compostos inorgânicos', 'difficulty_level': 3},
                {'name': 'Físico-Química', 'description': 'Cinética e equilíbrio químico', 'difficulty_level': 4}
            ],
            'Biologia': [
                {'name': 'Citologia', 'description': 'Estrutura e função celular', 'difficulty_level': 3},
                {'name': 'Genética', 'description': 'Hereditariedade e evolução', 'difficulty_level': 4},
                {'name': 'Ecologia', 'description': 'Relações ecológicas e meio ambiente', 'difficulty_level': 2},
                {'name': 'Fisiologia', 'description': 'Sistemas do corpo humano', 'difficulty_level': 3}
            ]
        }
        
        topics = {}
        for subject_name, topic_list in topics_data.items():
            if subject_name in subjects:
                for topic_data in topic_list:
                    topic_data['subject_id'] = subjects[subject_name].id
                    topic = Topic(**topic_data)
                    db.session.add(topic)
                    db.session.flush()
                    topics[f"{subject_name}_{topic.name}"] = topic
                    print(f"Tópico criado: {subject_name} - {topic.name}")
        
        # Criar materiais de estudo
        print("Criando materiais de estudo...")
        materials_data = [
            {
                'subject': 'Português',
                'topic': 'Gramática',
                'title': 'Classes Gramaticais',
                'content': '''
                <h3>Classes Gramaticais</h3>
                <p>As classes gramaticais são categorias que organizam as palavras da língua portuguesa de acordo com suas características morfológicas e sintáticas.</p>
                
                <h4>1. Substantivo</h4>
                <p>Palavra que nomeia seres, objetos, lugares, sentimentos, etc.</p>
                <ul>
                    <li><strong>Concreto:</strong> casa, carro, pessoa</li>
                    <li><strong>Abstrato:</strong> amor, felicidade, justiça</li>
                    <li><strong>Próprio:</strong> João, Brasil, São Paulo</li>
                    <li><strong>Comum:</strong> cidade, país, rio</li>
                </ul>
                
                <h4>2. Adjetivo</h4>
                <p>Palavra que caracteriza o substantivo, indicando qualidades, estados, etc.</p>
                <ul>
                    <li><strong>Simples:</strong> bonito, grande, feliz</li>
                    <li><strong>Composto:</strong> azul-marinho, verde-limão</li>
                </ul>
                
                <h4>3. Verbo</h4>
                <p>Palavra que expressa ação, estado ou fenômeno.</p>
                <ul>
                    <li><strong>Transitivo:</strong> precisa de complemento</li>
                    <li><strong>Intransitivo:</strong> não precisa de complemento</li>
                    <li><strong>Ligação:</strong> ser, estar, parecer</li>
                </ul>
                ''',
                'material_type': 'text',
                'difficulty_level': 2,
                'estimated_time': 20
            },
            {
                'subject': 'Matemática',
                'topic': 'Álgebra',
                'title': 'Equações do 1º Grau',
                'content': '''
                <h3>Equações do 1º Grau</h3>
                <p>Uma equação do primeiro grau é uma igualdade que contém uma ou mais incógnitas elevadas à potência 1.</p>
                
                <h4>Forma Geral</h4>
                <p>ax + b = 0, onde a ≠ 0</p>
                
                <h4>Resolução</h4>
                <p>Para resolver uma equação do 1º grau, seguimos estes passos:</p>
                <ol>
                    <li>Isolar a incógnita (x) em um dos membros</li>
                    <li>Passar todos os termos que não contêm x para o outro membro</li>
                    <li>Realizar as operações necessárias</li>
                    <li>Encontrar o valor de x</li>
                </ol>
                
                <h4>Exemplo</h4>
                <p>Resolva a equação: 3x + 5 = 17</p>
                <p><strong>Solução:</strong></p>
                <p>3x + 5 = 17</p>
                <p>3x = 17 - 5</p>
                <p>3x = 12</p>
                <p>x = 12/3</p>
                <p>x = 4</p>
                
                <h4>Verificação</h4>
                <p>3(4) + 5 = 17</p>
                <p>12 + 5 = 17</p>
                <p>17 = 17 ✓</p>
                ''',
                'material_type': 'text',
                'difficulty_level': 2,
                'estimated_time': 25
            },
            {
                'subject': 'História',
                'topic': 'História do Brasil',
                'title': 'Período Colonial',
                'content': '''
                <h3>Período Colonial Brasileiro (1500-1822)</h3>
                <p>O período colonial brasileiro foi marcado pela exploração dos recursos naturais e pela formação da sociedade brasileira.</p>
                
                <h4>Principais Características</h4>
                <ul>
                    <li><strong>Exploração:</strong> Baseada na extração de recursos naturais</li>
                    <li><strong>Monocultura:</strong> Produção de um único produto (açúcar, ouro)</li>
                    <li><strong>Escravidão:</strong> Mão de obra escrava africana</li>
                    <li><strong>Pacto Colonial:</strong> Brasil só podia comercializar com Portugal</li>
                </ul>
                
                <h4>Ciclos Econômicos</h4>
                <ol>
                    <li><strong>Ciclo do Pau-Brasil (1500-1530):</strong> Extração de madeira</li>
                    <li><strong>Ciclo da Cana-de-Açúcar (1530-1700):</strong> Plantation no Nordeste</li>
                    <li><strong>Ciclo do Ouro (1700-1800):</strong> Mineração em Minas Gerais</li>
                </ol>
                
                <h4>Sociedade Colonial</h4>
                <p>A sociedade era dividida em:</p>
                <ul>
                    <li><strong>Elite:</strong> Proprietários rurais e comerciantes</li>
                    <li><strong>Classe Média:</strong> Funcionários públicos e profissionais liberais</li>
                    <li><strong>Escravos:</strong> Trabalhadores sem direitos</li>
                </ul>
                ''',
                'material_type': 'text',
                'difficulty_level': 2,
                'estimated_time': 30
            }
        ]
        
        for material_data in materials_data:
            subject_name = material_data.pop('subject')
            topic_name = material_data.pop('topic')
            topic_key = f"{subject_name}_{topic_name}"
            
            if topic_key in topics:
                material_data['subject_id'] = topics[topic_key].subject_id
                material_data['topic_id'] = topics[topic_key].id
                material = StudyMaterial(**material_data)
                db.session.add(material)
                print(f"Material criado: {material.title}")
        
        # Criar algumas questões de exemplo
        print("Criando questões de exemplo...")
        questions_data = [
            {
                'subject': 'Português',
                'topic': 'Gramática',
                'question_text': 'Qual das palavras abaixo é um substantivo abstrato?',
                'question_type': 'multiple_choice',
                'difficulty_level': 2,
                'answers': [
                    {'answer_text': 'casa', 'is_correct': False},
                    {'answer_text': 'amor', 'is_correct': True},
                    {'answer_text': 'carro', 'is_correct': False},
                    {'answer_text': 'livro', 'is_correct': False}
                ]
            },
            {
                'subject': 'Matemática',
                'topic': 'Álgebra',
                'question_text': 'Qual é a solução da equação 2x + 3 = 11?',
                'question_type': 'multiple_choice',
                'difficulty_level': 2,
                'answers': [
                    {'answer_text': 'x = 3', 'is_correct': False},
                    {'answer_text': 'x = 4', 'is_correct': True},
                    {'answer_text': 'x = 5', 'is_correct': False},
                    {'answer_text': 'x = 6', 'is_correct': False}
                ]
            },
            {
                'subject': 'História',
                'topic': 'História do Brasil',
                'question_text': 'Qual foi o primeiro ciclo econômico do Brasil colonial?',
                'question_type': 'multiple_choice',
                'difficulty_level': 2,
                'answers': [
                    {'answer_text': 'Ciclo do Ouro', 'is_correct': False},
                    {'answer_text': 'Ciclo da Cana-de-Açúcar', 'is_correct': False},
                    {'answer_text': 'Ciclo do Pau-Brasil', 'is_correct': True},
                    {'answer_text': 'Ciclo do Café', 'is_correct': False}
                ]
            }
        ]
        
        for question_data in questions_data:
            subject_name = question_data.pop('subject')
            topic_name = question_data.pop('topic')
            answers_data = question_data.pop('answers')
            
            topic_key = f"{subject_name}_{topic_name}"
            if topic_key in topics:
                question_data['subject_id'] = topics[topic_key].subject_id
                question_data['topic_id'] = topics[topic_key].id
                
                question = Question(**question_data)
                db.session.add(question)
                db.session.flush()
                
                for answer_data in answers_data:
                    answer_data['question_id'] = question.id
                    answer = Answer(**answer_data)
                    db.session.add(answer)
                
                print(f"Questão criada: {question.question_text[:50]}...")
        
        # Commit final
        db.session.commit()
        print("\n✅ Banco de dados populado com sucesso!")
        print("\nCredenciais de acesso:")
        print("👤 Admin: admin / admin123")
        print("👤 Teste: teste / teste123")

if __name__ == '__main__':
    populate_database()
