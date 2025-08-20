import json
import os

# Always use absolute paths relative to this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE_DIR, "stock.json")
SUPPLIERS_FILE = os.path.join(BASE_DIR, "suppliers.json")
SALES_FILE = os.path.join(BASE_DIR, "sales.json")
CASH_FILE = os.path.join(BASE_DIR, "cash.json")   # to track real cash


# ---------------- HELPER FUNCTIONS ----------------
def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


# ---------------- CASH MANAGEMENT ----------------
def get_cash_in_hand():
    """Read cash balance safely from cash.json"""
    if not os.path.exists(CASH_FILE):
        return 0.0
    try:
        with open(CASH_FILE, "r") as f:
            data = json.load(f)
            return data.get("cash_in_hand", 0.0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0.0

def update_cash(amount):
    """Increase (positive) or decrease (negative) cash balance safely"""
    current_cash = get_cash_in_hand()
    cash = {"cash_in_hand": current_cash + amount}
    with open(CASH_FILE, "w") as f:
        json.dump(cash, f, indent=4)

    # ✅ Debug print
    print(f"💰 Cash updated! Old: {current_cash}, Added: {amount}, New: {cash['cash_in_hand']}")

def get_total_sales():
    """Return total revenue from sales.json"""
    sales = load_json(SALES_FILE)
    return sum(sale.get("total", 0) for sale in sales)

def view_cash_status():
    """Show both total revenue and actual available cash"""
    total_sales = get_total_sales()
    cash_in_hand = get_cash_in_hand()
    print("\n--- Cash Status ---")
    print(f"Total Sales (Revenue generated): ₹{total_sales}")
    print(f"Cash in Hand (Available now): ₹{cash_in_hand}")
    print("--------------------\n")


# ---------------- SUPPLIER MANAGEMENT ----------------
def request_stock_from_supplier():
    suppliers = load_json(SUPPLIERS_FILE)
    stock = load_json(STOCK_FILE)

    if not suppliers:
        print("No suppliers found. Please add suppliers first.")
        return

    print("\n--- Suppliers ---")
    for s in suppliers:
        print(f"{s['id']}. {s['name']} | Contact: {s['contact']} | Payment Due: ₹{s['payment_due']}")

    try:
        supplier_id = int(input("\nEnter supplier ID to request stock from: "))
    except ValueError:
        print("Invalid ID.")
        return

    supplier = next((s for s in suppliers if s["id"] == supplier_id), None)
    if not supplier:
        print("Supplier not found!")
        return

    try:
        product_id = int(input("Enter product ID to restock: "))
        quantity = int(input("Enter quantity to add: "))
        price_per_unit = float(input("Enter price per unit from supplier: "))
    except ValueError:
        print("Invalid input. Please enter correct numbers.")
        return

    # Update stock
    existing_product = next((p for p in stock if p["id"] == product_id), None)
    if existing_product:
        existing_product["quantity"] += quantity
        existing_product["price"] = price_per_unit  # purchase price
    else:
        stock.append({
            "id": product_id,
            "name": input("Enter the product name: "),
            "price": price_per_unit,  # purchase price
            "quantity": quantity,
            "min_stock": 15
        })

    save_json(STOCK_FILE, stock)

    # Update supplier's payment due
    total_cost = quantity * price_per_unit
    supplier["payment_due"] += total_cost
    save_json(SUPPLIERS_FILE, suppliers)

    print(f"✅ Stock updated! Payment due to {supplier['name']} is now ₹{supplier['payment_due']}.")


def pay_supplier():
    suppliers = load_json(SUPPLIERS_FILE)

    if not suppliers:
        print("No suppliers found.")
        return

    print("\n--- Suppliers ---")
    for s in suppliers:
        print(f"{s['id']}. {s['name']} | Payment Due: ₹{s['payment_due']}")

    try:
        supplier_id = int(input("\nEnter supplier ID to pay: "))
    except ValueError:
        print("Invalid ID.")
        return

    supplier = next((s for s in suppliers if s["id"] == supplier_id), None)
    if not supplier:
        print("Supplier not found!")
        return

    # Check available cash
    available_cash = get_cash_in_hand()
    print(f"Cash available: ₹{available_cash}")

    try:
        amount = float(input("Enter amount to pay: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount > available_cash:
        print(f"❌ Payment failed! Not enough cash. You only have ₹{available_cash}.")
        return

    if amount > supplier["payment_due"]:
        print("Amount exceeds payment due. Paying full amount instead.")
        amount = supplier["payment_due"]

    # Deduct from supplier due & cash
    supplier["payment_due"] -= amount
    update_cash(-amount)

    save_json(SUPPLIERS_FILE, suppliers)

    # ✅ Show updated balances
    remaining_cash = get_cash_in_hand()
    print(f"💰 Paid ₹{amount} to {supplier['name']}. Remaining due: ₹{supplier['payment_due']}")
    print(f"🏦 Remaining Cash Balance: ₹{remaining_cash}")
