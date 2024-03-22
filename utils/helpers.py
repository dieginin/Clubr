from flet import Page, SnackBar, Text


def error_snackbar(page: Page, message: str | None = None):
    page.snack_bar = SnackBar(
        Text(message, color="onerrorcontainer"), bgcolor="errorcontainer"
    )
    page.snack_bar.open = True
    page.update()


def success_snackbar(page: Page, message: str | None = None):
    page.snack_bar = SnackBar(
        Text(message, color="onprimarycontainer"), bgcolor="primarycontainer"
    )
    page.snack_bar.open = True
    page.update()
