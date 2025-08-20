from stock_manager import add_product,view_stock,delete_product,update_product
from billing import generate_bill
from report import view_sales_report
from supplier_manager import request_stock_from_supplier,pay_supplier
def main():
    while True:
        print("\n ----Supermarket Stock Management----")
        print("1.Add Product")
        print("2.View Stock")
        print("3.Update Product")
        print("4.Delete Product")
        print("5.Generate Bill")
        print("6.View Sales Report")
        print("7.request_stock_from_supplier")
        print("8.pay_supplier")
        print("9.Exit")
        choice = input("Enter your choice:")
        if choice == '1':
            add_product()
        elif choice =='2':
            view_stock()
        elif choice == '3':
            delete_product()
        elif choice == '4':
            update_product()
        elif choice == '5':
            generate_bill()
        elif choice =='6':
            view_sales_report()
        elif choice =='7':
            request_stock_from_supplier()
        elif choice =='8':
            pay_supplier()
        elif choice =='9':
            print('Exiting..')
            break
        else:
            print("Invalid choice.Try again.")
if __name__ == "__main__":
    main()