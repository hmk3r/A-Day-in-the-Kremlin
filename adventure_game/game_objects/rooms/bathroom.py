from adventure_game.models import Room


class Bathroom(Room):
    def __init__(self):
        super().__init__("bathroom")

    def check_if_completed(self):
        for puzzle in self.puzzles:
            if not puzzle.is_solved:
                return False

        return True
