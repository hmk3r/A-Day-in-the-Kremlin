from adventure_game.models.contracts import IRoom


class Room(IRoom):

    def __init__(self, room_id, name, description, room_exits_scheme, items):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = room_exits_scheme
        self.items = items
