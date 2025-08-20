import json
import os

SALES_FILE = "sales.json"
SUPPLIERS_FILE = "suppliers.json"
CASH_FILE = "cash.json"

def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

def get_cash_in_hand():
    """Read real available cash from cash.json"""
    if not os.path.exists(CASH_FILE):
        return 0.0
    try:
        with open(CASH_FILE, "r") as f:
            data = json.load(f)
            return data.get("cash_in_hand", 0.0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0.0

def view_sales_report():
    if not os.path.exists(SALES_FILE):
        print("No sales data found.")
        return

    sales = load_json(SALES_FILE)
    if not sales:
        print("No sales have been made yet.\n")
        return

    total_sales = 0
    total_profit = 0

    print("\n---Sales Report---")
    for i, sale in enumerate(sales, 1):
        print(f"\nSale #{i} | Date: {sale['date']}")
        for item in sale['items']:
            print(f" - {item['name']} x {item['quantity']} = ₹{item['subtotal']} (Profit: ₹{item.get('profit', 0)})")
        print(f" Sale Total: ₹{sale['total']}")
        print(f" Sale Profit: ₹{sale.get('total_profit', 0)}")
        total_sales += sale['total']
        total_profit += sale.get('total_profit', 0)

    suppliers = load_json(SUPPLIERS_FILE)
    total_due = sum(s["payment_due"] for s in suppliers)

    # Get actual available balance
    cash_in_hand = get_cash_in_hand()

    print("\n------------------------------")
    print(f"Total Sales Value (Revenue generated): ₹{total_sales}")
    print(f"Total Profit: ₹{total_profit}")
    print(f"Cash in Hand (Real money you have): ₹{cash_in_hand}")
    print(f"Total Supplier Payments Due: ₹{total_due}")
    print(f"Net Cash after Paying Suppliers: ₹{cash_in_hand - total_due}")
    print("------------------------------\n")
