from adventure_game.models import Room

BEAR_PUZZLE_ID = "bear_problem"
SPLIT_POINT_ROOM_DESCRIPTION = ", under which Kirillina"
END_SENTENCE = "."


class GardensEast(Room):
    def __init__(self):
        super().__init__("gardens_east")
        self._is_completed = False
        self._is_bear_puzzle_completed = False

    def check_if_completed(self):
        if self._is_completed:
            return True

        for puzzle in self.puzzles:
            if puzzle.id == BEAR_PUZZLE_ID and puzzle.is_solved and not self._is_bear_puzzle_completed:
                self._is_bear_puzzle_completed = True
                self.description = self.description.split(SPLIT_POINT_ROOM_DESCRIPTION, 1)[0] + END_SENTENCE

        self._is_completed = self._is_bear_puzzle_completed

        return self._is_completed
