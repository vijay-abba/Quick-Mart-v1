from RegistrationForm import RegistrationForm
from LoginForm import LoginForm


class Menu:

    state = ""

    def __init__(self):
        self.show_menu()

    def show_menu(self):
        print("\n===== QuickMart =====\n\n1.Register  2.Login  3.Exit")
        choice = input("\nEnter choice: ")

        if choice == "1":
            self.register_login(RegistrationForm)
        elif choice == "2":
            self.register_login(LoginForm)
        elif choice == "3":
            print("Exit")
        else:
            print("Wrong")

    def register_data(self):
        # print("Register")
        username = input("Username: ")
        password = input("Password: ")
        role = input("Role: ")
        print("\n")
        return {"username": username, "password": password, "role": role}

    def register_login(self, fn):
        data = self.register_data()
        username = data["username"]
        password = data["password"]
        role = data["role"]

        f1 = fn(username, password, role)
        result = f1.flow()
        if not result:
            print("\n--TRY AGAIN--")
            self.register_login(fn)


m1 = Menu()
