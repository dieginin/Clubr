from flet import (
    CrossAxisAlignment,
    ElevatedButton,
    FloatingActionButton,
    MainAxisAlignment,
    Page,
    ProgressBar,
    View,
)

from components import (
    AuthCard,
    CenterColumn,
    CodeField,
    MailField,
    PasswordField,
    RepeatPasswordField,
    SecondaryButton,
    Title,
    UserField,
)
from services import Fyrebase
from utils import error_snackbar


class RegisterView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()
        self.fb = fb
        self.pg = page

        self.floating_action_button = FloatingActionButton(
            "Regresar", on_click=lambda _: self.pg.go("/login"), width=85
        )

        self.route = "/register"
        self.bgcolor = "primary"
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.code_field = CodeField("Código", self.set_code)

        self.club_field = CodeField("Club Tag", self.register)
        self.mail_field = MailField("Correo", self.register)
        self.pass_field = PasswordField("Contraseña", self.register)
        self.pcon_field = RepeatPasswordField(
            self.pass_field, "Confirmar Contraseña", self.register
        )
        self.user_field = UserField("Usuario", self.register)

        self.code_sectn = CenterColumn(
            [
                Title("Ingresa el código de tu club"),
                self.code_field,
                ElevatedButton("Guardar", on_click=self.set_code),
                SecondaryButton("No tengo código", on_click=self.no_code),
            ]
        )
        self.info_sectn = CenterColumn(
            [
                Title("Ingresa tus datos"),
                CenterColumn(
                    [
                        self.mail_field,
                        self.user_field,
                        self.pass_field,
                        self.pcon_field,
                        self.club_field,
                    ]
                ),
                ElevatedButton("Registrarse", on_click=self.register),
            ],
            visible=False,
            width=340,
        )

        self.controls = [
            AuthCard(
                [self.code_sectn, self.info_sectn],
                style="slim",
            ),
        ]

    def set_code(self, _) -> None:
        if self.code_field.value == "" or self.code_field.color == "red":
            error_snackbar(self.pg, "Ingrese un código válido")
            self.code_field.focus()
            return

        clubes = self.fb.db.child("clubs").get()
        try:
            if self.code_field.value not in set([u.val()["code"] for u in clubes]):
                error_snackbar(self.pg, "El código no existe")
                self.code_field.focus()
                return
        except:
            error_snackbar(self.pg, "El código no existe")
            self.code_field.focus()
            return

        self.pg.splash = ProgressBar()
        self.disabled = True
        self.pg.update()

        self.code_sectn.visible = False
        self.info_sectn.visible = True
        self.club_field.opacity = 0
        self.update()

        self.pg.splash = None
        self.disabled = False
        self.pg.update()

    def no_code(self, _):
        self.code_sectn.visible = False
        self.info_sectn.visible = True
        self.update()

    def register(self, _):
        if self.mail_field.value == "":
            error_snackbar(self.pg, "Ingrese un correo")
            self.mail_field.focus()
            return
        if self.mail_field.color == "red":
            error_snackbar(self.pg, "Ingrese un correo válido")
            self.mail_field.focus()
            return
        if self.user_field.value == "":
            error_snackbar(self.pg, "Ingrese un usuario")
            self.user_field.focus()
            return
        if self.user_field.color == "red":
            error_snackbar(self.pg, "Ingrese un usuario válido")
            self.user_field.focus()
            return
        if self.pass_field.value == "":
            error_snackbar(self.pg, "Ingrese una contraseña")
            self.pass_field.focus()
            return
        if self.pass_field.color == "red":
            error_snackbar(self.pg, "Ingrese una contraseña válida")
            self.pass_field.focus()
            return
        if self.pcon_field.value == "" or self.pcon_field.color == "red":
            error_snackbar(self.pg, "Ingrese contraseñas que coincida")
            self.pcon_field.focus()
            return
        if self.club_field.opacity == 1 and (
            self.club_field.value == "" or self.club_field.color == "red"
        ):
            error_snackbar(self.pg, "Ingrese un tag de club válido")
            self.club_field.focus()
            return

        self.pg.splash = ProgressBar()
        self.disabled = True
        self.pg.update()

        if self.club_field.opacity == 1:
            res = self.fb.register_new_user(
                self.club_field.value,
                self.user_field.value,
                self.mail_field.value,
                self.pass_field.value,
            )
        else:
            res = self.fb.register_code_user(
                self.code_field.value,
                self.user_field.value,
                self.mail_field.value,
                self.pass_field.value,
            )

        self.pg.splash = None
        self.disabled = False

        if res == True:
            self.pg.go("/")
        else:
            error_snackbar(self.pg, res)
