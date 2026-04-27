from pathlib import Path
import os
import json
import hashlib
import hmac

from MainMenu import MainMenu

class LoginForm:

    def __init__(self):
        self.locked = "no"
        is_username_valid = self.run_until_valid(self.receive_username_details)
        is_password_valid = self.run_until_valid(self.receive_password_details)

        if is_username_valid and is_password_valid:
            username = self.user_obj["username"]
            role = self.user_obj["role"]

            print(f"\nWelcome, {username}! (Role: {role})")
            print(self.user_obj)
            m1 = MainMenu(self.user_obj)



    def run_until_valid(self, fn):
        if self.locked == "yes":
            return 
        
        result = fn()
        if not result:
            return self.run_until_valid(fn)
        return result

    def receive_username_details(self):
        self.username = input("\nUsername: ")

        if self.is_user_exits() != True:
            msg = "\nUsername does not Exists \nTry Again"
            print(msg)
            return False
        if self.is_user_account_locked():
            print("Your account is locked contact admin")
            return False
        else:
            return True

    def receive_password_details(self):
        if self.is_user_account_locked():
            print("Your account is locked contact admin")

        self.password = input("Password: ")

        veryify_password = self.check_password(self.user_obj["password"], self.password)
        
        if veryify_password != True:
            msg = "\n\n Invalid Password \nTry Again"
            print(msg)
            self.update_wrong_password_count()
            return False
        else:
            return True

    def update_wrong_password_count(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"

        if file_name.is_file():

            username = self.user_obj["username"]
            password = self.user_obj["password"]
            role = self.user_obj["role"]
            wrong = self.user_obj["wrong"]
            user_dict = {
                "username": username,
                "password": password,
                "role": role,
                "wrong": wrong + 1,
            }
            json_string = json.dumps(user_dict)
            with open(file_name, "w") as f:
                f.write(json_string)

    def is_user_exits(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"

        if file_name.is_file():
            # get data from it
            with open(file_name, "r") as f:
                json_string = f.readline()
                user_obj = json.loads(json_string)
                self.user_obj = user_obj
            return file_name.is_file()
        
    def is_user_account_locked(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"

        if file_name.is_file():
            # get data from it
            with open(file_name, "r") as f:
                json_string = f.readline()
                user_obj = json.loads(json_string)
                if user_obj["wrong"] == 3:
                    self.locked = 'yes'
                    return True
                else:
                    return False
        

    def check_password(self, stored_string, provided_password):
        try:
            salt_hex, hash_hex = stored_string.split(":")
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256", provided_password.encode("utf-8"), salt, 100000
            )

            return hmac.compare_digest(new_hash, stored_hash)  # True or False
        except Exception:
            return False
