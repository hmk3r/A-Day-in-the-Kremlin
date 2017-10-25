from adventure_game.contracts import *
from adventure_game.exceptions import PlayerDeadException
import adventure_game.constants as constants


class GameEngine(IEngine):
    rooms = {}
    items = {}
    puzzles = {}
    player = None

    def __init__(self, writer: IWriter, reader: IReader, parser: IParser, objects_loader: IObjectsLoader):
        self.writer = writer
        self.reader = reader
        self.parser = parser
        self.objects_loader = objects_loader
        self.setup()

    def run(self):
        try:
            while True:
                self.print_current_game_info()

                user_input = self.reader.read_input("What would you ike to do? >")
                command = self.parser.parse_command(user_input)
                self.writer.clear()
                self.execute_command(command)
                if self.check_win():
                    # Display end game screen
                    raise PlayerDeadException("You won!")
        except PlayerDeadException as player_dead_exception:
            self.writer.write_separator()
            self.writer.write(str(player_dead_exception))
            self.writer.write_separator()
        except KeyboardInterrupt:
            self.writer.write_separator()
            self.writer.write_separator()
            self.writer.write("Thanks for playing! You're welcome back anytime!")
            self.writer.write_separator()

    def get_next_room(self, room_id):
        if room_id not in self.rooms:
            return None

        return self.rooms[room_id]

    def check_win(self):
        is_completed = True
        for room_id in self.rooms:
            if not self.rooms[room_id].check_if_completed():
                return False
            is_completed = is_completed and self.rooms[room_id].check_if_completed()
        return is_completed

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

    def execute_look(self, item_id):
        if item_id not in self.items:
            print("This item does not exist")
            return
        item = self.items[item_id]

        if (item in self.player.inventory) or (item in self.player.location.items):
            print(item.description)
        else:
            print("You can't inspect this item right now.")
        
        
            


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

        if not set(puzzle.required_items).issubset(self.player.inventory):
            self.writer.write_separator()
            self.writer.write("You don't have the required items to complete this puzzle!")
            self.writer.write("Think logically and you'll find out what you need.")
            return

        self.writer.write_separator()
        self.writer.write(puzzle.name.upper())

        self.writer.write_separator()
        if puzzle.is_annoying:
            self.writer.write_slowly(puzzle.description)
        else:
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
            if puzzle.win_message:
                self.writer.write(puzzle.win_message)
            if puzzle.reward:
                self.player.take_item(puzzle.reward)
            if puzzle.takes_items:
                for used_item in puzzle.required_items:
                    self.player.drop_item(used_item)
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
        
        elif command[0] == constants.COMMAND_LOOK:
            if len(command) > 1:
                self.execute_look(command[1])
            else:
                self.writer.write("Look at what?")
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
                self.writer.write("Type SOLVE {0} to {1}.".format(puzzle.id.upper(), puzzle.name))

        self.writer.write("Type LOOK AT {ITEM} to inspect an item in your inventory or room.")
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
        [self.items, self.puzzles, self.rooms, self.player] = self.objects_loader.load()
