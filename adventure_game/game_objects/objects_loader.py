from adventure_game.contracts import IObjectsLoader
from adventure_game.factories.contracts import *
from bs4 import BeautifulSoup
import os


class ObjectsLoader(IObjectsLoader):

    def __init__(self,
                 item_factory: IItemFactory,
                 puzzle_factory: IPuzzleFactory,
                 room_factory: IRoomFactory,
                 player_factory: IPlayerFactory):
        self.raw_items = {}
        self.raw_puzzles = {}
        self.raw_rooms = {}
        self.raw_player = {}
        self.item_factory = item_factory
        self.puzzle_factory = puzzle_factory
        self.room_factory = room_factory
        self.player_factory = player_factory
        self.items_as_objects = {}
        self.puzzles_as_objects = {}
        self.rooms_as_objects = {}
        self.player_as_object = None

    def load(self):
        self._parse_xml(os.path.abspath("adventure_game/game_objects/data.xml"))
        self.convert_objects()

        return [self.items_as_objects,
                self.puzzles_as_objects,
                self.rooms_as_objects,
                self.player_as_object]

    def convert_objects(self):
        self.convert_items()
        self.convert_puzzles()
        self.convert_rooms()
        self.convert_player()

    def convert_items(self):
        for item_id in self.raw_items:
            item_object = self.item_factory.create_item(item_id,
                                                        self.raw_items[item_id]["name"],
                                                        self.raw_items[item_id]["description"])
            self.items_as_objects[item_id] = item_object

    def convert_puzzles(self):
        for puzzle_id in self.raw_puzzles:
            puzzle_object = self.puzzle_factory.create_puzzle(puzzle_id,
                                                              self.raw_puzzles[puzzle_id]["name"],
                                                              self.raw_puzzles[puzzle_id]["description"],
                                                              self.raw_puzzles[puzzle_id]["possible_answers"],
                                                              self.raw_puzzles[puzzle_id]["correct_answer"])

            reward_item_id = self.raw_puzzles[puzzle_id]["reward_item_id"]
            if reward_item_id:
                puzzle_object.reward = self.items_as_objects[reward_item_id]

            self.puzzles_as_objects[puzzle_id] = puzzle_object

    def convert_rooms(self):
        for room_id in self.raw_rooms:

            room_items = []
            for item_id in self.raw_rooms[room_id]["room_item_ids"]:
                room_items.append(self.items_as_objects[item_id])

            room_puzzles = []
            for puzzle_id in self.raw_rooms[room_id]["room_puzzles_ids"]:
                room_puzzles.append(self.puzzles_as_objects[puzzle_id])

            room_as_object = self.room_factory.create_room(room_id,
                                                           self.raw_rooms[room_id]["name"],
                                                           self.raw_rooms[room_id]["description"],
                                                           exits=self.raw_rooms[room_id]["exits"],
                                                           items=room_items,
                                                           puzzles=room_puzzles)

            self.rooms_as_objects[room_id] = room_as_object

    def convert_player(self):
        player_inventory = []
        for item_id in self.raw_player["inventory"]:
            player_inventory.append(self.items_as_objects[item_id])

        player_location = self.rooms_as_objects[self.raw_player["location"]]

        self.player_as_object = self.player_factory.create_player(self.raw_player["name"],
                                                                  player_location,
                                                                  inventory=player_inventory)

    def _parse_xml(self, file_name):
        with open(file_name) as file:
            xml = BeautifulSoup(file, "html.parser")

        items = xml.data.items.find_all("item")
        for item in items:
            item_id = item["id"]
            item_name = item.find('name').string
            item_desc = item.description.string
            self.raw_items[item_id] = {"name": item_name, "description": item_desc}

        puzzles = xml.data.puzzles.find_all("puzzle")
        for puzzle in puzzles:
            puzzle_id = puzzle["id"]
            puzzle_name = puzzle.find("name").string
            puzzle_desc = puzzle.description.string
            correct_answer = puzzle.correct_answer.string
            reward_item_id = puzzle.reward_item_id.string if puzzle.reward_item_id else None
            possible_answers_elements = puzzle.possible_answers.find_all("answer")
            possible_answers = []
            for answer_element in possible_answers_elements:
                possible_answers.append(answer_element.string)
            self.raw_puzzles[puzzle_id] = {"name": puzzle_name,
                                           "description": puzzle_desc,
                                           "possible_answers": possible_answers,
                                           "correct_answer": correct_answer,
                                           "reward_item_id": reward_item_id}

        rooms = xml.data.rooms.find_all("room")
        for room in rooms:
            room_id = room["id"]
            room_name = room.find("name").string
            room_desc = room.description.string

            room_items_elements = room.items.find_all('item')
            room_items = []
            for room_item_element in room_items_elements:
                room_items.append(room_item_element.string)

            room_puzzles_elements = room.puzzles.find_all('puzzle')
            room_puzzles = []
            for room_puzzle_element in room_puzzles_elements:
                room_puzzles.append(room_puzzle_element.string)

            room_exits_elements = room.exits.children
            room_exits = {}
            for room_exit in room_exits_elements:
                if not room_exit.name:
                    continue
                room_exits[room_exit.name] = room_exit.string

            self.raw_rooms[room_id] = {"name": room_name,
                                       "description": room_desc,
                                       "room_item_ids": room_items,
                                       "room_puzzles_ids": room_puzzles,
                                       "exits": room_exits}

        player = xml.data.find("player")
        player_name = player.find("name").string
        player_location_room_id = player.location.string
        player_inventory_raw = player.inventory.find_all("item")
        player_inventory_item_ids = []
        for player_inventory_item_id in player_inventory_raw:
            player_inventory_item_ids.append(player_inventory_item_id.string)

        self.raw_player = {"name": player_name,
                           "location": player_location_room_id,
                           "inventory": player_inventory_item_ids}