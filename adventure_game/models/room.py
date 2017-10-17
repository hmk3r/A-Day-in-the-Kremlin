from .room_exits_scheme import RoomExitsScheme


class Room:

    def __init__(self, room_id, name, description, room_exits_scheme=RoomExitsScheme(), items=[]):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = room_exits_scheme
        self.items = items
