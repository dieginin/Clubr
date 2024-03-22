from flet import Page, View

from services import Fyrebase


class PastMembersView(View):
    def __init__(self, page: Page, fb: Fyrebase):
        super().__init__()

        self.route = "/past_members"
        self.controls = []
