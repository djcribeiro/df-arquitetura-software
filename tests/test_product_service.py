# /tests/test_product_service.py
import pytest
from unittest.mock import MagicMock
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository


# --- Fixtures de Teste ---

@pytest.fixture
def mock_product_repository():
    """Cria um 'mock' (simulação) do ProductRepository."""
    return MagicMock(spec=ProductRepository)


@pytest.fixture
def product_service(mock_product_repository):
    """Injeta o repositório mockado no serviço para testes unitários."""
    service = ProductService()
    service.repository = mock_product_repository
    return service


# --- Testes Unitários da Camada de Serviço ---

def test_create_product_success(product_service, mock_product_repository):
    """Testa a lógica de criação de produto com dados válidos."""
    product_data = {'name': 'Produto Válido', 'price': 50.0}
    # Configura o mock para retornar o próprio dado salvo
    mock_product_repository.save.return_value = {**product_data, 'id': 1}

    new_product, error = product_service.create_product(product_data)

    assert error is None
    assert new_product is not None
    assert new_product['name'] == 'Produto Válido'
    # Verifica se o método 'save' do repositório foi chamado uma vez
    mock_product_repository.save.assert_called_once_with(product_data)


def test_create_product_missing_name(product_service, mock_product_repository):
    """Testa a validação para criação de produto sem nome."""
    product_data = {'price': 50.0}

    new_product, error = product_service.create_product(product_data)

    assert new_product is None
    assert error == "Nome e preço são obrigatórios."
    # Garante que o repositório não foi chamado se a validação falhou
    mock_product_repository.save.assert_not_called()


def test_create_product_negative_price(product_service, mock_product_repository):
    """Testa a validação para criação de produto com preço negativo."""
    product_data = {'name': 'Produto Inválido', 'price': -10.0}

    new_product, error = product_service.create_product(product_data)

    assert new_product is None
    assert error == "O preço do produto não pode ser negativo."
    mock_product_repository.save.assert_not_called()


def test_get_product_by_id_found(product_service, mock_product_repository):
    """Testa a busca de um produto que existe."""
    mock_product = {'id': 1, 'name': 'Produto Encontrado', 'price': 100}
    # Configura o mock para retornar o produto quando find_by_id é chamado
    mock_product_repository.find_by_id.return_value = mock_product

    product = product_service.get_product_by_id(1)

    assert product is not None
    assert product['id'] == 1
    mock_product_repository.find_by_id.assert_called_once_with(1)


def test_get_product_by_id_not_found(product_service, mock_product_repository):
    """Testa a busca de um produto que não existe."""
    # Configura o mock para retornar None
    mock_product_repository.find_by_id.return_value = None

    product = product_service.get_product_by_id(99)

    assert product is None
    mock_product_repository.find_by_id.assert_called_once_with(99)


def test_delete_product_failure(product_service, mock_product_repository):
    """Testa a lógica de deleção para um produto que não existe."""
    # Configura o mock do repositório para simular uma falha na deleção
    mock_product_repository.delete.return_value = False

    success, error = product_service.delete_product(99)

    assert not success
    assert error == "Produto com ID 99 não encontrado."
    mock_product_repository.delete.assert_called_once_with(99)
