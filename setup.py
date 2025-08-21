#!/usr/bin/env python3
"""
Script de setup automatizado para o Sistema de Estudos ENEM
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        print(f"Comando: {command}")
        print(f"Erro: {e.stderr}")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def create_virtual_environment():
    """Cria ambiente virtual"""
    if os.path.exists("venv"):
        print("✅ Ambiente virtual já existe!")
        return True
    
    return run_command("python -m venv venv", "Criando ambiente virtual")

def activate_virtual_environment():
    """Ativa o ambiente virtual"""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"🔄 Ativando ambiente virtual...")
    print(f"Execute: {activate_script}")
    return True

def install_dependencies():
    """Instala as dependências"""
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependências")

def create_env_file():
    """Cria arquivo .env se não existir"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ Arquivo .env já existe!")
        return True
    
    print("📝 Criando arquivo .env...")
    env_content = """# Configurações do Sistema ENEM
SECRET_KEY=dev-secret-key-change-this-in-production
DATABASE_URL=sqlite:///enem_study_system.db
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        "app/assets/uploads",
        "app/assets/css",
        "app/assets/js",
        "logs"
    ]
    
    print("📁 Criando diretórios necessários...")
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Diretório {directory} criado/verificado")
        except Exception as e:
            print(f"❌ Erro ao criar diretório {directory}: {e}")
            return False
    return True

def populate_database():
    """Popula o banco de dados"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} populate_db.py", "Populando banco de dados")

def show_next_steps():
    """Mostra os próximos passos"""
    print("\n" + "="*60)
    print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
    print("="*60)
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Ative o ambiente virtual:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Execute o sistema:")
    print("   python main.py")
    
    print("\n3. Acesse no navegador:")
    print("   http://localhost:5000")
    
    print("\n👤 CREDENCIAIS DE ACESSO:")
    print("   Admin: admin / admin123")
    print("   Teste: teste / teste123")
    
    print("\n🔧 CONFIGURAÇÕES IMPORTANTES:")
    print("   - Altere a SECRET_KEY no arquivo .env para produção")
    print("   - Configure HTTPS para ambiente de produção")
    print("   - Use um banco de dados robusto (PostgreSQL) para produção")
    
    print("\n📚 DOCUMENTAÇÃO:")
    print("   Consulte o README.md para mais informações")
    
    print("\n" + "="*60)

def main():
    """Função principal do setup"""
    print("🚀 INICIANDO SETUP DO SISTEMA DE ESTUDOS ENEM")
    print("="*60)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Criar ambiente virtual
    if not create_virtual_environment():
        return False
    
    # Criar diretórios
    if not create_directories():
        return False
    
    # Criar arquivo .env
    if not create_env_file():
        return False
    
    # Instalar dependências
    if not install_dependencies():
        return False
    
    # Popular banco de dados
    if not populate_database():
        return False
    
    # Mostrar próximos passos
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup falhou! Verifique os erros acima.")
        sys.exit(1)
    else:
        print("\n✅ Setup concluído com sucesso!")
