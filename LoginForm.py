from pathlib import Path
import os
import json
import hashlib
import hmac

class LoginForm:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.stored_user_obj = {}

    def user_exist(self):
        files = list(Path("employees").glob("*.txt"))
        file_names = list(map(lambda file: str(file).split(".")[0], files))
        isExist = list(filter(lambda name: name == f'employees/{self.username}', file_names))
        return True if len(isExist) == 1 else False

    def get_stored_user_obj(self):
        file_path = Path("employees")
        file_name = file_path / f"{self.username}.txt"
        with open(file_name, "r") as f:
            dict_json = f.readlines()
            if len(dict_json) == 1:
                user_dict = json.loads(dict_json[0])
                self.stored_user_obj = user_dict
                return True
            elif len(dict_json) == 0:
                return False

    def check_password(self, stored_string, provided_password):
        try:
            salt_hex, hash_hex = stored_string.split(":")
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256", provided_password.encode("utf-8"), salt, 100000
            )

            return hmac.compare_digest(new_hash, stored_hash) #True or False 
        except Exception:
            return False

    def flow(self):

        if not self.user_exist():
            print("\nUsername not found!")
            return False
        
        if not self.get_stored_user_obj():
            print("\nUser file exist But No data found in it")
            return False
        
        hashed_stirng = self.stored_user_obj["Password"]
        role = self.stored_user_obj["Role"]

        if self.check_password(hashed_stirng, self.password):
            print(f"\nWelcome, {self.username}! (Role: {role})")
            return True
        else:
            print("Invalid Password")
            return False

l1 = LoginForm("Prajapathi", "1Vijaykrishna") 
