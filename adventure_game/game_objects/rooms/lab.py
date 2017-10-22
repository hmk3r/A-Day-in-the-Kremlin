from adventure_game.models import Room


class Lab(Room):
    def __init__(self):
        super().__init__("lab", "", "")

    @property
    def is_completed(self):
        print("Customise 'completed' conditions here. This room. for an example, never gets completed")
        return False
