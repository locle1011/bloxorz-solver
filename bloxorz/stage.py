from state import Board, Box, State

C_ABYSS = ' '
C_GREYTILE = '█'
C_HOLE = '#'
C_ORANGETILE = '▒'
C_SOFTSWITCH = 'O'
C_HARDSWITCH = 'X'
C_TELEPORTSWITCH = 'C'


def get_stage(stage=0):
    return eval(f'get_stage_{stage}()')


def get_stage_0():
    box = Box(location=(0, 0))
    board = Board(strboard="#\n", switches={})
    return State(box=box, board=board)


def get_stage_1():
    """Passcode: 780464"""

    sboard = """
███       
██████    
█████████ 
 █████████
     ██#██
      ███ 
"""
    sboard = sboard[1:]
    box = Box(location=(1, 1))
    switches = {}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_2():
    """Passcode: 290299"""

    sboard = """
      ████  ███
████  ██X█  █#█
██O█  ████  ███
████  ████  ███
████  ████  ███
████  ████     
"""
    sboard = sboard[1:]

    box = Box(location=(4, 1))
    switches = {(2, 2): {'type': C_SOFTSWITCH,
                         'param': {'on_tiles': {(4, 4), (4, 5)},
                                   'off_tiles': set(),
                                   'toggle': True}},
                (1, 8): {'type': C_HARDSWITCH,
                         'param': {'on_tiles': {(4, 10), (4, 11)},
                                   'off_tiles': set(),
                                   'toggle': True}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_4():
    """Passcode: 520967"""

    sboard = """
   ▒▒▒▒▒▒▒    
   ▒▒▒▒▒▒▒    
████     ███  
███       ██  
███       ██  
███  ████▒▒▒▒▒
███  ████▒▒▒▒▒
     █#█  ▒▒█▒
     ███  ▒▒▒▒
"""
    sboard = sboard[1:]

    box = Box(location=(5, 1))
    switches = {(0, 3): {'type': C_ORANGETILE, 'param': {}},
                (0, 4): {'type': C_ORANGETILE, 'param': {}},
                (0, 5): {'type': C_ORANGETILE, 'param': {}},
                (0, 6): {'type': C_ORANGETILE, 'param': {}},
                (0, 7): {'type': C_ORANGETILE, 'param': {}},
                (0, 8): {'type': C_ORANGETILE, 'param': {}},
                (0, 9): {'type': C_ORANGETILE, 'param': {}},
                (1, 3): {'type': C_ORANGETILE, 'param': {}},
                (1, 4): {'type': C_ORANGETILE, 'param': {}},
                (1, 5): {'type': C_ORANGETILE, 'param': {}},
                (1, 6): {'type': C_ORANGETILE, 'param': {}},
                (1, 7): {'type': C_ORANGETILE, 'param': {}},
                (1, 8): {'type': C_ORANGETILE, 'param': {}},
                (1, 9): {'type': C_ORANGETILE, 'param': {}},
                (5, 9): {'type': C_ORANGETILE, 'param': {}},
                (5, 10): {'type': C_ORANGETILE, 'param': {}},
                (5, 11): {'type': C_ORANGETILE, 'param': {}},
                (5, 12): {'type': C_ORANGETILE, 'param': {}},
                (5, 13): {'type': C_ORANGETILE, 'param': {}},
                (6, 9): {'type': C_ORANGETILE, 'param': {}},
                (6, 10): {'type': C_ORANGETILE, 'param': {}},
                (6, 11): {'type': C_ORANGETILE, 'param': {}},
                (6, 12): {'type': C_ORANGETILE, 'param': {}},
                (6, 13): {'type': C_ORANGETILE, 'param': {}},
                (7, 10): {'type': C_ORANGETILE, 'param': {}},
                (7, 11): {'type': C_ORANGETILE, 'param': {}},
                (7, 13): {'type': C_ORANGETILE, 'param': {}},
                (8, 10): {'type': C_ORANGETILE, 'param': {}},
                (8, 11): {'type': C_ORANGETILE, 'param': {}},
                (8, 12): {'type': C_ORANGETILE, 'param': {}},
                (8, 13): {'type': C_ORANGETILE, 'param': {}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_8():
    """Passcode: 499707"""

    sboard = """
         ███   
         ███   
         ███   
██████   ██████
████C█   ████#█
██████   ██████
         ███   
         ███   
         ███   
"""
    sboard = sboard[1:]

    box = Box(location=(4, 1))
    switches = {(4, 4): {'type': C_TELEPORTSWITCH,
                         'param': {'first_half_coord': (1, 10),
                                   'second_half_coord': (7, 10)}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)
