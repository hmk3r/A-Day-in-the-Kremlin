from adventure_game.models import Room


class Office(Room):
    def __init__(self):
        super().__init__("office", "The main office", "You are trapped. There are no exits", items=["laptop"])
