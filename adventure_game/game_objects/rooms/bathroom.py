from adventure_game.models import Room
from adventure_game.exceptions import PlayerDeadException


class Bathroom(Room):
    def __init__(self):
        super().__init__("bathroom")
        self.is_bath_power_in_room = False

    def check_if_completed(self):
        if self.is_bath_power_in_room:
            return True
        for item in self.items:
            if item.id == "bubblebath_power":
                self.is_bath_power_in_room = True
                self.description += " You've chosen the right bubblebath"
                self.items.remove(item)
            elif item.id == "bubblebath_lemon":
                raise PlayerDeadException("Stalin hates lemons. You're going to GULAG!")

        return self.is_bath_power_in_room
