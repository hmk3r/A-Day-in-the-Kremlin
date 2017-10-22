from adventure_game.models import Room
from adventure_game.factories.contracts import IRoomFactory


class RoomFactory(IRoomFactory):
    def __init__(self):
        pass

    def create_room(self, room_id, name, description, exits=None, items=None, puzzles=None):
        return Room(room_id,
                    name,
                    description,
                    items=items,
                    exits=exits,
                    puzzles=puzzles)
