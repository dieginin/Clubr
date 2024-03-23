from flet import Page, RouteChangeEvent

from views import *

from .fyrebase import Fyrebase

routes = {
    "/brawlers": BrawlersView,
    "/forgot": ForgotView,
    "/": HomeView,
    "/login": LoginView,
    "/members": MembersView,
    "/no_club": NoClubView,
    "/past_members": PastMembersView,
    "/register": RegisterView,
    "/valorate": ValorateView,
}


class Router:
    def __init__(self, page: Page):
        self.page = page
        self.page.on_route_change = self.route_change

        self.fb = Fyrebase(page)
        if self.fb.active_sesion():
            self.page.go("/")
        else:
            self.page.go("/login")

    def route_change(self, e: RouteChangeEvent):
        self.page.views.clear()
        self.page.views.append(routes[e.route](self.page, self.fb))
        self.page.update()
