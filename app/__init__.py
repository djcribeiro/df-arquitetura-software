# /app/__init__.py
from flask import Flask
from config import config_by_name


def create_app(config_name: str) -> Flask:
    """
    Application Factory: Cria e configura a instância da aplicação Flask.
    """
    app = Flask(__name__)

    # Carrega as configurações do objeto de configuração correspondente ao ambiente.
    app.config.from_object(config_by_name[config_name])

    # Importa e regista os blueprints (nossos controladores)
    from .controllers.auth_controller import auth_api as auth_blueprint
    from .controllers.product_controller import product_api as product_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(product_blueprint, url_prefix='/produtos')

    # Adiciona uma rota raiz para verificar o status da API
    @app.route("/")
    def index():
        return "API de Parceiros está online!"

    return app