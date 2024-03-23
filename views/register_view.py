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

        self.init_ui()

    def init_ui(self):
        self.setup_layout()
        self.setup_fields()
        self.setup_controls()

    def setup_layout(self):
        self.route = "/register"
        self.bgcolor = "primary"
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

    def setup_fields(self):
        self.code_field = CodeField("Código", self.handle_code_input)
        self.club_field = CodeField("Club Tag", self.handle_register)
        self.mail_field = MailField("Correo", self.handle_register)
        self.pass_field = PasswordField("Contraseña", self.handle_register)
        self.pcon_field = RepeatPasswordField(
            self.pass_field, "Confirmar Contraseña", self.handle_register
        )
        self.user_field = UserField("Usuario", self.handle_register)

    def setup_controls(self):
        self.code_sectn = CenterColumn(
            [
                Title("Ingresa el código de tu club"),
                self.code_field,
                ElevatedButton("Guardar", on_click=self.handle_code_input),
                SecondaryButton("No tengo código", on_click=self.no_code),
            ],
            visible=True,
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
                ElevatedButton("Registrarse", on_click=self.handle_register),
            ],
            visible=False,
            width=340,
        )

        self.controls = [AuthCard([self.code_sectn, self.info_sectn], style="slim")]

        self.floating_action_button = FloatingActionButton(
            "Regresar", on_click=lambda _: self.pg.go("/login"), width=85
        )

    def handle_code_input(self, _):
        code = self.code_field.value
        if code == "" or self.invalid_code(code):
            error_snackbar(self.pg, "Ingrese un código válido")
            self.code_field.focus()
            return
        self.switch_views()

    def switch_views(self, option="code"):
        if option == "code":
            self.pg.splash = ProgressBar()
            self.disabled = True
            self.pg.update()

            self.code_sectn.visible = False
            self.info_sectn.visible = True
            self.club_field.opacity = 0
            self.update()

            self.pg.splash = None
            self.disabled = False
        else:
            self.code_sectn.visible = False
            self.info_sectn.visible = True
        self.pg.update()

    def no_code(self, _):
        self.switch_views("nocode")

    def invalid_code(self, code):
        try:
            return code not in {
                u.val()["code"] for u in self.fb.db.child("clubs").get()
            }
        except:
            return True

    def handle_register(self, _):
        if not self.validate_fields():
            return

        self.pg.splash = ProgressBar()
        self.disabled = True
        self.pg.update()

        res = self.register_user()

        self.pg.splash = None
        self.disabled = False

        if res == True:
            self.pg.go("/")
        else:
            error_snackbar(self.pg, res)

    def validate_fields(self):
        fields = [
            (self.mail_field, "Ingrese un correo válido"),
            (self.user_field, "Ingrese un usuario válido"),
            (self.pass_field, "Ingrese una contraseña válida"),
            (self.pcon_field, "Ingrese contraseñas que coincidan"),
        ]

        if self.club_field.opacity == 1:
            fields.append((self.club_field, "Ingrese un tag de club válido"))

        for field, error_message in fields:
            if field.value == "" or field.color == "red":
                error_snackbar(self.pg, error_message)
                field.focus()
                return False

        return True

    def register_user(self):
        if self.club_field.opacity == 1:
            return self.fb.register_club(
                self.club_field.value,
                self.user_field.value,
                self.mail_field.value,
                self.pass_field.value,
            )
        else:
            return self.fb.add_member(
                self.code_field.value,
                self.user_field.value,
                self.mail_field.value,
                self.pass_field.value,
            )
