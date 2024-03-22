import re


class Validator:
    @staticmethod
    def is_valid_name(name) -> bool:
        return (
            isinstance(name, str)
            and len(name.strip()) >= 1
            and all(c.isalpha() or c.isspace() or c in "-'." for c in name)
        )

    @staticmethod
    def is_valid_username(name) -> bool:
        return (
            isinstance(name, str)
            and len(name.strip()) >= 3
            and all(c.isalpha() for c in name)
        )

    @staticmethod
    def is_valid_mail(email) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_password(password) -> bool:
        return (
            isinstance(password, str)
            and len(password.strip()) >= 6
            and any(c.isnumeric() for c in password)
        )

    @staticmethod
    def is_valid_code(code) -> bool:
        pattern = r"(#{0,1})[A-Za-z0-9]+"
        return len(code.strip()) >= 6 and re.match(pattern, code) is not None
