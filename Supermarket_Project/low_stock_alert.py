import json
import os

STOCK_FILE = "stock.json"
SUPPLIERS_FILE = "suppliers.json"

def load_json(file):
    """Load JSON data from file or return empty list."""
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

def check_low_stock():
    """Check stock and alert suppliers if quantity is below minimum."""
    stock = load_json(STOCK_FILE)
    suppliers = load_json(SUPPLIERS_FILE)

    for product in stock:
        if product["quantity"] < product["min_stock"]:
            print(f"Low stock alert for {product['name']} (Qty: {product['quantity']})")
            for supplier in suppliers:
                if product["id"] in supplier["products"]:  # fixed key name
                    send_message(supplier, product)

def send_message(supplier, product):
    """Simulated supplier alert (print only)."""
    message = f"Hello {supplier['name']}, please send more stock of {product['name']} (current qty: {product['quantity']})."
    print(f"Message sent to {supplier['contact']}: {message}")

