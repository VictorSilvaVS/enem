#!/usr/bin/env python3
"""
Script simples para testar a inicialização do sistema
"""

from flask import Flask
from config import config

def create_test_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    
    # Testar se a configuração está funcionando
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
    print(f"DATABASE_URL: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    print("✅ Aplicação Flask criada com sucesso!")
