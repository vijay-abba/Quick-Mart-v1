from pathlib import Path
import json
import random
from datetime import datetime, date, time


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
                self.__init__(self.user_obj)

        elif self.action_choice == "2":
            # print("View Cart")
            result = self.c1.view_cart()
            if result:
                self.__init__(self.user_obj)
        elif self.action_choice == "3":
            print("Remove Item")
            id = input("Enter Id: ")
            result = self.c1.remove_item(id)
            if result:
                self.__init__(self.user_obj)
        elif self.action_choice == "4":
            print("Checkout")
            result = self.c1.checkout()
            if result:
                self.__init__(self.user_obj)
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

        def print_invoice(self):
            divider = "========================================"
            heading = "         QUICKMART - INVOICE"
            heading = f"{divider}\n{heading}\n{divider}"
            print(heading)

            now = datetime.today()
            date_string = f"Date: {now.date()}"
            user_string = f"Cahier: {self.user_obj['username']}"
            date_user_text = f"{date_string.ljust(20)}{user_string.rjust(19)}"
            print(date_user_text)

            divider_two = "----------------------------------------"
            sub_heading_string = (
                f"{'Item'.ljust(15)}{'Qty'.ljust(6)}{'Price'.ljust(9)}{'Subtotal'}"
            )

            print(divider_two)
            print(sub_heading_string)

            # print items
            total_subtotal = 0
            for item in self.cart:

                name = item["name"]
                quantity = int(item["quantity"])
                price = float(item["price"])
                subtotal = quantity * price
                total_subtotal += subtotal

                num_price = int(price)
                f_price = f"{num_price:.2f}"
                fmt_price = str(f_price).rjust(9)

                fmt_name = name[:13].ljust(13)
                fmt_quantity = str(quantity).rjust(4)

                f_subtotal = f"{subtotal:.2f}"
                fmt_subtotal = str(f_subtotal).rjust(11)

                line = f"{fmt_name}{fmt_quantity}{fmt_price}{fmt_subtotal}"
                print(line)

            print(divider_two)
            # ---

            f_total_subtotal = f"{total_subtotal:.2f}"
            pad_f_total_subtotal = f_total_subtotal.rjust(28)
            subtotal = f"{'Subtotal:'}{pad_f_total_subtotal}"
            print(subtotal)

            discount_amt = 0
            if total_subtotal > 10000:
                discount_amt += (15 / 100) * total_subtotal
                f_discount_amt = f"-{discount_amt:.2f}"
                print(f"Discount (15%):{f_discount_amt.rjust(22)}")
            elif total_subtotal > 5000:
                discount_amt += (10 / 100) * total_subtotal
                f_discount_amt = f"-{discount_amt:.2f}"
                print(f"Discount (10%):{f_discount_amt.rjust(22)}")

            # GST
            # total_subtotal - discount_amt
            new_total = total_subtotal - discount_amt
            gst_amt = (18 / 100) * new_total
            f_gst_amt = f"{gst_amt:.2f}"
            print(f"GST (18%):{f_gst_amt.rjust(27)}")

            grand_total = new_total + gst_amt
            # save_grand total in self 

            f_grand_total = f"{grand_total:.2f}"
            # print(f_grand_total)
            print(f"GRAND TOTAL:{f_grand_total.rjust(25)}")

            print(divider)

        def get_product_obj(self, id):
            file_path = Path("data")
            products_file_name = file_path / f"products.txt"

            if products_file_name.is_file():
                with open(products_file_name, "r") as f:
                    str_product_list = f.readline()
                    product_list_obj = json.loads(str_product_list)
                    selected_items = list(
                        filter(lambda i: i["id"] == id, product_list_obj)
                    )

                    if selected_items:
                        return selected_items[0]
                    else:
                        print("No Product Found")
                        return False
            else:
                print("No Products Found")
                return False

        def add_to_cart(self, id, quantity):
            cart_item_obj = {"id": id, "quantity": quantity}
            # TASK 1. VALIDATE USER PRODUCT EXIST
            # TASK 2. Validate quantity avaliable and entered Number

            product = self.get_product_obj(id)
            avaliable_quantity = int(product["quantity"])

            if avaliable_quantity < int(quantity):
                print(f"Only {avaliable_quantity} left in stock")
            else:
                cart_item_obj["name"] = product["name"]
                cart_item_obj["price"] = product["price"]

            self.cart.append(cart_item_obj)
            print(f"Added! ID: {id} x{quantity}")
            self.writ_to_file()
            return True

        def view_cart(self):
            # self.read_from_file()
            # print(self.cart)

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

            # create data/orders.txt
            # orders schema
            # id, name, total amount , date , casier(staff)

            # TASK should be replaces
            current_order_value = 5000
            # current_order_value = 500
            
            # TASK  get Coupons 
            avaliable_coupons = [
                {
                    "code": "SAVE10",
                    "type": 1,
                    "value": "10",
                    "min-order": "1000",
                    "expiry": "2026-04-28",
                    "usage-limit": "100",
                },
                {
                    "code": "SAVE20",
                    "type": 1,
                    "value": "10",
                    "min-order": "1000",
                    "expiry": "2026-12-31",
                    "usage-limit": "0",
                },
                {
                    "code": "SAVE30",
                    "type": 1,
                    "value": "10",
                    "min-order": "1000",
                    "expiry": "2025-12-31",
                    "usage-limit": "40",
                },
                {
                    "code": "OFF500",
                    "type": 2,
                    "value": "500",
                    "min-order": "1000",
                    "expiry": "2026-12-31",
                    "usage-limit": "100",
                },
            ]

            #  Coupon: SAVE10
            # Coupon applied! ₹500 off

            coupon_code = input("Coupon code (or skip): ")
            # customer_name = input("Customer name: ")
            coupone_code_list = list(map(lambda x: x["code"], avaliable_coupons))

            print(coupone_code_list)
            if coupon_code != "":
                print("Apply Coupon here ")
                if coupon_code in coupone_code_list:
                    print("COUPON IS PRESENT ")

                    valid_coupon_obj = list(
                        filter(lambda x: x["code"] == coupon_code, avaliable_coupons)
                    )[0]
                    expiry_date = valid_coupon_obj["expiry"]
                    min_order_value = int(valid_coupon_obj["min-order"])
                    usage_limit = int(valid_coupon_obj["usage-limit"])

                    expiry_date_obj = datetime.fromisoformat(expiry_date)
                    hours_24 = 86400
                    expiry_date_timestamp = expiry_date_obj.timestamp() + hours_24
                    print("expiry_date_timestamp", expiry_date_timestamp)

                    today = date.today()
                    today_date = datetime.combine(today, time.min)
                    today_timestamp = today_date.timestamp()
                    print("today_timestamp", today_timestamp)

                    if expiry_date_timestamp < today_timestamp:
                        print("your coupon expired")
                    else:
                        print("coupon is valid")
                        if current_order_value < min_order_value:
                            print(
                                f"minium order value should be at least{min_order_value}"
                            )
                        else:
                            print("you have min order value amount")
                            print(usage_limit)
                            if usage_limit < 1:
                                print("coupon limit is completd")
                            else:
                                print("You can use the coupoin ")
                                # check type 1 or type 2 
                                # if type 1 cal percentage 

                                #if 2 subtact  amount for grand total 

            else:
                print("Direct Checkout")

            print("Checkout ")
            return True


user_obj = {
    "username": "vijay",
    "password": "89297d356b74ddc8d217eb863eb970e3:df6c51583f8677b4e8bec1f6978ee8c5ed3f3a26bb3aba0e69753865ebe4e6cd",
    "role": "staff",
    "wrong": 3,
}
sm = ShoppingMenu(user_obj)
