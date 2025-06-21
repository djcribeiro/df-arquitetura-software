# /config.py
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Configuração base que todas as outras herdam."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    TESTING = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuração para o ambiente de desenvolvimento."""
    DEBUG = True

class TestingConfig(Config):
    """Configuração para o ambiente de testes."""
    TESTING = True
    SECRET_KEY = 'test_secret_key' # Chave consistente para testes

class ProductionConfig(Config):
    """Configuração para o ambiente de produção."""
    # Em produção, a SECRET_KEY DEVE ser carregada do ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("Nenhuma SECRET_KEY definida para o ambiente de produção")

# Dicionário que mapeia os nomes dos ambientes para as classes de configuração.
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
