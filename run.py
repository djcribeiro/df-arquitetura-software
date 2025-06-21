# /run.py
import os
from app import create_app

# Obtém a configuração do ambiente da variável de ambiente FLASK_ENV.
# Se não estiver definida, usa 'development' como padrão.
env_name = os.getenv('FLASK_ENV') or 'default'

# Cria a instância da aplicação Flask usando a factory 'create_app'
app = create_app(env_name)

if __name__ == '__main__':
    # Executa a aplicação.
    # As configurações de host e porta podem ser definidas aqui ou via variáveis de ambiente.
    app.run(host='127.0.0.1', port=5001)