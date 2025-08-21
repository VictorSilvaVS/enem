# Sistema de Estudos ENEM

Um sistema completo e profissional para auxílio nos estudos do Exame Nacional do Ensino Médio (ENEM), desenvolvido com Flask e arquitetura modular.

## 🚀 Características

- **Sistema de Autenticação Seguro**: Login, registro e gerenciamento de contas
- **Materiais Organizados**: Conteúdo estruturado por disciplinas e tópicos
- **Sistema de Progresso**: Acompanhamento detalhado do desenvolvimento
- **Quizzes Interativos**: Testes com questões similares ao ENEM
- **Interface Moderna**: Design responsivo e intuitivo
- **Arquitetura Modular**: Fácil manutenção e expansão
- **Segurança Robusta**: Proteção contra vulnerabilidades comuns

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🛠️ Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd enem-study-system
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Crie um arquivo .env na raiz do projeto
   SECRET_KEY=sua-chave-secreta-super-segura
   DATABASE_URL=sqlite:///enem_study_system.db
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Popule o banco de dados**
   ```bash
   python populate_db.py
   ```

6. **Execute o sistema**
   ```bash
   python main.py
   ```

7. **Acesse o sistema**
   - Abra seu navegador e vá para `http://localhost:5000`
   - Use as credenciais padrão:
     - **Admin**: `admin` / `admin123`
     - **Usuário Teste**: `teste` / `teste123`

## 🏗️ Arquitetura do Sistema

```
enem-study-system/
├── main.py                 # Arquivo principal da aplicação
├── config.py              # Configurações do sistema
├── requirements.txt       # Dependências Python
├── populate_db.py         # Script para popular banco de dados
├── README.md             # Documentação
└── app/
    ├── assets/           # Arquivos estáticos (CSS, JS, templates)
    │   ├── templates/    # Templates HTML
    │   ├── css/         # Estilos CSS
    │   └── js/          # Scripts JavaScript
    └── structure/       # Estrutura modular
        ├── auth/        # Sistema de autenticação
        ├── database/    # Modelos e configuração do banco
        ├── forms/       # Formulários web
        ├── functions/   # Funções utilitárias
        ├── routes/      # Rotas da aplicação
        └── cryptography/ # Criptografia e segurança
```

## 🔐 Módulos de Segurança

### Autenticação
- Hash de senhas com bcrypt
- Tokens JWT para sessões
- Proteção contra ataques de força bruta
- Validação de formulários

### Autorização
- Controle de acesso baseado em roles
- Middleware de autenticação
- Proteção de rotas sensíveis

### Dados
- Validação de entrada
- Sanitização de dados
- Proteção contra SQL Injection
- CSRF Protection

## 📚 Funcionalidades

### Para Estudantes
- **Dashboard Personalizado**: Visão geral do progresso
- **Materiais de Estudo**: Conteúdo organizado por disciplina
- **Sistema de Progresso**: Acompanhamento detalhado
- **Quizzes**: Testes para verificar conhecimento
- **Busca**: Encontrar materiais rapidamente

### Para Administradores
- **Gestão de Usuários**: Criar, editar e gerenciar contas
- **Gestão de Conteúdo**: Adicionar materiais e questões
- **Estatísticas**: Relatórios de uso do sistema
- **Configurações**: Personalizar o sistema

## 🎨 Interface

- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Tema Moderno**: Interface limpa e profissional
- **Navegação Intuitiva**: Fácil de usar
- **Feedback Visual**: Notificações e indicadores de progresso

## 🔧 Configuração Avançada

### Banco de Dados
O sistema suporta diferentes bancos de dados:
- SQLite (padrão para desenvolvimento)
- PostgreSQL (recomendado para produção)
- MySQL

### Email
Configure o envio de emails para:
- Recuperação de senha
- Notificações
- Relatórios

### Produção
Para deploy em produção:
1. Configure HTTPS
2. Use um servidor WSGI (Gunicorn, uWSGI)
3. Configure um proxy reverso (Nginx)
4. Use variáveis de ambiente para configurações sensíveis

## 🚀 Deploy

### Heroku
```bash
# Crie um arquivo Procfile
web: gunicorn main:app

# Configure as variáveis de ambiente
heroku config:set SECRET_KEY=sua-chave-secreta
heroku config:set DATABASE_URL=sua-url-do-banco
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

## 🧪 Testes

```bash
# Execute os testes
python -m pytest tests/

# Cobertura de código
python -m pytest --cov=app tests/
```

## 📊 Monitoramento

O sistema inclui:
- Logs estruturados
- Métricas de performance
- Monitoramento de erros
- Relatórios de uso

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- **Documentação**: Consulte este README
- **Issues**: Abra uma issue no GitHub
- **Email**: contato@enem-system.com

## 🔄 Atualizações

Para atualizar o sistema:
```bash
git pull origin main
pip install -r requirements.txt
python populate_db.py  # Se houver mudanças no banco
```

## 📈 Roadmap

- [ ] Sistema de notificações
- [ ] App mobile
- [ ] Integração com APIs externas
- [ ] Sistema de gamificação
- [ ] Análise avançada de progresso
- [ ] Suporte a múltiplos idiomas

---

**Desenvolvido com ❤️ para ajudar estudantes a se prepararem para o ENEM**
