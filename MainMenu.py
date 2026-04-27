from ProductMenu import ProductMenu

class MainMenu:

    def __init__(self, user_obj):
        self.user_obj = user_obj
        print(
            "\n============================\n    QUICKMART MAIN MENU    \n============================"
        )

        self.load_staff_or_admin()

        result = self.define_operation()

    def load_staff_or_admin(self):
        if self.user_obj["role"] == "staff":
            menu = "\n1. Inventory Management\n2. New Sale\n3. Order History\n4. Reports\n5. Logout\n6. Exit\n\nEnter choice: "
            action_index = ["1", "2", "3", "4", "5", "6"]
            self.action_choice = self.run_until_valid(
                self.action_choice_validate_fn, action_index, menu
            )
            # print("selected", self.action_choice)

        elif self.user_obj["role"] == "admin":
            menu = "\n1. Inventory Management\n2. New Sale\n3. Order History\n4. Reports\n5. Coupons       [Admin only]\n6. User Mgmt     [Admin only]\n7. Logout\n8. Exit\n\nEnter choice: "
            action_index = ["1", "2", "3", "4", "5", "6", "7", "8"]
            self.action_choice = self.run_until_valid(
                self.action_choice_validate_fn, action_index, menu
            )
            # print("selected", self.action_choice)

    def action_choice_validate_fn(self, index_list, message):
        action_list = index_list
        action_choice = input(message)
        if action_choice in action_list:
            return action_choice
        else:
            print("\nInvalid choice, TRY AGAIN")
            return False

    def run_until_valid(self, fn, list_indexs, messages):
        result = fn(list_indexs, messages)
        if not result:
            return self.run_until_valid(fn, list_indexs, messages)
        return result

    def define_operation(self):

        if self.action_choice == "1":
            print("Inventary management")
            p1 = ProductMenu(self.user_obj)
            if p1.result:
                self.__init__(self.user_obj)

        elif self.action_choice == "2":
            print("New Sale management")

        elif self.action_choice == "3":
            print("Order History management")

        elif self.action_choice == "4":
            print("Reports management")

        elif self.action_choice == "5":
            print("Coupons management")

        elif self.action_choice == "6":
            print("User Mgmt  management")

        elif self.action_choice == "7":
            print("Logout management")

        elif self.action_choice == "8":
            print("Exit management")

        else:
            print("INVALID AGAIN")


# user_object = {
#     "username": "vijay1",
#     "password": "66ded1eebda7c3a9257a167f94ceebc7:bd88a1d0359a12ee29444089664844ee82223df6dcac8963cf7eb578ff70704e",
#     "role": "admin",
#     "wrong": 0,
# }
# m1 = MainMenu(user_object)
