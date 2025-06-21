# /app/utils/responses.py
from flask import jsonify
from http import HTTPStatus

def success_response(data=None, status_code=HTTPStatus.OK):
    """
    Cria uma resposta JSON de sucesso padronizada.
    Engloba os dados retornados em uma chave 'data'.
    """
    response_data = {
        "status": "success",
        "data": data
    }
    return jsonify(response_data), status_code

def error_response(message, status_code):
    """
    Cria uma resposta JSON de erro padronizada.
    """
    response_data = {
        "status": "error",
        "erro": {
            "message": message
        }
    }
    return jsonify(response_data), status_code

# Funções auxiliares para erros comuns
def not_found_error(resource="Recurso"):
    """Cria uma resposta para erro 404 Not Found."""
    return error_response(f"{resource} não encontrado.", HTTPStatus.NOT_FOUND)

def bad_request_error(message="Requisição inválida."):
    """Cria uma resposta para erro 400 Bad Request."""
    return error_response(message, HTTPStatus.BAD_REQUEST)

def unauthorized_error(message="Acesso não autorizado."):
    """Cria uma resposta para erro 401 Unauthorized."""
    return error_response(message, HTTPStatus.UNAUTHORIZED)

