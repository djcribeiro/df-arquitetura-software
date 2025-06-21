# /app/controllers/auth_controller.py
import jwt
from flask import request, Blueprint, current_app
from datetime import datetime, timedelta
from ..utils.responses import success_response, bad_request_error, unauthorized_error

auth_api = Blueprint('auth_api', __name__)

# Simulação de um banco de dados de parceiros autorizados
AUTHORIZED_PARTNERS = {
    "partner_123": {
        "secret": "super_secret_key_123",
        "permissions": ["read", "write"]
    }
}

@auth_api.route("/login", methods=["POST"])
def login():
    """Endpoint para autenticar um parceiro e retornar um token JWT."""
    auth_data = request.json
    if not auth_data or not auth_data.get('client_id') or not auth_data.get('client_secret'):
        return bad_request_error("Credenciais 'client_id' e 'client_secret' são necessárias.")

    client_id = auth_data['client_id']
    client_secret = auth_data['client_secret']

    partner = AUTHORIZED_PARTNERS.get(client_id)
    if not partner or partner['secret'] != client_secret:
        return unauthorized_error("Credenciais inválidas.")

    # Credenciais válidas, gerar o token
    secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode({
        'client_id': client_id,
        'exp': datetime.utcnow() + timedelta(hours=1) # Token expira em 1 hora
    }, secret_key, algorithm="HS256")

    return success_response({"token": token})
