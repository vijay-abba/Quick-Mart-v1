import hashlib
import os
import json
from pathlib import Path


class RegistrationForm:

    def __init__(self, username, password, role="staff"):
        self.username = username
        self.password = password
        self.role = role

    def validate_role(self):
        if self.role == "staff":
            return True
        elif self.role == "admin":
            return True
        else:
            return False

    def validate_username(self):
        length_username = len(self.username)
        spaces_count = self.username.count(" ")
        if length_username >= 4 and length_username <= 20 and spaces_count == 0:
            return True
        else:
            return False

    def validate_password(self):
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

    def save_it(self, hash):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"
        user_dict = {"Username": self.username, "Password": hash, "Role": self.role}
        user_dict_json = json.dumps(user_dict)

        with open(file_name, "w") as f:
            f.write(user_dict_json)

        # for Devvelopment only
        all_user_file = file_path / "user-data.txt"
        with open(all_user_file, "a") as f:
            f.write(f" {self.username} | {self.password} | {self.role}")

    def isUserExist(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"
        return file_name.is_file()

    def flow(self):
        if not self.validate_username():
            print(
                "The username must be 4–20 characters long and should not contain spaces."
            )
            return False
        if not self.validate_password():
            print(
                "Password must contain at least 9 characters, including at least 1 uppercase letter and 1 digit."
            )
            return False

        if not self.validate_role():
            print("Role should be (staff or admin)")

        if not self.isUserExist():
            hash = self.hash_password()
            self.save_it(hash)
            print("\nRegistration successful!")
            return True
        else:
            print("\nuser already Exist")
            return False


# r1 = RegistrationForm("Prajapathi", "1Vijaykrishna")
# print(r1.flow())
