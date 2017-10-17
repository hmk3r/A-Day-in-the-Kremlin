class RoomExitsScheme:

    def __init__(self, east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        self.east_room_id = east_room_id
        self.west_room_id = west_room_id
        self.north_room_id = north_room_id
        self.south_room_id = south_room_id


class Room:

    def __init__(self, room_id, name, description, room_exits_scheme=RoomExitsScheme(), items=[]):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = room_exits_scheme
        self.items = items
