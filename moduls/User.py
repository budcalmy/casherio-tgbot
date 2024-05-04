from moduls.Waste import Waste


class User:

    def __init__(self, name: str, id: int, wastes: list[Waste]):
        self.name = name
        self.id = id
        self.wastes = wastes

