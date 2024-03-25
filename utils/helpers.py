from typing import Any, Callable, List, TypeVar

from flet import Page, SnackBar, Text

T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


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
