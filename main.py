from flet import Page, Theme, app

from services import Router


class Main:
    def __init__(self, page: Page):
        super().__init__()

        page.title = "Clubr"
        page.theme = Theme(color_scheme_seed="cyan")

        self.__init_window__(page)
        Router(page)

    def __init_window__(self, page: Page):
        page.window_height = 700
        page.window_width = 900
        page.window_min_height = 700
        page.window_min_width = 900
        page.window_center()


app(Main)
