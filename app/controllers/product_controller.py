# /app/controllers/product_controller.py
from flask import request, Blueprint
from http import HTTPStatus
from ..services.product_service import ProductService
from ..utils.security import token_required
from ..utils.responses import success_response, bad_request_error, not_found_error

product_api = Blueprint('product_api', __name__)
product_service = ProductService()


@product_api.route("", methods=['GET'])
@token_required
def get_all_products():
    """Retorna uma lista de todos os produtos."""
    products = product_service.get_all_products()
    return success_response(products)


@product_api.route("", methods=['POST'])
@token_required
def create_product():
    """Cria um novo produto."""
    new_prod, error_message = product_service.create_product(request.json)
    if error_message:
        return bad_request_error(error_message)
    return success_response(new_prod, HTTPStatus.CREATED)


@product_api.route("/<int:pid>", methods=['GET'])
@token_required
def get_product_by_id(pid):
    """Busca um produto específico pelo seu ID."""
    prod = product_service.get_product_by_id(pid)
    if not prod:
        return not_found_error("Produto")
    return success_response(prod)


@product_api.route("/<int:pid>", methods=['PUT', 'PATCH'])
@token_required
def update_product(pid):
    """Atualiza um produto existente."""
    updated_prod, error_message = product_service.update_product(pid, request.json)
    if error_message:
        return not_found_error("Produto")
    return success_response(updated_prod)


@product_api.route("/<int:pid>", methods=['DELETE'])
@token_required
def delete_product(pid):
    """Deleta um produto."""
    success, error_message = product_service.delete_product(pid)
    if error_message:
        return not_found_error("Produto")
    # Para DELETE, é comum retornar uma resposta de sucesso sem dados
    return success_response(status_code=HTTPStatus.NO_CONTENT)


@product_api.route("/count", methods=['GET'])
@token_required
def get_products_count():
    """Retorna a contagem total de produtos."""
    count = product_service.get_products_count()
    return success_response({"total_produtos": count})


@product_api.route("/search", methods=['GET'])
@token_required
def search_product_by_name():
    """Busca produtos por nome."""
    name = request.args.get("name")
    if not name:
        return bad_request_error("O parâmetro 'name' é obrigatório.")

    products = product_service.get_products_by_name(name)
    return success_response(products)
