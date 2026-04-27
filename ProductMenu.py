from Product import Product, PerishableProduct, ElectronicProduct, ClothingProduct


class ProductMenu:

    def __init__(self, user_obj):
        self.user_obj = user_obj
        # print(user_obj)
        action_indexs = ["1", "2", "3", "4", "5", "6"]
        action_message = "\n===== Inventory =====\n\n\n1.Add  2.Update  3.Delete 4.Search  5.View All  6.Low Stock:\n"

        self.action_choice = self.run_until_valid(
            self.action_choice_validate_fn, action_indexs, action_message
        )

        self.define_operation()

    def action_choice_validate_fn(self, index_list, message):
        action_list = index_list
        action_choice = input(message)
        if action_choice in action_list:
            return action_choice
        else:
            print("\nInvalid choice, TRY AGAIN")
            return False

    def run_until_valid(self, fn, index_list, message):
        result = fn(index_list, message)

        if not result:
            return self.run_until_valid(fn, index_list, message)

        return result

    def prodoct_choice_fn(self):
        product_index = ["1", "2", "3", "4"]
        product_message = (
            "\n--- Add Product ---\n\n1.General 2.Perishable 3.Electronic 4.Clothing:\n"
        )
        return self.run_until_valid(
            self.action_choice_validate_fn, product_index, product_message
        )

    def add_product_details(self, product_type):
        if product_type == "1":
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")

            p1 = Product()
            p1.add(name, quantity, price)

        elif product_type == "2":
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            expiry_date = input("Expiry Date: ")

            pp2 = PerishableProduct()
            pp2.add(name, quantity, price, expiry_date)

        elif product_type == "3":

            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            warranty = input("Warranty: ")

            ep3 = ElectronicProduct()
            ep3.add(name, quantity, price, warranty)

        elif product_type == "4":
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            size = input("Size: ")
            material = input("Material: ")

            ecp4 = ClothingProduct()
            ecp4.add(name, quantity, price, size, material)

    def update_product_details(self, product_type):
        if product_type == "1":
            id = input("Id:")
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")

            p1 = Product()
            p1.update(id, name, quantity, price)

        elif product_type == "2":
            id = input("Id:")
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            expiry_date = input("Expiry Date: ")

            pp2 = PerishableProduct()
            pp2.update(id, name, quantity, price, expiry_date)

        elif product_type == "3":
            id = input("Id:")
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            warranty = input("Warranty: ")

            ep3 = ElectronicProduct()
            ep3.update(id, name, quantity, price, warranty)

        elif product_type == "4":
            id = input("Id:")
            name = input("Name:")
            quantity = input("Quantity: ")
            price = input("Price: ")
            size = input("Size: ")
            material = input("Material: ")

            ecp4 = ClothingProduct()
            ecp4.update(id, name, quantity, price, size, material)

    def delete_product_details(self):
        id = input("ID: ")
        p1 = Product()
        isExist = list(filter(lambda x: x["id"] == id, p1.product_list))
        if len(isExist) == 1 and isExist[0]["id"] == id:
            p1.delete(id)

    def search_products(self):
        name = input("Name: ")
        p1 = Product()
        p1.search(name)

    def define_operation(self):
        # Task 1. validate input data in add_product_details and update_product_details
        # Task 2. Check If product exist in update option
        # Optional Task 3. Can access only that product type items (eg: Electronics when pro_type = 3 )

        if self.action_choice == "1":
            product_type_choice = self.prodoct_choice_fn()
            self.add_product_details(product_type_choice)

        elif self.action_choice == "2":
            product_type_choice = self.prodoct_choice_fn()
            self.update_product_details(product_type_choice)

        elif self.action_choice == "3":
            self.delete_product_details()

        elif self.action_choice == "4":
            self.search_products()

        elif self.action_choice == "5":
            p1 = Product()
            p1.view_all()

        elif self.action_choice == "6":
            p1 = Product()
            p1.lowstock()
        else:
            print("INVALID AGAIN")


# pm = ProductMenu()
