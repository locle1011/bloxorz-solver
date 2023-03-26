from abc import ABC, abstractmethod
from enum import Enum

ROW = 0
COL = 1
NEIGHBOR_TILE = [(-1, 0, 'V'), (1, 0, 'V'), (0, -1, 'H'), (0, 1, 'H')]

C_ABYSS = ' '
C_GREYTILE = '█'
C_HOLE = '#'
C_ORANGETILE = '▒'
C_SOFTSWITCH = 'O'
C_HARDSWITCH = 'X'
C_TELEPORTSWITCH = 'C'


class Action(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    SWITCH = 5


class Box:
    def __init__(self, location: tuple):
        if len(location) != 2:
            raise ValueError("location must be in length of two!")
        elif type(location[ROW]) is type(location[COL]) is int:
            first_location = second_location = location
        elif type(location[ROW]) is type(location[COL]) is tuple:
            first_location, second_location = location
        else:
            raise TypeError(location)

        self.first_half = list(first_location)
        self.second_half = list(second_location)
        self.splitted = False

        if first_location == second_location:
            self.stand_up()
        elif first_location[ROW] == second_location[ROW] and abs(first_location[COL]-second_location[COL]) == 1:
            self.lie_horizontal()
        elif first_location[COL] == second_location[COL] and abs(first_location[ROW]-second_location[ROW]) == 1:
            self.lie_vertical()
        else:
            self.split(first_location, second_location)

    def copy(self):
        return Box((tuple(self.first_half), tuple(self.second_half)))

    def get_location(self):
        return tuple(self.first_half), tuple(self.second_half)

    def get_first_half(self):
        return tuple(self.first_half)

    def get_second_half(self):
        return tuple(self.second_half)

    def is_splitted(self):
        return self.splitted

    def is_standing(self):
        return self.first_half == self.second_half

    def split(self, first_half_coord, second_half_coord):
        self.first_half = list(first_half_coord)
        self.second_half = list(second_half_coord)
        self.splitted = True

        self.moveLeft = self.moveLeftSingle
        self.moveRight = self.moveRightSingle
        self.moveUp = self.moveUpSingle
        self.moveDown = self.moveDownSingle

    def merge_horizontal(self):
        if self.first_half[COL] > self.second_half[COL]:
            self.first_half, self.second_half = self.second_half, self.first_half
        self.lie_horizontal()
        self.splitted = False

    def merge_vertical(self):
        if self.first_half[ROW] > self.second_half[ROW]:
            self.first_half, self.second_half = self.second_half, self.first_half
        self.lie_vertical()
        self.splitted = False

    def switch(self):
        if self.is_splitted():
            self.first_half, self.second_half = self.second_half, self.first_half

    def moveLeftSingle(self):
        self.first_half[COL] -= 1

    def moveRightSingle(self):
        self.first_half[COL] += 1

    def moveUpSingle(self):
        self.first_half[ROW] -= 1

    def moveDownSingle(self):
        self.first_half[ROW] += 1

    def stand_up(self):
        self.moveLeft = self.moveLeftStand
        self.moveRight = self.moveRightStand
        self.moveUp = self.moveUpStand
        self.moveDown = self.moveDownStand

    def lie_vertical(self):
        self.moveLeft = self.moveLeftVertical
        self.moveRight = self.moveRightVertical
        self.moveUp = self.moveUpVertical
        self.moveDown = self.moveDownVertical

    def lie_horizontal(self):
        self.moveLeft = self.moveLeftHorizontal
        self.moveRight = self.moveRightHorizontal
        self.moveUp = self.moveUpHorizontal
        self.moveDown = self.moveDownHorizontal

    def moveLeftStand(self):
        self.first_half[COL] -= 2
        self.second_half[COL] -= 1
        self.lie_horizontal()

    def moveLeftVertical(self):
        self.first_half[COL] -= 1
        self.second_half[COL] -= 1

    def moveLeftHorizontal(self):
        self.first_half[COL] -= 1
        self.second_half[COL] -= 2
        self.stand_up()

    def moveRightStand(self):
        self.first_half[COL] += 1
        self.second_half[COL] += 2
        self.lie_horizontal()

    def moveRightVertical(self):
        self.first_half[COL] += 1
        self.second_half[COL] += 1

    def moveRightHorizontal(self):
        self.first_half[COL] += 2
        self.second_half[COL] += 1
        self.stand_up()

    def moveUpStand(self):
        self.first_half[ROW] -= 2
        self.second_half[ROW] -= 1
        self.lie_vertical()

    def moveUpVertical(self):
        self.first_half[ROW] -= 1
        self.second_half[ROW] -= 2
        self.stand_up()

    def moveUpHorizontal(self):
        self.first_half[ROW] -= 1
        self.second_half[ROW] -= 1

    def moveDownStand(self):
        self.first_half[ROW] += 1
        self.second_half[ROW] += 2
        self.lie_vertical()

    def moveDownVertical(self):
        self.first_half[ROW] += 2
        self.second_half[ROW] += 1
        self.stand_up()

    def moveDownHorizontal(self):
        self.first_half[ROW] += 1
        self.second_half[ROW] += 1


class Board:
    pass


class ActiveTile(ABC):
    @abstractmethod
    def activate(self, box: Box, board: Board) -> bool:
        pass


class OrangeTile(ActiveTile):
    symbol = C_ORANGETILE

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            board[box.get_first_half()] = C_ABYSS
            return False
        return True


class SoftSwitch(ActiveTile):
    symbol = C_SOFTSWITCH

    def __init__(self, radio_on=[], radio_off=[], toggle=[]):
        self.radio_on = radio_on.copy()
        self.radio_off = radio_off.copy()
        self.toggle = toggle.copy()

    def activate(self, box: Box, board: Board):
        board.turn_on_bridges(self.radio_on)
        board.turn_off_bridges(self.radio_off)
        board.toggle_bridges(self.toggle)
        return True


class HardSwitch(SoftSwitch):
    symbol = C_HARDSWITCH

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            super().activate(box, board)
            return False
        return True


class MergeTile(ActiveTile):
    symbol = 'M'

    def __init__(self, tile: ActiveTile, merge_type: str):
        self.tile = tile
        if merge_type == 'H':
            self.merge = lambda box: box.merge_horizontal()
        elif merge_type == 'V':
            self.merge = lambda box: box.merge_vertical()
        else:
            raise ValueError('merge_type not found!')

    def activate(self, box: Box, board: Board):
        if isinstance(self.tile, ActiveTile):
            self.tile.activate(box, board)

        other_id = box.get_second_half()
        for diff in NEIGHBOR_TILE:
            index = (other_id[ROW] + diff[ROW], other_id[COL] + diff[COL])
            if board.is_valid_index(index):
                tile = board[index].tile
                if isinstance(tile, ActiveTile):
                    board[index] = tile
                else:
                    board.active_tiles.pop(index)

        other_tile = board[other_id]
        if isinstance(other_tile, ActiveTile):
            other_tile.activate(box, board)

        self.merge(box)
        return False


class TeleportSwitch(ActiveTile):
    symbol = C_TELEPORTSWITCH

    def __init__(self, first_half_coord: tuple[int, int], second_half_coord: tuple[int, int]):
        self.first_half_coord = first_half_coord
        self.second_half_coord = second_half_coord

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            box.split(self.first_half_coord, self.second_half_coord)
            other_id = box.get_second_half()
            for diff in NEIGHBOR_TILE:
                index = (other_id[ROW] + diff[ROW], other_id[COL] + diff[COL])
                if board.is_valid_index(index):
                    tile = board[index]
                    board[index] = MergeTile(tile, merge_type=diff[2])
            return False
        return True


class Board:
    active_cls = {C_ORANGETILE: OrangeTile,
                  C_TELEPORTSWITCH: TeleportSwitch,
                  C_SOFTSWITCH: SoftSwitch,
                  C_HARDSWITCH: HardSwitch}

    def __init__(self, strboard: str, switches: dict):
        self.active_tiles = dict()
        self.strboard = list(strboard)
        self.row_length = len(strboard[:strboard.index('\n')])+1
        self.hole = strboard.index(C_HOLE)
        self.hole = (self.hole//self.row_length, self.hole % self.row_length)

        for idx, obj in switches.items():
            self.active_tiles[idx] = self.active_cls[obj['type']](
                **obj['param'])

    def copy(self):
        other = Board('\n#', {})
        other.hole = self.hole
        other.row_length = self.row_length
        other.strboard = self.strboard.copy()
        other.active_tiles = self.active_tiles.copy()
        return other

    def ravel(self, index):
        return index[ROW]*self.row_length + index[COL]

    def to_string(self):
        return ''.join(self.strboard)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.to_string())

    def is_valid_index(self, index: tuple[int, int]):
        return index[COL]+1 < self.row_length and all(x >= 0 for x in index) and self.ravel(index) < len(self.strboard)

    def __getitem__(self, index: tuple[int, int]):
        if not self.is_valid_index(index):
            return C_ABYSS
        elif index in self.active_tiles.keys():
            return self.active_tiles[index]
        else:
            return self.strboard[self.ravel(index)]

    def __setitem__(self, index: tuple[int, int], value):
        if not self.is_valid_index(index):
            raise IndexError(index)

        i = self.ravel(index)
        if isinstance(value, ActiveTile):
            self.active_tiles[index] = value
            if type(value) is not MergeTile:
                self.strboard[i] = type(value).symbol
        elif value in [C_GREYTILE, C_ABYSS, C_HOLE]:
            self.active_tiles.pop(index, None)
            self.strboard[i] = value
        else:
            raise ValueError(value)

    def turn_on_bridges(self, on_tiles: list):
        for tile in on_tiles:
            self.strboard[self.ravel(tile)] = C_GREYTILE

    def turn_off_bridges(self, off_tiles: list):
        for tile in off_tiles:
            self.strboard[self.ravel(tile)] = C_ABYSS

    def toggle_bridges(self, tiles: list):
        for tile in tiles:
            i = self.ravel(tile)
            v = self.strboard[i]
            self.strboard[i] = C_GREYTILE if v == C_ABYSS else C_ABYSS


class State:
    def __init__(self, box: Box, board: Board):
        self.box = box
        self.board = board

    def to_string(self):
        bboard = list(self.board.to_string())
        first_id, second_id = self.box.get_location()

        if self.board.is_valid_index(first_id):
            first_id = self.board.ravel(first_id)
            bboard[first_id] = '1'

        if self.board.is_valid_index(second_id):
            second_id = self.board.ravel(second_id)
            bboard[second_id] = '2'

        return ''.join(bboard)

    def encode(self):
        return self.board.to_string() + str(self.box.get_location())

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.encode())

    def __eq__(self, other):
        return self.encode() == other.encode()

    def copy(self):
        return State(self.box.copy(), self.board.copy())

    def is_end(self):
        first_id, second_id = self.box.get_location()
        return self.board[first_id] is C_ABYSS or self.board[second_id] is C_ABYSS

    def is_goal(self):
        first_id, second_id = self.box.get_location()
        return first_id == second_id == self.board.hole

    def perform(self, action: Action):
        if self.is_end() or self.is_goal():
            return False

        if action is Action.LEFT:
            self.box.moveLeft()
        elif action is Action.RIGHT:
            self.box.moveRight()
        elif action is Action.UP:
            self.box.moveUp()
        elif action is Action.DOWN:
            self.box.moveDown()
        elif action is Action.SWITCH:
            if self.box.is_splitted():
                self.handle_switch()
                return True
            else:
                return False

        first_tile = self.board[self.box.get_first_half()]
        active_second_tile = True
        if isinstance(first_tile, ActiveTile):
            active_second_tile = first_tile.activate(self.box, self.board)

        second_tile = self.board[self.box.get_second_half()]
        if isinstance(second_tile, ActiveTile):
            if active_second_tile and not self.box.is_standing() and not self.box.is_splitted():
                second_tile.activate(self.box, self.board)

        return True

    def handle_switch(self):
        self.box.switch()
        current_id = self.box.get_first_half()

        for diff in NEIGHBOR_TILE:
            index = (current_id[ROW] + diff[ROW], current_id[COL] + diff[COL])
            if self.board.is_valid_index(index):
                tile = self.board[index].tile
                if isinstance(tile, ActiveTile):
                    self.board[index] = tile
                else:
                    self.board.active_tiles.pop(index)

        other_id = self.box.get_second_half()

        for diff in NEIGHBOR_TILE:
            index = (other_id[ROW] + diff[ROW], other_id[COL] + diff[COL])
            if self.board.is_valid_index(index):
                tile = self.board[index]
                self.board[index] = MergeTile(tile, merge_type=diff[2])
