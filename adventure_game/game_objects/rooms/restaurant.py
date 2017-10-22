from adventure_game.models import Room


class Restaurant(Room):
    def __init__(self):
        super().__init__("restaurant",
                         "The Restaurant",
                         "Drink and eat",
                         west_room_id="library",
                         items=["food", "drink"],
                         puzzles=["puzzle"])
