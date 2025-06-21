# /app/utils/security.py
import jwt
from functools import wraps
from flask import request, g, current_app
from .responses import unauthorized_error, bad_request_error

def token_required(f):
    """Decorator para validar o token JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Extrai o token do formato "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return bad_request_error("Cabeçalho de autorização malformado.")

        if not token:
            return unauthorized_error("Token de autenticação ausente.")

        try:
            secret_key = current_app.config['SECRET_KEY']
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            # Armazena os dados do usuário no contexto da requisição
            g.current_user = data
        except jwt.ExpiredSignatureError:
            return unauthorized_error("Token expirado.")
        except jwt.InvalidTokenError:
            return unauthorized_error("Token inválido.")

        return f(*args, **kwargs)
    return decorated
