from flet import ButtonStyle, ElevatedButton, TextButton


class SecondaryButton(ElevatedButton):
    def __init__(self, text: str | None = None, on_click=None):
        super().__init__()
        colSelf = "secondary"

        self.text = text
        self.on_click = on_click
        self.style = ButtonStyle(
            color=colSelf,
            overlay_color=f"{colSelf},.15",
        )


class MyTextButton(TextButton):
    def __init__(self, text: str | None = None, on_click=None):
        super().__init__()
        colSelf = "outline"

        self.text = text
        self.on_click = on_click
        self.style = ButtonStyle(color=colSelf, overlay_color="transparent")
