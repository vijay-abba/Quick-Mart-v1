from pathlib import Path
import json
import random




class Product:

    file_path = Path("data")
    file_name = file_path / f"products.txt"

    def __init__(self):
        # connect to database / product txt
        self.product_list = ""
        self.read_from_file()

    def read_from_file(self):
        # if no file create empty
        if not self.file_name.is_file():
            with open(Product.file_name, "w") as f:
                f.write(json.dumps([]))

        with open(Product.file_name, "r") as f:
            str_product_list = f.readline()
            product_list = json.loads(str_product_list)
            self.product_list = product_list

    def writ_to_file(self):
        str_product_list = json.dumps(self.product_list)
        with open(Product.file_name, "w") as f:
            f.write(str_product_list)
        self.read_from_file()

    def print_key_values(self, obj_a):
        long_string = ""
        for key, value in obj_a.items():

            if key == "price":
                long_string += f" ₹{value} |"
            elif key == "quantity":
                long_string += f" Qty:{value} |"
            elif key == "type":
                pass
            else:
                long_string += f" {value} |"
        return long_string

    def add(self, name, quantity, price):

        id = f"PRD-{random.randint(0,9999):04d}"
        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "1",
        }

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"ADDED! ID {id}")
        return True

    def update(self, id, name, quantity, price):

        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "1",
        }
        self.delete(id)
        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"UPDATED! ID {id}")
        return True

    def delete(self, id):

        self.product_list = list(
            filter(lambda item: item["id"] != id, self.product_list)
        )
        self.writ_to_file()

        print(f"DELETED! ID {id}")
        return True

    def search(self, name):
        filtered_list = list(
            filter(
                lambda x: x["name"].lower().startswith(name.lower()), self.product_list
            )
        )

        # Found 1 result:
        print(f"\n Found {len(filtered_list)} results: \n")

        # list(map(lambda x: print(x), filtered_list))
        # list(map(lambda item:  self.print_key_values(item)) , filtered_list)

        for item in filtered_list:
            print(self.print_key_values(item))
        return True

    def view_all(self):
        print(f"\n Found {len(self.product_list)} results: \n")
        for i in self.product_list:
            print(self.print_key_values(i))
        return True

    def lowstock(self):
        
        filtered_list = list(
            filter(lambda x: int(x["quantity"]) < 5, self.product_list)
        )
        print(f"\n Found {len(filtered_list)} results: \n")
        for item in filtered_list:
            print(self.print_key_values(item))
        return True


class PerishableProduct(Product):
    def __init__(self):
        super().__init__()

    def add(self, name, quantity, price, expiry_date):

        id = f"PPD-{random.randint(0,9999):04d}"
        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "2",
            "expiry_date": expiry_date,
        }

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"ADDED! ID {id}")
        return True

    def update(self, id, name, quantity, price, expiry_date):

        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "2",
            "expiry_date": expiry_date,
        }
        self.delete(id)
        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"UPDATED! ID {id}")
        return True


class ElectronicProduct(Product):
    def __init__(self):
        super().__init__()

    def add(self, name, quantity, price, warranty):

        id = f"EPD-{random.randint(0,9999):04d}"
        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "3",
            "warranty": warranty,
        }

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"ADDED! ID {id}")
        return True

    def update(self, id, name, quantity, price, warranty):

        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "3",
            "warranty": warranty,
        }
        self.delete(id)

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"UPDATED! ID {id}")
        return True


class ClothingProduct(Product):
    def __init__(self):
        super().__init__()

    def add(self, name, quantity, price, size, material):
        id = f"CPD-{random.randint(0,9999):04d}"
        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "4",
            "size": size,
            "material": material,
        }

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"ADDED! ID {id}")
        return True

    def update(self, id, name, quantity, price, size, material):
        new_product_obj = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "type": "4",
            "size": size,
            "material": material,
        }
        self.delete(id)

        self.product_list.append(new_product_obj)
        self.writ_to_file()
        print(f"UPDATED! ID {id}")
        return True



