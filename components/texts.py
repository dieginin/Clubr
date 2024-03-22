from flet import FontWeight, Text, TextAlign, TextStyle


class Title(Text):
    def __init__(self, value: str | None = None):
        super().__init__()

        self.color = "outline"
        self.style = TextStyle(size=27, weight=FontWeight.W_100)
        self.text_align = TextAlign.CENTER
        self.value = value
