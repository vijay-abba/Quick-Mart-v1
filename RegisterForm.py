import hashlib
import os
import json
from pathlib import Path


class RegistrationForm:

    def __init__(self):
        is_username_valid = self.run_until_valid(self.receive_username_details)
        is_password_valid = self.run_until_valid(self.receive_password_details)
        is_role_valid = self.run_until_valid(self.receive_role_details)

        if is_username_valid and is_password_valid and is_role_valid:
            self.create_new_user()

    def run_until_valid(self, fn):
        result = fn()
        if not result:
            return self.run_until_valid(fn)
        return result

    def receive_username_details(self):
        self.username = input("\nUsername: ")

        if self.username_is_valid() != True:
            msg = "\nThe username must be 4–20 characters long and should not contain spaces.\nTry Again"
            print(msg)
            return False
        elif self.is_user_exits() == True:
            msg = "\nUsername already Exist Try with different username \nTry Again"
            print(msg)
            return False
        else:
            return True

    def receive_password_details(self):
        self.password = input("Password: ")

        if self.password_is_valid() != True:
            msg = "\n\nPassword must contain at least 9 characters, including at least 1 uppercase letter and 1 digit.\nTry Again"
            print(msg)
            return False
        else:
            return True

    def receive_role_details(self):
        self.role = input("Role: ")

        if self.role != "staff" and self.role != "admin":
            msg = "\n\nRole must be either (staff or admin)\nTry Again"
            print(msg)
            return False
        else:
            return True

    def is_user_exits(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"
        return file_name.is_file()

    def username_is_valid(self):
        # check len 4 to 20 adn no spaces
        length_username = len(self.username)
        spaces_count = self.username.count(" ")
        if length_username >= 4 and length_username <= 20 and spaces_count == 0:
            return True
        else:
            return False

    def password_is_valid(self):
        # check psd for 1 upper 1 number and atleast 9 chars length
        length_password = len(self.password)
        upper_count = len(list(filter(lambda c: c.isupper(), self.password)))
        digits_count = len(list(filter(lambda i: i.isnumeric(), self.password)))

        if length_password > 8 and upper_count >= 1 and digits_count >= 1:
            return True
        else:
            return False

    def hash_password(self):
        salt = os.urandom(16)

        # Explicitly call the constructor# Ensure password is encoded to bytes
        dk = hashlib.pbkdf2_hmac("sha256", self.password.encode("utf-8"), salt, 100000)

        # If dk is None, it means your Python build has a broken hashlib/OpenSSL link
        if dk is None:
            raise RuntimeError(
                "Hashlib failed to generate a key. Check your OpenSSL installation."
            )

        return salt.hex() + ":" + dk.hex()

    def create_new_user(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"
        user_dict = {
            "username": self.username,
            "password": self.hash_password(),
            "role": self.role,
            "wrong": 0
        }
        user_dict_json = json.dumps(user_dict)

        with open(file_name, "w") as f:
            f.write(user_dict_json)

        print("\nRegistration successful!")

        # FOR  DEVELOPEMENT only (to  see password )
        all_user_file = file_path / "user-data.txt"
        with open(all_user_file, "a") as f:
            f.write(f"{self.username} | {self.password} | {self.role}\n")
