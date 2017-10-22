from adventure_game.models import Room


class Library(Room):
    def __init__(self):
        super().__init__("library",
                         "Cardiff library",
                         "You can find books here",
                         east_room_id="restaurant",
                         west_room_id="lab",
                         north_room_id="workshop",
                         south_room_id="office",
                         items=["book"])
