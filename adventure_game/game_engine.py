from adventure_game.contracts import *
from adventure_game.models import Puzzle
from adventure_game.factories import RoomFactory, ItemFactory, PlayerFactory
import adventure_game.constants as constants


class GameEngine(IEngine):
    rooms = {}
    items = {}
    puzzles = {}
    player = None

    def __init__(self, writer: IWriter, reader: IReader, parser: IParser, object_loader: IObjectsLoader):
        self.writer = writer
        self.reader = reader
        self.parser = parser
        self.object_loader = object_loader
        self.setup()

    def run(self):
        while True:
            self.print_current_game_info()

            user_input = self.reader.read_input("What would you ike to do? >")
            command = self.parser.parse_command(user_input)
            self.execute_command(command)

    def get_next_room(self, room_id):
        if room_id not in self.rooms:
            return None

        return self.rooms[room_id]

    def execute_go(self, direction):

        if direction not in self.player.location.exits:
            self.writer.write_separator()
            self.writer.write("Invalid direction")
            return

        next_room = self.get_next_room(self.player.location.exits[direction])

        if not next_room:
            self.writer.write_separator()
            self.writer.write("You can't go there")
            return

        self.player.move_to(next_room)

    def execute_take(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write("No such thing exists")
            return
        item = self.items[item_id]

        if item not in self.player.location.items:
            self.writer.write_separator()
            self.writer.write("There's no such item in the room")
            return

        self.player.location.items.remove(item)
        self.player.take_item(item)

    def execute_drop(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write("No such thing exists")
            return
        item = self.items[item_id]

        if item not in self.player.inventory:
            self.writer.write_separator()
            self.writer.write("You don't have this item")
            return

        self.player.inventory.remove(item)
        self.player.location.items.append(item)

    def execute_solve(self, puzzle_id):
        if puzzle_id not in self.puzzles:
            self.writer.write_separator()
            self.writer.write("There's no such puzzle")
            return
        puzzle = self.puzzles[puzzle_id]

        if puzzle not in self.player.location.puzzles:
            self.writer.write_separator()
            self.writer.write("You can't solve this puzzle right now")
            return

        if puzzle.is_solved:
            self.writer.write_separator()
            self.writer.write("You've already solved this puzzle")
            return

        self.writer.write_separator()
        self.writer.write(puzzle.name.upper())

        self.writer.write_separator()
        self.writer.write(puzzle.description)

        if puzzle.reward:
            self.writer.write("You'll get {0} if you solve this correctly".format(puzzle.reward.name))

        self.writer.write_separator()
        self.writer.write("Possible answers:")
        for possible_answer in puzzle.possible_answers:
            self.writer.write(possible_answer)

        answer_raw = self.reader.read_input("Answer: ")
        answer = self.parser.normalise_string(answer_raw)
        if puzzle.answer_is_correct(answer):
            self.writer.write_separator()
            self.writer.write("Correct answer!")
            if puzzle.reward:
                self.writer.write("Here's {0}".format(puzzle.reward.name))
                self.player.inventory.append(puzzle.reward)
        else:
            self.writer.write("Wrong answer!")

    def execute_command(self, command):

        if 0 == len(command):
            return

        if command[0] == constants.COMMAND_GO:
            if len(command) > 1:
                self.execute_go(command[1])
            else:
                self.writer.write("Go where?")

        elif command[0] == constants.COMMAND_TAKE:
            if len(command) > 1:
                self.execute_take(command[1])
            else:
                self.writer.write("Take what?")

        elif command[0] == constants.COMMAND_DROP:
            if len(command) > 1:
                self.execute_drop(command[1])
            else:
                self.writer.write("Drop what?")

        elif command[0] == constants.COMMAND_SOLVE:
            if len(command) > 1:
                self.execute_solve(command[1])
            else:
                self.writer.write("Solve what?")
        else:
            self.writer.write("This makes no sense.")

    def print_current_game_info(self):
        self.writer.write_separator()
        self.writer.write(self.player.location.name.upper())
        self.writer.write_separator()

        self.writer.write(self.player.location.description)
        self.writer.write_separator()

        self.writer.write("You can:")

        for puzzle in self.player.location.puzzles:
            if not puzzle.is_solved:
                self.writer.write("Type SOLVE {0} to solve {1}.".format(puzzle.id.upper(), puzzle.name))

        for item in self.player.location.items:
            self.writer.write("Type TAKE {0} to take {1}".format(item.id.upper(), item.name))

        for i in self.player.inventory:
            self.writer.write("Type DROP {0} to drop {1}".format(i.id.upper(), i.name))

        for direction in self.player.location.exits:
            if not self.player.location.exits[direction]:
                continue

            room_exit = self.rooms[self.player.location.exits[direction]]

            self.writer.write("Type GO {0} to go to {1}".format(direction.upper(), room_exit.name))

    def setup(self):
        [self.items, self.puzzles, self.rooms, self.player] = self.object_loader.load()