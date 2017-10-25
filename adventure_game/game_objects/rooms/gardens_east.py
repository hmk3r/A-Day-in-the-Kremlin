from adventure_game.models import Room


class GardensEast(Room):
    def __init__(self):
        super().__init__("gardens_east")

    def check_if_completed(self):
        for puzzle in self.puzzles:
            if not puzzle.is_solved:
                return False

        self.description = self.description.split(", under which Kirillina", 1)[0]
        return True
