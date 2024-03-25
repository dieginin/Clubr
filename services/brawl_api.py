import requests

from models import Battlelog, Club, Player
from utils import ROYALE_TOKEN, URL_ROYALE


class BrawlAPI:
    @staticmethod
    def is_valid_club(tag: str) -> bool:
        res = requests.get(
            URL_ROYALE + "clubs/%23" + tag,
            headers={"Authorization": f"Bearer {ROYALE_TOKEN}"},
        )

        return res.status_code == 200

    @staticmethod
    def is_valid_player(tag: str) -> bool:
        res = requests.get(
            URL_ROYALE + "players/%23" + tag,
            headers={"Authorization": f"Bearer {ROYALE_TOKEN}"},
        )

        return res.status_code == 200

    def _request(self, endpoint: str, tag: str, extra_key: str = ""):
        url = URL_ROYALE + endpoint + "%23" + tag + extra_key
        res = requests.get(
            url,
            headers={"Authorization": f"Bearer {ROYALE_TOKEN}"},
        )

        if res.status_code == 200 or res.status_code == 404:
            return res.json()
        else:
            raise Exception("Error en petición")

    def club(self, tag) -> Club:
        data = self._request("clubs/", tag)
        return Club.from_dict(data)

    def player(self, tag: str) -> Player:
        data = self._request("players/", tag)
        return Player.from_dict(data)

    def battlelog(self, tag: str) -> Battlelog:
        data = self._request("players/", tag, "/battlelog")
        return Battlelog.from_dict(data)
