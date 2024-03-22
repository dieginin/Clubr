import pyrebase
from flet import Page
from flet.security import decrypt, encrypt

from utils import FIREBASE_CONFIG as keys

SECRET_KEY = "sample"


class Fyrebase:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.firebase = pyrebase.initialize_app(keys)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        self.idToken = None
        self.uuid = None

    def _save_token(self, token, uuid):
        encrypted_token = encrypt(token, SECRET_KEY)
        self.page.client_storage.set("firebase_token", encrypted_token)
        self.page.client_storage.set("firebase_id", uuid)
        self.idToken = token
        self.uuid = uuid

    def _erase_token(self):
        self.page.client_storage.remove("firebase_token")
        self.page.client_storage.remove("firebase_id")

    def check_token(self):
        encrypted_token = self.page.client_storage.get("firebase_token")
        uuid = self.page.client_storage.get("firebase_id")
        if encrypted_token:
            decrypted_token = decrypt(encrypted_token, SECRET_KEY)
            self.idToken = decrypted_token
            self.uuid = uuid
            try:
                self.auth.get_account_info(self.idToken)
                return True
            except:
                return False
        return False

    def _user_exists(self, username, email, club=None):
        users_db = self.db.child("users").get()
        try:
            for user in users_db:
                if user.key() == username:
                    return "Usuario existente"
                if "email" in user.val() and user.val()["email"] == email:
                    return "Correo existente"
                if club and "club" in user.val() and user.val()["club"] == club:
                    return "Club existente, pide el código"
            return False
        except:
            return False

    def register_new_user(self, club, username, email, password):
        user_exists = self._user_exists(username, email, club)
        if user_exists:
            return user_exists

        try:
            self.auth.create_user_with_email_and_password(email, password)
            self.sign_in(email, password)

            code = club[-3:] + username[-3:].upper()
            self.db.child("users").child(username).set(
                {"club": club, "email": email}, self.idToken
            )
            self.db.child("clubs").child(club).set(
                {"club": club, "code": code}, self.idToken
            )
            return True
        except:
            return "Error en registro"

    def register_code_user(self, code, username, email, password):
        user_exists = self._user_exists(username, email)
        if user_exists:
            return user_exists

        club = ""
        clubs = self.db.child("clubs").get()
        for c in clubs:
            if "code" in c.val() and c.val()["code"] == code:
                club = c.val()["club"]
                break
        try:
            self.auth.create_user_with_email_and_password(email, password)
            self.sign_in(email, password)

            self.db.child("users").child(username).set(
                {"club": club, "email": email}, self.idToken
            )
            return True
        except:
            return "Error en registro"

    def _get_email_from_username(self, users_db, username):
        email = ""
        try:
            for user in users_db.each():
                if user.key() == username:
                    email = user.val().get("email", "")
                    break
        except:
            pass
        return email

    def sign_in_with_username(self, username, password):
        users_db = self.db.child("users").get()
        email = self._get_email_from_username(users_db, username)
        if not email:
            return False

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            if user:
                token = user["idToken"]
                uuid = user["localId"]
                self._save_token(token, uuid)
                return True
        except:
            return False
        return False

    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        if user:
            token = user["idToken"]
            uuid = user["localId"]
            self._save_token(token, uuid)

    def verification_email(self, email):
        self.auth.send_email_verification(email)

    def send_reset_email(self, email):
        self.auth.send_password_reset_email(email)

    def sign_out(self):
        self._erase_token()
