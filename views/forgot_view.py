from time import sleep

from flet import (
    CrossAxisAlignment,
    ElevatedButton,
    FloatingActionButton,
    MainAxisAlignment,
    Page,
    VerticalDivider,
    View,
)

from components import AuthCard, CenterColumn, MailField, Title
from services import Fyrebase
from utils import error_snackbar, success_snackbar


class ForgotView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()
        self.fb = fb
        self.pg = page

        self.init_ui()

    def init_ui(self):
        self.setup_layout()
        self.setup_fields()
        self.setup_controls()

    def setup_layout(self):
        self.route = "/forgot"
        self.bgcolor = "primary"
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.floating_action_button = FloatingActionButton(
            "Regresar", on_click=lambda _: self.pg.go("/login"), width=85
        )

    def setup_fields(self):
        self.mail_field = MailField("Correo", self.send_reset)

    def setup_controls(self):
        self.form_sectn = CenterColumn(
            [
                self.mail_field,
                VerticalDivider(),
                ElevatedButton("Recuperar", on_click=self.send_reset),
            ],
            width=340,
        )

        self.controls = [
            AuthCard(
                [Title("Recuperación de Contraseña"), self.form_sectn],
                style="slim",
            )
        ]

    def send_reset(self, _):
        if self.mail_field.value == "" or self.mail_field.color == "red":
            error_snackbar(self.pg, "Ingrese un correo válido")
            self.mail_field.focus()
            return
        self.fb.send_reset_email(self.mail_field.value)
        success_snackbar(self.pg, "Correo de recuperación enviado")
        sleep(0.2)
        self.pg.go("/login")
