from adventure_game.models import Room


class Workshop(Room):
    def __init__(self):
        super().__init__("workshop", "The Workshop", "vrum vrum", south_room_id="library")
