from flet import Page, View

from services import Fyrebase


class NoClubView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()

        self.route = "/no_club"
        self.controls = []
