from flet import ElevatedButton, Page, View

from services import Fyrebase


class HomeView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()
        self.fb = fb
        self.pg = page

        self.route = "/home"
        self.controls = [ElevatedButton("Logout", on_click=self.log_out)]

    def log_out(self, _):
        self.fb.sign_out()
        self.pg.go("/login")
        self.pg.update()
