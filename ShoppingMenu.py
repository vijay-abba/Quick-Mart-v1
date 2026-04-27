from pathlib import Path
import json
import random
from datetime import date


class ShoppingMenu:

    def __init__(self, user_obj):
        self.user_obj = user_obj
        action_indexs = ["1", "2", "3", "4"]
        action_message = "\n===== New Sale =====\n\n1.Add to Cart\n2.View Cart\n3.Remove Item\n4.Checkout\n\nEnter Choice: "
        self.action_choice = self.run_until_valid(
            self.action_choice_validate_fn, action_indexs, action_message
        )

        self.c1 = self.Cart(self.user_obj)

        self.define_operation()

    def run_until_valid(self, fn, index_list, message):
        result = fn(index_list, message)

        if not result:
            return self.run_until_valid(fn, index_list, message)

        return result

    def action_choice_validate_fn(self, index_list, message):
        action_list = index_list
        action_choice = input(message)
        if action_choice in action_list:
            return action_choice
        else:
            print("\nInvalid choice, TRY AGAIN")
            return False

    def define_operation(self):
        if self.action_choice == "1":
            print("----Add to Cart----")
            product_id = input("Product ID: ")
            quantity = input("Quantity : ")
            result = self.c1.add_to_cart(product_id, quantity)
            if result:
                self.__init__()

        elif self.action_choice == "2":
            print("View Cart")
            result = self.c1.view_cart()
            if result:
                self.__init__(self.user_obj)
        elif self.action_choice == "3":
            print("Remove Item")
            id = input("Enter Id: ")
            result = self.c1.remove_item(id)
            if result:
                self.__init__()
        elif self.action_choice == "4":
            print("Checkout")
        else:
            print("INVALID AGAIN")

    class Cart:
        # unable to use file_name and file_path as class variables in inner class
        def __init__(self, user_obj):
            self.user_obj = user_obj
            file_path = Path("data")
            self.file_name = file_path / f"cart.txt"
            self.cart = []
            self.read_from_file()

        def read_from_file(self):
            # if no file create empty
            if not self.file_name.is_file():
                with open(self.file_name, "w") as f:
                    f.write(json.dumps([]))

            with open(self.file_name, "r") as f:
                str_cart_list = f.readline()
                cart_list = json.loads(str_cart_list)
                self.cart = cart_list

        def writ_to_file(self):
            str_cart_list = json.dumps(self.cart)
            with open(self.file_name, "w") as f:
                f.write(str_cart_list)
            self.read_from_file()

        def validate_product_id_quantity(self, id, quantity):
            file_path = Path("data")
            products_file_name = file_path / f"products.txt"

            if products_file_name.is_file():
                with open(products_file_name, "r") as f:
                    str_product_list = f.readline()
                    product_list_obj = json.loads(str_product_list)
                    selected_items = list(
                        filter(lambda i: i["id"] == id, product_list_obj)
                    )

                    item = (
                        selected_items[0]
                        if selected_items
                        else print("No Product Found")
                    )
                    if not item:
                        return [False]

                    item_avl_stock = item["quantity"]
                    stock_check = int(item_avl_stock) < int(quantity)
                    if stock_check:
                        print(f"Only {item_avl_stock} left in stock")
                        return [False]
                    return [True, item]

        def print_invoice(self):
            divider = "========================================"
            heading = "         QUICKMART - INVOICE"
            heading = f"{divider}\n{heading}\n{divider}"
            print(heading)

            date_string = f"Date: {date.today()}"
            user_string = f"Cahier: {self.user_obj['username']}"
            date_user_text = f"{date_string.ljust(20)}{user_string.rjust(19)}"
            print(date_user_text)

            divider_two = "----------------------------------------"
            sub_heading_string = (
                f"{'Item'.ljust(15)}{'Qty'.ljust(6)}{'Price'.ljust(9)}{'Subtotal'}"
            )
            print(divider_two)
            print(sub_heading_string)
            print("ITEMS ")

            print(divider_two)

            print(divider)

        def add_to_cart(self, id, quantity):
            item_obj = {"id": id, "quantity": quantity}
            # TASK 1. VALIDATE USER PRODUCT EXIST
            # TASK 2. Validate quantity avaliable and entered Number
            # add product pirce if item is already present in cart then increment quantity 
            result = self.validate_product_id_quantity(id, quantity)
            if result[0]:
                self.cart.append(item_obj)
                print(f"Added! ID: {id} x{quantity}")
                self.writ_to_file()
            return True

        def view_cart(self):
            # self.read_from_file()
            print(self.cart)

            self.print_invoice()

            return True

        def remove_item(self, id):
            # self.read_from_file()
            print(id)
            # TASK 3  CHEKC ID EXIST IN CART
            # Task Check if id product exist in cart
            filtered_cart = list(filter(lambda item: item["id"] != id, self.cart))
            print(filtered_cart)
            self.cart = filtered_cart
            self.writ_to_file()
            print("remove item ")
            return True

        def checkout(self):
            print("Checkout ")


user_obj = {
    "username": "vijay",
    "password": "89297d356b74ddc8d217eb863eb970e3:df6c51583f8677b4e8bec1f6978ee8c5ed3f3a26bb3aba0e69753865ebe4e6cd",
    "role": "staff",
    "wrong": 3,
}
sm = ShoppingMenu(user_obj)
