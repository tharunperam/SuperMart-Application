import json
import os
from datetime import datetime
from low_stock_alert import check_low_stock
from supplier_manager import update_cash, get_cash_in_hand

STOCK_FILE = "stock.json"
SALES_FILE = "sales.json"
PROFIT_PERCENT = 20 # Profit amount is 20%

def load_stock():
    if not os.path.exists(STOCK_FILE):
        return []
    with open(STOCK_FILE, 'r') as file:
        return json.load(file)

def save_stock(stock):
    with open(STOCK_FILE, 'w') as file:
        json.dump(stock, file, indent=4)

def save_sale(sale):
    sales = []
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'r') as file:
            try:
                sales = json.load(file)
            except json.JSONDecodeError:
                sales = []

    sales.append(sale)
    with open(SALES_FILE, 'w') as file:
        json.dump(sales, file, indent=4)

def generate_bill():
    stock = load_stock()
    cart = []
    total = 0
    total_profit = 0  

    while True:
        try:
            product_id = int(input("Enter product ID (0 to finish): "))
            if product_id == 0:
                break

            found = False
            for item in stock:
                if item["id"] == product_id:
                    quantity = int(input(f"Enter quantity for {item['name']}: "))
                    if quantity <= item["quantity"]:
                        purchase_price = item["price"]
                        selling_price = round(purchase_price * (1 + PROFIT_PERCENT / 100), 2)
                        subtotal = selling_price * quantity
                        profit = (selling_price - purchase_price) * quantity
                        total += subtotal
                        total_profit += profit

                        cart.append({
                            "id": item["id"],
                            "name": item["name"],
                            "purchase_price": purchase_price,
                            "selling_price": selling_price,
                            "quantity": quantity,
                            "subtotal": subtotal,
                            "profit": profit  # stored but not printed to customer
                        })
                        item["quantity"] -= quantity
                        print(f"Added {quantity} x {item['name']} at ₹{selling_price} each\n")
                    else:
                        print("Not enough stock available\n")
                    found = True
                    break

            if not found:
                print("Product not found.\n")

        except ValueError:
            print("Invalid input. Try again.\n")

    # After items are added and total is calculated
    if cart:
        # Ask for payment method
        pay_online = input("Did customer pay online? (y/n): ").strip().lower()
        discount = 0
        if pay_online == "y":
            discount = round(total * 0.04, 2)
            total -= discount
            print(f"Applied 4% online payment discount: -₹{discount}")

        # Customer-facing bill
        print("\n --- BILL RECEIPT ---")
        for item in cart:
            print(f"{item['name']} x {item['quantity']} = ₹{item['subtotal']}")
        if discount > 0:
            print(f"Discount: -₹{discount}")
        print(f"----------------------\nTotal: ₹{total}\n")

        # Save sale
        sale = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": cart,
            "total": total,
            "total_profit": total_profit - discount  # profit reduced if discount applied
        }

        save_sale(sale)
        save_stock(stock)
        print("Sale completed and saved.\n")
        update_cash(total)
        check_low_stock()
        get_cash_in_hand()
        


