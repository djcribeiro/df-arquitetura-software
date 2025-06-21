# /app/repositories/product_repository.py
import threading

_db_data = {"products": {}}
_db_lock = threading.Lock()
_next_product_id = 1


class ProductRepository:
    def find_all(self):
        with _db_lock:
            return list(_db_data["products"].values())

    def find_by_id(self, product_id):
        with _db_lock:
            return _db_data["products"].get(product_id)

    def find_by_name(self, name):
        with _db_lock:
            return [p for p in _db_data["products"].values() if name.lower() in p["name"].lower()]

    def save(self, product_data):
        global _next_product_id
        with _db_lock:
            new_id = _next_product_id
            product_data["id"] = new_id
            _db_data["products"][new_id] = product_data
            _next_product_id += 1
            return product_data

    def update(self, product_id, product_data):
        with _db_lock:
            if product_id in _db_data["products"]:
                _db_data["products"][product_id].update(product_data)
                return _db_data["products"][product_id]
            return None

    def delete(self, product_id):
        with _db_lock:
            if product_id in _db_data["products"]:
                del _db_data["products"][product_id]
                return True
            return False

    def count(self):
        with _db_lock:
            return len(_db_data["products"])

    def clear(self):
        global _next_product_id
        with _db_lock:
            _db_data["products"].clear()
            _next_product_id = 1
