from adventure_game.models import Room


class GardensEast(Room):
    def __init__(self):
        super().__init__("gardens_east")
        self._is_completed = False
        self._is_bear_puzzle_completed = False

    def check_if_completed(self):
        if self._is_completed:
            return True

        for puzzle in self.puzzles:
            if puzzle.id == "bear_problem" and puzzle.is_solved and not self._is_bear_puzzle_completed:
                self._is_bear_puzzle_completed = True
                self.description = self.description.split(", under which Kirillina", 1)[0] + "."

        self._is_completed = self._is_bear_puzzle_completed

        return self._is_completed
