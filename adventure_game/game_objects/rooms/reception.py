from adventure_game.models import Room


class Reception(Room):
    def __init__(self):
        super().__init__("reception")
        self._is_completed = False
        self._is_bear_in_room = False

    def check_if_completed(self):
        if self._is_completed:
            return True

        for item in self.items:
            if item.id == "bear" and not self._is_bear_in_room:
                self._is_bear_in_room = True
                self.items.remove(item)
                self.description = self.description.split("It's open and", 1)[0] + "Kirillina's in there and she seems to be sleeping."

        self._is_completed = self._is_bear_in_room

        return self._is_completed
