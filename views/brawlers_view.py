from flet import Page, View

from services import Fyrebase


class BrawlersView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()

        self.route = "/brawlers"
        self.controls = []
