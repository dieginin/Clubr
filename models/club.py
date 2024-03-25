from typing import Any, List

from utils import from_int, from_list, from_str

roles = {
    "notMember": "No Miembro",
    "member": "Miembro",
    "president": "Presidente",
    "senior": "Veterarno",
    "vicePresident": "Vice Presidente",
    "unknown": "Desconocido",
}


class Icon:
    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Icon":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return Icon(id)


class Member:
    def __init__(
        self,
        tag: str,
        name: str,
        name_color: str,
        role: str,
        trophies: int,
        icon: Icon,
    ) -> None:
        self.tag = tag
        self.name = name
        self.name_color = name_color
        self.role = role
        self.trophies = trophies
        self.icon = icon

    @staticmethod
    def from_dict(obj: Any) -> "Member":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag")).replace("#", "")
        name = from_str(obj.get("name"))
        name_color = from_str(obj.get("nameColor"))
        role = roles[from_str(obj.get("role"))]
        trophies = from_int(obj.get("trophies"))
        icon = Icon.from_dict(obj.get("icon"))
        return Member(tag, name, name_color, role, trophies, icon)


class Club:
    def __init__(
        self,
        tag: str,
        name: str,
        description: str,
        badge_id: int,
        trophies: int,
        members: List[Member],
    ) -> None:
        self.tag = tag
        self.name = name
        self.description = description
        self.badge_id = badge_id
        self.trophies = trophies
        self.members = members

    @staticmethod
    def from_dict(obj: Any) -> "Club":
        assert isinstance(obj, dict)
        tag = from_str(obj.get("tag"))
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        badge_id = from_int(obj.get("badgeId"))
        trophies = from_int(obj.get("trophies"))
        members = from_list(Member.from_dict, obj.get("members"))
        return Club(tag, name, description, badge_id, trophies, members)


def club_from_dict(s: Any) -> Club:
    return Club.from_dict(s)
