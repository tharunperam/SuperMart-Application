import json
import os

STOCK_FILE ='stock.json'

#Loading the stock file 
def load_stock():
    if not os.path.exists(STOCK_FILE):
        return []
    with open (STOCK_FILE,'r') as file:
        return json.load(file)
    
#saving the stock file
def save_stock(stock):
    with open (STOCK_FILE,'w') as file:
        json.dump(stock,file,indent=4)
# Adding a New Product
def add_product():
    stock = load_stock()
    try:
        product_id= int(input('Enter Product id :'))
        name = input('Enter Product name :')
        price = float(input("enter Price :"))
        quantity = int(input("Enter Quantity :"))
        min_stock = int(input("Enter Minimum Stock Level :")) 
    #checking duplicate ids

        for item in stock:
            if item["id"]==product_id:
                print("Product_ID Alredy exist!")
                return
        # Appending a new Product stock 
        stock.append({
            "id" : product_id,
            "name": name,
            "price":price,
            "quantity":quantity,
            "min_stock": min_stock  

        })
        #saving the changes
        save_stock(stock)
        print("Product added successfully!\n")
    except ValueError:
        print("Invalid input. Try again.")
# View all products in the stock
def view_stock():
    stock=load_stock()
    if not stock:
        print("No Product in stock \n")
        return
    print("\n---Current Stock---")
    for item in stock:
        print(f"ID:{item['id']}|Name:{item['name']}|Price:{item['price']}|Quantity:{item['quantity']}")
        print()
def delete_product():
    stock = load_stock()
    product_id = int(input("Enter Product ID to delete: "))
    new_stock = [item for item in stock if item["id"] != product_id]
    if len(new_stock)==len(stock):
        print("Prduct ID not found.\n")
    else:
        save_stock(new_stock)
        print("Product deleted successfully")
def update_product():
    stock = load_stock()
    product_id = int(input("Enter product ID to update :"))
    for item in stock:
        if item["id"] == product_id:
            name = input("enter new name :")
            price = float(input("enter new price :"))
            quantity = int(input("enter new quantity :"))
            min_stock = input(f"Enter new minimum stock ({item.get('min_stock', 15)}): ")
            item["name"] =name
            item["price"] = price
            item["quantity"] = quantity
            item["min_stock"] = min_stock
            
            save_stock(stock)
            print("Product updated successfully!\n")
            return 
    print("Product ID not found.\n")





        
