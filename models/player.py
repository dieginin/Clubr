from typing import Any, List

from utils import from_bool, from_int, from_list, from_str


class Gadget:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> "Gadget":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        return Gadget(id, name)


class Gear:
    def __init__(self, id: int, name: str, level: int) -> None:
        self.id = id
        self.name = name
        self.level = level

    @staticmethod
    def from_dict(obj: Any) -> "Gear":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        level = from_int(obj.get("level"))
        return Gear(id, name, level)


class Brawler:
    def __init__(
        self,
        id: int,
        name: str,
        power: int,
        rank: int,
        trophies: int,
        highest_trophies: int,
        gears: List[Gear],
        star_powers: List[Gadget],
        gadgets: List[Gadget],
    ) -> None:
        self.id = id
        self.name = name
        self.power = power
        self.rank = rank
        self.trophies = trophies
        self.highest_trophies = highest_trophies
        self.gears = gears
        self.star_powers = star_powers
        self.gadgets = gadgets

    @staticmethod
    def from_dict(obj: Any) -> "Brawler":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        power = from_int(obj.get("power"))
        rank = from_int(obj.get("rank"))
        trophies = from_int(obj.get("trophies"))
        highest_trophies = from_int(obj.get("highestTrophies"))
        gears = from_list(Gear.from_dict, obj.get("gears"))
        star_powers = from_list(Gadget.from_dict, obj.get("starPowers"))
        gadgets = from_list(Gadget.from_dict, obj.get("gadgets"))
        return Brawler(
            id,
            name,
            power,
            rank,
            trophies,
            highest_trophies,
            gears,
            star_powers,
            gadgets,
        )


class Club:
    def __init__(self, tag: str, name: str) -> None:
        self.tag = tag
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> "Club":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        return Club(tag, name)


class Icon:
    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Icon":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return Icon(id)


class Player:
    def __init__(
        self,
        tag: str,
        name: str,
        name_color: str,
        icon: Icon,
        trophies: int,
        highest_trophies: int,
        is_qualified: bool,
        the_3_vs3_victories: int,
        solo_victories: int,
        duo_victories: int,
        club: Club,
        brawlers: List[Brawler],
    ) -> None:
        self.tag = tag
        self.name = name
        self.name_color = name_color
        self.icon = icon
        self.trophies = trophies
        self.highest_trophies = highest_trophies
        self.is_qualified = is_qualified
        self.the_3_vs3_victories = the_3_vs3_victories
        self.solo_victories = solo_victories
        self.duo_victories = duo_victories
        self.club = club
        self.brawlers = brawlers

    @staticmethod
    def from_dict(obj: Any) -> "Player":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        name_color = from_str(obj.get("nameColor"))
        icon = Icon.from_dict(obj.get("icon"))
        trophies = from_int(obj.get("trophies"))
        highest_trophies = from_int(obj.get("highestTrophies"))
        is_qualified = from_bool(obj.get("isQualifiedFromChampionshipChallenge"))
        the_3_vs3_victories = from_int(obj.get("3vs3Victories"))
        solo_victories = from_int(obj.get("soloVictories"))
        duo_victories = from_int(obj.get("duoVictories"))
        club = Club.from_dict(obj.get("club"))
        brawlers = from_list(
            Brawler.from_dict,
            sorted(obj.get("brawlers", {}), key=lambda x: x["trophies"], reverse=True),
        )
        return Player(
            tag,
            name,
            name_color,
            icon,
            trophies,
            highest_trophies,
            is_qualified,
            the_3_vs3_victories,
            solo_victories,
            duo_victories,
            club,
            brawlers,
        )


def player_from_dict(s: Any) -> Player:
    return Player.from_dict(s)
