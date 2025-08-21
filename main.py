import os
from flask import Flask
from config import config
from app.structure.database import init_app as init_db
from app.structure.auth.auth_manager import init_auth
from app.structure.routes.auth_routes import auth
from app.structure.routes.main_routes import main

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='app/assets/templates', 
                static_folder='app/assets')
    
    # Configuração
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    init_db(app)
    init_auth(app)
    
    # Registrar blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    
    # Criar diretórios necessários
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)