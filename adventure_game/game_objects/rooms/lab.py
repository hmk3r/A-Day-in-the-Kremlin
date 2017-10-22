from adventure_game.models import Room


class Lab(Room):
    def __init__(self):
        super().__init__("lab",
                         "PC Lab",
                         "A room full of computers",
                         east_room_id="library",
                         items=["flashlight"],
                         puzzles=["harderquest", "quest"])
