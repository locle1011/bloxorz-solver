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
        self.current_half = None
        self.other_half = None

        if first_location == second_location:
            self.stand_up()
        elif first_location[ROW] == second_location[ROW] and abs(first_location[COL]-second_location[COL]) == 1:
            self.lie_vertical()
        elif first_location[COL] == second_location[COL] and abs(first_location[ROW]-second_location[ROW]) == 1:
            self.lie_horizontal()
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

    def get_current_half(self):
        if self.current_half is None:
            return None
        return tuple(self.current_half)

    def get_other_half(self):
        if self.other_half is None:
            return None
        return tuple(self.other_half)

    def is_splitting(self):
        return self.current_half is not None and self.other_half is not None

    def is_standing(self):
        return self.first_half == self.second_half

    def split(self, first_half_coord, second_half_coord):
        self.first_half[:] = first_half_coord
        self.second_half[:] = second_half_coord
        self.current_half = self.first_half
        self.other_half = self.second_half

        self.moveLeft = self.moveLeftSingle
        self.moveRight = self.moveRightSingle
        self.moveUp = self.moveUpSingle
        self.moveDown = self.moveDownSingle

    def merge_horizontal(self):
        if self.first_half[COL] > self.second_half[COL]:
            self.first_half, self.second_half = self.second_half, self.first_half
        self.lie_horizontal()
        self.current_half = self.other_half = None

    def merge_vertical(self):
        if self.first_half[ROW] > self.second_half[ROW]:
            self.first_half, self.second_half = self.second_half, self.first_half
        self.lie_vertical()
        self.current_half = self.other_half = None

    def switch(self):
        self.current_half, self.other_half = self.other_half, self.current_half

    def moveLeftSingle(self):
        self.current_half[COL] -= 1

    def moveRightSingle(self):
        self.current_half[COL] += 1

    def moveUpSingle(self):
        self.current_half[ROW] -= 1

    def moveDownSingle(self):
        self.current_half[ROW] += 1

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
    def activate(self, box: Box, board: Board):
        pass


class OrangeTile(ActiveTile):
    symbol = C_ORANGETILE

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            board[box.get_first_half()] = C_ABYSS


class SoftSwitch(ActiveTile):
    symbol = C_SOFTSWITCH

    def __init__(self, on_tiles: set, off_tiles: set, toggle=False):
        self.on_tiles = set(on_tiles)
        self.off_tiles = set(off_tiles)

        def trigger(box: Box, board: Board):
            board.turn_on_bridges(self.on_tiles)
            board.turn_off_bridges(self.off_tiles)

        if toggle:
            def toggle_trigger(box: Box, board: Board):
                trigger(box, board)
                self.on_tiles, self.off_tiles = self.off_tiles, self.on_tiles
            self._activate = toggle_trigger
        else:
            self._activate = trigger

    def activate(self, box: Box, board: Board):
        self._activate(box, board)


class HardSwitch(SoftSwitch):
    symbol = C_HARDSWITCH

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            super(HardSwitch, self)._activate(box, board)


class MergeTile(ActiveTile):
    symbol = 'M'

    def __init__(self, tile: ActiveTile, merge_type: str):
        self.tile = tile
        if merge_type == 'H':
            def wrapper(box: Box, board: Board):
                if self.tile is not C_GREYTILE and self.tile is not C_HOLE:
                    self.tile.activate(box, board)
                box.merge_horizontal()

        elif merge_type == 'V':
            def wrapper(box: Box, board: Board):
                if self.tile is not C_GREYTILE and self.tile is not C_HOLE:
                    self.tile.activate(box, board)
                box.merge_vertical()

        else:
            raise ValueError('merge_type not found!')

        self._activate = wrapper

    def activate(self, box: Box, board: Board):
        self._activate(box, board)


class TeleportSwitch(ActiveTile):
    symbol = C_TELEPORTSWITCH

    def __init__(self, first_half_coord: tuple[int, int], second_half_coord: tuple[int, int]):
        self.first_half_coord = first_half_coord
        self.second_half_coord = second_half_coord

    def activate(self, box: Box, board: Board):
        if box.is_standing():
            box.split(self.first_half_coord, self.second_half_coord)
            other_id = box.get_other_half()
            for diff in NEIGHBOR_TILE:
                index = (other_id + diff[ROW], other_id + diff[COL])
                tile = board[index]
                if tile is not C_ABYSS:
                    board[index] = MergeTile(tile, merge_type=diff[2])


class Board:
    active_cls = {C_ORANGETILE: OrangeTile,
                  C_TELEPORTSWITCH: TeleportSwitch,
                  C_SOFTSWITCH: SoftSwitch,
                  C_HARDSWITCH: HardSwitch}

    def __init__(self, strboard: str, switches: dict):
        self.active_tiles = dict()
        self.strboard = list(strboard.strip())
        self.row_length = len(strboard[:strboard.index('\n')])
        self.hole = self.strboard.index(C_HOLE)
        self.hole = (self.hole//self.row_length, self.hole % self.row_length)

        for idx, obj in switches.items():
            self.active_tiles[idx] = self.active_cls[obj['type']](
                **obj['param'])

    def copy(self):
        other = Board('', {})
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

    def __getitem__(self, index: tuple[int, int]):
        if index in self.active_tiles.keys():
            return self.active_tiles[index]

        if all(x >= 0 for x in index):
            i = self.ravel(index)
            if self.strboard[i] == C_GREYTILE:
                return C_GREYTILE
            elif self.strboard[i] == C_HOLE:
                return C_HOLE
            else:
                return C_ABYSS
        else:
            return C_ABYSS

    def __setitem__(self, index: tuple[int, int], value):
        if any(x < 0 for x in index) or self.ravel(index) >= len(self.strboard):
            raise IndexError(index)

        i = self.ravel(index)
        if value in {C_GREYTILE, C_ABYSS, C_HOLE}:
            if index in self.active_tiles.keys():
                self.active_tiles.pop(index)
            self.strboard[i] = value
        elif isinstance(value, ActiveTile):
            self.active_tiles[index] = value
            if type(value) is MergeTile:
                pass
            else:
                self.strboard[i] = type(value).symbol
        else:
            raise TypeError(type(value))

    def turn_on_bridges(self, on_tiles: set):
        self.tiles |= on_tiles
        for tile in on_tiles:
            self.strboard[self.ravel(tile)] = C_GREYTILE

    def turn_off_bridges(self, off_tiles: set):
        self.tiles -= off_tiles
        for tile in off_tiles:
            self.strboard[self.ravel(tile)] = C_ABYSS


class State:
    def __init__(self, box: Box, board: Board):
        self.box = box
        self.board = board

    def to_string(self):
        bboard = list(self.board.to_string())
        first_id, second_id = self.box.get_location()
        first_id = self.board.ravel(first_id)
        second_id = self.board.ravel(second_id)
        bboard[first_id] = '1'
        bboard[second_id] = '2'
        return ''.join(bboard)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.to_string())

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
            if self.box.is_splitting():
                self.handle_switch()
            else:
                return False

        first_tile = self.board[self.box.get_first_half()]
        if first_tile is not C_GREYTILE and first_tile is not C_ABYSS:
            first_tile.activate()
        if not self.box.is_standing():
            second_tile = self.board[self.box.get_second_half()]
            if second_tile is not C_GREYTILE and second_tile is not C_ABYSS:
                second_tile.activate()

        return True

    def handle_switch(self):
        self.box.switch()
        other_id = self.box.get_other_half()

        for diff in NEIGHBOR_TILE:
            index = (other_id + diff[ROW], other_id + diff[COL])
            tile = self.board[index]
            if tile is not C_ABYSS:
                self.board[index] = MergeTile(tile, merge_type=diff[2])

        # Current half
        current_id = self.box.get_current_half()

        for diff in NEIGHBOR_TILE:
            index = (current_id + diff[ROW], current_id + diff[COL])
            mtile = self.board[index]
            if tile is not C_ABYSS:
                self.board[index] = mtile.tile
