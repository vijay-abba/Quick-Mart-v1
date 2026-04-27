from RegisterForm import RegistrationForm
from LoginForm import LoginForm


class LoginAndRegisterMenu:

    def __init__(self):
        action_indexs = ["1", "2", "3"]
        action_message = (
            "\n===== QuickMart =====\n\n1.Register  2.Login  3.Exit\n\nEnter choice: "
        )

        self.action_choice = self.run_until_valid(
            self.action_choice_validate_fn, action_indexs, action_message
        )

        result = self.define_operation()

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

    def define_operation(self):

        if self.action_choice == "1":
            print("\n--- Register ---")
            r1 = RegistrationForm()
            if r1:
                self.__init__()

        elif self.action_choice == "2":
            print("\n--- Login ---")
            l1 = LoginForm()
        elif self.action_choice == "3":
            print("\n--- Exit ---")
        else:
            print("INVALID AGAIN")


lr1 = LoginAndRegisterMenu()
