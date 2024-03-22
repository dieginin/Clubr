from typing import List, Literal

from flet import (
    Card,
    Column,
    Control,
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    Row,
)


class CenterColumn(Column):
    def __init__(
        self,
        controls: List[Control] | None = None,
        visible: bool | None = None,
        width: OptionalNumber = None,
    ):
        super().__init__()
        self.controls = controls
        self.alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.visible = visible
        self.width = width


class CenterRow(Row):
    def __init__(
        self, controls: List[Control] | None = None, visible: bool | None = None
    ):
        super().__init__()
        self.controls = controls
        self.alignment = MainAxisAlignment.CENTER
        self.vertical_alignment = CrossAxisAlignment.CENTER
        self.visible = visible


class AuthCard(Card):
    def __init__(
        self,
        controls: List[Control] | None = None,
        style: Literal["slim", "fat"] = "fat",
    ):
        super().__init__()

        self.content = CenterRow(controls) if style == "fat" else CenterColumn(controls)
        self.elevation = 3
        self.height = 500
        self.width = 700 if style == "fat" else 400
