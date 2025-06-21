# /tests/test_product_endpoints.py
import pytest
from app import create_app
from app.repositories.product_repository import ProductRepository

# --- Fixtures de Teste ---

@pytest.fixture(scope='module')
def test_client():
    """Cria e configura um cliente de teste para a aplicação."""
    flask_app = create_app('testing')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(autouse=True)
def clean_db_before_each_test():
    """Garante que o 'banco de dados' esteja limpo antes de cada teste."""
    repo = ProductRepository()
    repo.clear()
    # Adiciona um produto base que pode ser usado por vários testes
    repo.save({'name': 'Produto Base de Teste', 'price': 10.0})

def get_auth_token(test_client):
    """Função auxiliar para obter um token de autenticação válido."""
    credentials = {"client_id": "partner_123", "client_secret": "super_secret_key_123"}
    response = test_client.post('/auth/login', json=credentials)
    return response.get_json()['data']['token']

# --- Testes de Autenticação ---

def test_login_success(test_client):
    """Verifica se o login com credenciais corretas retorna um token."""
    credentials = {"client_id": "partner_123", "client_secret": "super_secret_key_123"}
    response = test_client.post('/auth/login', json=credentials)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert 'token' in response_data['data']

def test_login_failure_invalid_credentials(test_client):
    """Verifica se o login com credenciais incorretas é rejeitado."""
    credentials = {"client_id": "partner_123", "client_secret": "wrong_secret"}
    response = test_client.post('/auth/login', json=credentials)
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data['status'] == 'error'
    assert "Credenciais inválidas" in response_data['erro']['message']

# --- Testes de Endpoints de Produtos ---

def test_access_protected_endpoint_without_token(test_client):
    """Verifica se um endpoint protegido não pode ser acessado sem um token."""
    response = test_client.get('/produtos')
    assert response.status_code == 401
    response_data = response.get_json()
    assert "Token de autenticação ausente" in response_data['erro']['message']

def test_get_all_products(test_client):
    """Testa a listagem de todos os produtos com um token válido."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get('/produtos', headers=headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert isinstance(response_data['data'], list)
    assert len(response_data['data']) == 1 # Apenas o produto base criado na fixture

def test_create_product(test_client):
    """Testa a criação de um novo produto."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    product_data = {'name': 'Novo Produto Criado', 'price': 150.75, 'description': 'Descrição do novo produto'}
    response = test_client.post('/produtos', json=product_data, headers=headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert response_data['data']['name'] == 'Novo Produto Criado'
    assert 'id' in response_data['data']

def test_get_product_by_id(test_client):
    """Testa a busca de um produto específico pelo ID."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    # O produto base terá ID 1
    response = test_client.get('/produtos/1', headers=headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert response_data['data']['id'] == 1
    assert response_data['data']['name'] == 'Produto Base de Teste'

def test_get_nonexistent_product(test_client):
    """Testa a busca por um ID de produto que não existe."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get('/produtos/999', headers=headers)
    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data['status'] == 'error'

def test_update_product(test_client):
    """Testa a atualização de um produto existente."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    update_data = {'price': 99.99}
    response = test_client.put('/produtos/1', json=update_data, headers=headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert response_data['data']['price'] == 99.99
    # Garante que o nome não foi alterado
    assert response_data['data']['name'] == 'Produto Base de Teste'

def test_delete_product(test_client):
    """Testa a exclusão de um produto."""
    token = get_auth_token(test_client)
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.delete('/produtos/1', headers=headers)
    assert response.status_code == 204
    # Verifica se o produto foi realmente deletado
    get_response = test_client.get('/produtos/1', headers=headers)
    assert get_response.status_code == 404
