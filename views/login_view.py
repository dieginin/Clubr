from time import sleep

from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    ElevatedButton,
    MainAxisAlignment,
    Page,
    ProgressBar,
    VerticalDivider,
    View,
)

from components import (
    AuthCard,
    MyTextButton,
    PasswordField,
    SecondaryButton,
    Title,
    UserField,
)
from services import Fyrebase
from utils import error_snackbar, success_snackbar


class LoginView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()
        self.fb = fb
        self.pg = page

        self.route = "/login"
        self.bgcolor = "primary"
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.user_field = UserField("Usuario", self.login, autofocus=True)
        self.pass_field = PasswordField("Contraseña", self.login)

        self.controls = [
            AuthCard(
                [
                    Title("Bienvenido\nPor favor inicia sesión"),
                    VerticalDivider(),
                    self.form_section(),
                ]
            ),
        ]

    def form_section(self):
        return Column(
            [
                self.user_field,
                self.pass_field,
                Container(height=5),
                ElevatedButton("Iniciar Sesión", on_click=self.login),
                SecondaryButton(
                    "Registrarse", on_click=lambda _: self.pg.go("/register")
                ),
                Container(height=20),
                MyTextButton(
                    "Recuperar contraseña", on_click=lambda _: self.pg.go("/forgot")
                ),
            ],
            alignment=MainAxisAlignment.END,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    def login(self, _):
        if self.user_field.value == "" or self.user_field.color == "red":
            error_snackbar(self.pg, "Ingrese un usuario válido")
            self.user_field.focus()
            return
        if self.pass_field.value == "" or self.pass_field.color == "red":
            error_snackbar(self.pg, "Ingrese una contraseña válida")
            self.pass_field.focus()
            return

        self.pg.splash = ProgressBar()
        self.disabled = True
        self.pg.update()

        if self.fb.sign_in_with_username(self.user_field.value, self.pass_field.value):
            success_snackbar(self.pg, "Inicio correcto")
            sleep(0.2)
            self.pg.go("/")
        else:
            error_snackbar(self.pg, "Revise sus credenciales")

        self.pg.splash = None
        self.disabled = False
        self.pg.update()
