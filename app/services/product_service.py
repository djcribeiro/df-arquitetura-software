# /app/services/product_service.py
from ..repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_all_products(self):
        return self.repository.find_all()

    def get_product_by_id(self, pid):
        return self.repository.find_by_id(pid)

    def get_products_by_name(self, name):
        return self.repository.find_by_name(name)

    def get_products_count(self):
        return self.repository.count()

    def create_product(self, data):
        if not data.get("name") or not data.get("price"):
            return None, "Nome e preço são obrigatórios."
        if data["price"] < 0:
            return None, "O preço do produto não pode ser negativo."
        return self.repository.save(data), None

    def update_product(self, pid, data):
        if not self.repository.find_by_id(pid):
            return None, f"Produto com ID {pid} não encontrado."
        return self.repository.update(pid, data), None

    def delete_product(self, pid):
        if not self.repository.delete(pid):
            return False, f"Produto com ID {pid} não encontrado."
        return True, None
