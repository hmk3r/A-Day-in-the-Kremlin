from adventure_game.contracts import *
from adventure_game.factories import RoomFactory, ItemFactory, PlayerFactory
import adventure_game.constants as constants


class GameEngine(IEngine):
    rooms = {}
    items = {}
    player = None

    def __init__(self, writer: IWriter, reader: IReader, parser: IParser):
        self.writer = writer
        self.reader = reader
        self.parser = parser
        self.setup()

    def run(self):
        while True:
            self.print_current_game_info()

            user_input = self.reader.read_input("What would you ike to do? ")
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

        else:
            self.writer.write("This makes no sense.")

    def print_current_game_info(self):
        self.writer.write_separator()
        self.writer.write(self.player.location.name.upper())
        self.writer.write_separator()

        self.writer.write(self.player.location.description)
        self.writer.write_separator()

        self.writer.write("You can:")
        for item in self.player.location.items:
            self.writer.write("Type TAKE {0} to take {1}".format(item.id, item.name))

        for i in self.player.inventory:
            self.writer.write("Type DROP {0} to drop {1}".format(i.id, i.name))

        for direction in self.player.location.exits:
            if not self.player.location.exits[direction]:
                continue

            room_exit = self.rooms[self.player.location.exits[direction]]

            self.writer.write("Type GO {0} to go to {1}".format(direction.upper(), room_exit.name))

    def setup(self):
        """ A temporary solution until I find out how to load all the data from an external file.
        Just ignore this for now.
        """
        item_factory = ItemFactory()
        player_factory = PlayerFactory()
        room_factory = RoomFactory(constants)

        for x in range(0, 6):
            new_item = item_factory.create_item(str(x), "Item {0}".format(x), "Cool item number {0}".format(x))
            self.items[str(x)] = new_item

        library_exits_scheme = \
            room_factory.create_room_exits(
                east_room_id="restaurant",
                west_room_id="lab",
                north_room_id="workshop",
                south_room_id="office")

        library = \
            room_factory.create_room(
                "library",
                "Cardiff library",
                "You can find books here",
                library_exits_scheme,
                [self.items["0"], self.items["2"]])
        self.rooms[library.id] = library

        restaurant_exits_scheme = room_factory.create_room_exits(west_room_id="library")
        restaurant = room_factory.create_room("restaurant", "The Restaurant", "Drink and eat", restaurant_exits_scheme)
        self.rooms[restaurant.id] = restaurant

        lab_exits_scheme = room_factory.create_room_exits(east_room_id="library")
        lab = room_factory.create_room("lab", "PC Lab", "A room full of computers", lab_exits_scheme, [self.items["1"]])
        self.rooms[lab.id] = lab

        workshop_exits_scheme = room_factory.create_room_exits(south_room_id="library")
        workshop = \
            room_factory.create_room("workshop", "The Workshop", "vrum vrum", workshop_exits_scheme,
                                     [self.items["3"], self.items["5"]])
        self.rooms[workshop.id] = workshop

        office = \
            room_factory.create_room("office", "The main office", "You are trapped. There are no exits",
                                     items=[self.items["4"]])
        self.rooms[office.id] = office

        self.player = player_factory.create_player("John Doe", library)
