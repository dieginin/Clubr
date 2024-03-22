import pyrebase
from flet import Page
from flet.security import decrypt, encrypt

from utils import FIREBASE_CONFIG as keys

secret_key = "sample"


class Fyrebase:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.firebase = pyrebase.initialize_app(keys)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        self.idToken = None
        self.uuid = None

    def _save_token(self, token, uuid):
        encrypted_token = encrypt(token, secret_key)
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
            decrypted_token = decrypt(encrypted_token, secret_key)
            self.idToken = decrypted_token
            self.uuid = uuid
            try:
                self.auth.get_account_info(self.idToken)
                return "Success"
            except:
                return

    def register_new_user(self, club, username, email, password):
        users_db = self.db.child("users").get()
        try:
            if username in [u.key() for u in users_db]:
                return "Usuario existente"
            if email in [u.val()["email"] for u in users_db]:
                return "Correo existente"
            if club in [u.val()["club"] for u in users_db]:
                return "Club existente, pide el código"
        except:
            pass

        try:
            self.auth.create_user_with_email_and_password(email, password)
            self.sign_in(email, password)

            code = club[-3:] + username[-3:].upper()
            self.db.child("users").child(username).set(
                {"club": club, "email": email},
                self.idToken,
            )
            self.db.child("clubs").child(club).set(
                {"club": club, "code": code},
                self.idToken,
            )
        except:
            return "Error en regitro"
        return True

    def register_code_user(self, code, username, email, password):
        users_db = self.db.child("users").get()
        try:
            if username in [u.key() for u in users_db]:
                return "Usuario existente"
            if email in [u.val()["email"] for u in users_db]:
                return "Correo existente"
        except:
            pass

        club = ""
        clubs = self.db.child("clubs").get()
        try:
            for c in clubs:
                if c.val()["code"] == code:
                    club = c.val()["club"]
            self.auth.create_user_with_email_and_password(email, password)
            self.sign_in(email, password)

            self.db.child("users").child(username).set(
                {"club": club, "email": email},
                self.idToken,
            )
        except:
            return "Error en registro"
        return True

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
