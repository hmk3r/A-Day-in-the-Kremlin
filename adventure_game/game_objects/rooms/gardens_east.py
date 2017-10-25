from adventure_game.models import Room
from adventure_game.exceptions import PlayerDeadException

class gardens_east(Room):
	def __init__(self):
        super().__init__("gardens_east")
        self.is_lead_in_room = False
        self.is_collar_in_room = False

    def check_if_completed(self):
    	if self.is_collar_in_room:
            return True
        for item in self.items:
            if item.id == "collar":
            	self.is_collar_in_room = True
            	self.description += " You've managed to get the collar on the bear."
            	self.items.remove(item)
        return self.is_collar_in_room