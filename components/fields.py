from flet import InputBorder, InputFilter, TextAlign, TextCapitalization, TextField

from utils import Validator


class _Field(TextField):
    def __init__(self, on_submit=None):
        super().__init__()
        self.border = InputBorder.UNDERLINE
        self.border_color = "primary"
        self.color = "secondary"
        self.cursor_color = "primary"
        self.focused_color = "secondary"

        self.on_change = lambda _: self.validate()
        self.on_submit = on_submit
        self.text_align = TextAlign.CENTER
        self.validator = Validator()
        self.validation_func = None

    def validate(self):
        if self.validation_func:
            if not self.validation_func(self.value):
                self.border_color = "red"
                self.color = "red"
                self.focused_color = "red"
            else:
                self.border_color = "primary"
                self.color = "secondary"
                self.focused_color = "secondary"
        self.update()


class CodeField(_Field):
    def __init__(self, hint_text: str | None = None, on_submit=None):
        super().__init__(on_submit=on_submit)
        self.autofocus = True
        self.capitalization = TextCapitalization.CHARACTERS
        self.counter_text = " "
        self.hint_text = hint_text
        self.max_length = 10
        self.prefix_icon = "tag"
        self.validation_func = self.validator.is_valid_code
        self.width = 175
        self.input_filter = InputFilter(
            regex_string=r"(#{0,1})[A-Za-z0-9]+", allow=True, replacement_string=""
        )


class UserField(_Field):
    def __init__(
        self,
        hint_text: str | None = None,
        on_submit=None,
        autofocus: bool | None = None,
    ):
        super().__init__(on_submit=on_submit)
        self.autofocus = autofocus
        self.hint_text = hint_text
        self.prefix_icon = "person"
        self.validation_func = self.validator.is_valid_username


class MailField(_Field):
    def __init__(self, hint_text: str | None = None, on_submit=None):
        super().__init__(on_submit=on_submit)
        self.autofocus = True
        self.hint_text = hint_text
        self.prefix_icon = "email_outlined"
        self.validation_func = self.validator.is_valid_mail


class PasswordField(_Field):
    def __init__(self, hint_text: str | None = None, on_submit=None):
        super().__init__(on_submit=on_submit)
        self.hint_text = hint_text
        self.prefix_icon = "password"
        self.password = True
        self.can_reveal_password = True
        self.helper_text = "mínimo 6 caracteres, con 1 número"
        self.validation_func = self.validator.is_valid_password


class RepeatPasswordField(_Field):
    def __init__(
        self,
        original_field: PasswordField,
        hint_text: str | None = None,
        on_submit=None,
    ):
        super().__init__(on_submit=on_submit)
        self.hint_text = hint_text
        self.prefix_icon = "password"
        self.password = True
        self.can_reveal_password = True
        self.helper_text = "las contraseñas deben de ser iguales"
        self.validation_func = self.validate_password
        self.original_field = original_field

    @property
    def ofv(self):
        return self.original_field.value

    def validate_password(self, _):
        return self.ofv == self.value
