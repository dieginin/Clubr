from typing import Any, List

from utils import from_int, from_list, from_str


class Brawler:
    def __init__(self, id: int, name: str, power: int, trophies: int) -> None:
        self.id = id
        self.name = name
        self.power = power
        self.trophies = trophies

    @staticmethod
    def from_dict(obj: Any) -> "Brawler":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        power = from_int(obj.get("power"))
        trophies = from_int(obj.get("trophies"))
        return Brawler(id, name, power, trophies)


class StarPlayer:
    def __init__(self, tag: str, name: str, brawler: Brawler) -> None:
        self.tag = tag
        self.name = name
        self.brawler = brawler

    @staticmethod
    def from_dict(obj: Any) -> "StarPlayer":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        brawler = Brawler.from_dict(obj.get("brawler"))
        return StarPlayer(tag, name, brawler)


class Battle:
    def __init__(
        self,
        mode: str,
        type: str,
        result: str,
        duration: int,
        trophy_change: int,
        star_player: StarPlayer,
        teams: List[List[StarPlayer]],
    ) -> None:
        self.mode = mode
        self.type = type
        self.result = result
        self.duration = duration
        self.trophy_change = trophy_change
        self.star_player = star_player
        self.teams = teams

    @staticmethod
    def from_dict(obj: Any) -> "Battle":
        assert isinstance(obj, dict)
        mode = from_str(obj.get("mode"))
        type = from_str(obj.get("type"))
        result = from_str(obj.get("result"))
        duration = from_int(obj.get("duration"))
        trophy_change = from_int(obj.get("trophyChange"))
        star_player = StarPlayer.from_dict(obj.get("starPlayer"))
        teams = from_list(
            lambda x: from_list(StarPlayer.from_dict, x), obj.get("teams")
        )
        return Battle(mode, type, result, duration, trophy_change, star_player, teams)


class Event:
    def __init__(self, id: int, mode: str, map: str) -> None:
        self.id = id
        self.mode = mode
        self.map = map

    @staticmethod
    def from_dict(obj: Any) -> "Event":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        mode = from_str(obj.get("mode"))
        map = from_str(obj.get("map"))
        return Event(id, mode, map)


class Battlelog:
    def __init__(self, battle_time: str, event: Event, battle: Battle) -> None:
        self.battle_time = battle_time
        self.event = event
        self.battle = battle

    @staticmethod
    def from_dict(obj: Any) -> "Battlelog":
        assert isinstance(obj, dict)
        battle_time = from_str(obj.get("battleTime"))
        event = Event.from_dict(obj.get("event"))
        battle = Battle.from_dict(obj.get("battle"))
        return Battlelog(battle_time, event, battle)


def battlelog_from_dict(s: Any) -> Battlelog:
    return Battlelog.from_dict(s)
