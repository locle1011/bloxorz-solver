from state import Board, Box, State

C_ABYSS = ' '
C_GREYTILE = '█'
C_HOLE = '#'
C_ORANGETILE = '▒'
C_SOFTSWITCH = 'O'
C_HARDSWITCH = 'X'
C_TELEPORTSWITCH = 'C'


def get_stage(number=0) -> State:
    return eval(f'get_stage_{number}()')


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
                         'param': {'radio_on': [(4, 4), (4, 5)]}},
                (1, 8): {'type': C_HARDSWITCH,
                         'param': {'radio_on': [(4, 10), (4, 11)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_3():
    """Passcode: 918660"""

    sboard = """
      ███████  
████  ███  ██  
█████████  ████
████       ██#█
████       ████
            ███
"""
    sboard = sboard[1:]

    box = Box(location=(3, 1))
    switches = {}
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


def get_stage_5():
    """Passcode: 028431"""

    sboard = """
           ████
 ███████O██████
 ████       ███
 ██O█          
 ████          
   ███O██████  
          ████O
███       █████
█#███████████  
████           
"""
    sboard = sboard[1:]

    box = Box(location=(1, 13))
    switches = {(1, 8): {'type': C_SOFTSWITCH,
                         'param': {'toggle': [(1, 5), (1, 6)]}},
                (3, 3): {'type': C_SOFTSWITCH,
                         'param': {'radio_on': [(8, 5), (8, 6)]}},
                (5, 6): {'type': C_SOFTSWITCH,
                         'param': {'radio_off': [(8, 5), (8, 6)]}},
                (6, 14): {'type': C_SOFTSWITCH,
                          'param': {'toggle': [(8, 5), (8, 6)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_6():
    """Passcode: 524383"""

    sboard = """
     ██████    
     █  ███    
     █  █████  
██████     ████
    ███    ██#█
    ███     ███
      █  ██    
      █████    
      █████    
       ███     
"""
    sboard = sboard[1:]

    box = Box(location=(3, 0))
    switches = {}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_7():
    """Passcode: 189493"""

    sboard = """
        ████   
        ████   
███     █  ████
█████████   █#█
███    ██X  ███
███    ███  ███
 ██    █       
  ██████       
"""
    sboard = sboard[1:]

    box = Box(location=(3, 1))
    switches = {(4, 9): {'type': C_HARDSWITCH,
                         'param': {'toggle': [(6, 3)]}}}
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


def get_stage_9():
    """Passcode: 074355"""

    sboard = """
████   █   ████
████   █   ██C█
███████████████
      █#█      
      ███      
"""
    sboard = sboard[1:]

    box = Box(location=(1, 1))
    switches = {(1, 13): {'type': C_TELEPORTSWITCH,
                          'param': {'first_half_coord': (1, 12),
                                    'second_half_coord': (1, 2)}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_10():
    """Passcode: 300590"""

    sboard = """
███     ██████
█#█  █  ████C█
███     ████  
         ███  
           ██ 
            █ 
            █ 
           ██ 
    █████  ██ 
    █O  ███X█ 
"""
    sboard = sboard[1:]

    box = Box(location=(1, 9))
    switches = {(1, 12): {'type': C_TELEPORTSWITCH,
                          'param': {'first_half_coord': (1, 12),
                                    'second_half_coord': (1, 9)}},
                (9, 5): {'type': C_SOFTSWITCH,
                         'param': {'toggle': [(1, 3), (1, 4)]}},
                (9, 11): {'type': C_HARDSWITCH,
                          'param': {'toggle': [(1, 6), (1, 7), (2, 12), (3, 12)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_11():
    """Passcode: 291709"""

    sboard = """
 ████       
 █#██       
 ███        
 █   ██████ 
 █   ██  ██ 
███████  ███
     █O    █
     ████  █
     ███████
        ███ 
"""
    sboard = sboard[1:]

    box = Box(location=(5, 0))
    switches = {(6, 6): {'type': C_SOFTSWITCH,
                         'param': {'radio_off': [(0, 4), (1, 4)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_12():
    """Passcode: 958640"""

    sboard = """
            X
     ███  ███
     █X█████ 
   █████  ██ 
   █#█    ██ 
 █████   ████
████     ████
████  █████  
     ███     
     ███     
"""
    sboard = sboard[1:]

    box = Box(location=(6, 2))
    switches = {(0, 12): {'type': C_HARDSWITCH,
                          'param': {'toggle': [(4, 6)]}},
                (2, 6): {'type': C_HARDSWITCH,
                         'param': {'toggle': [(2, 12)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_13():
    """Passcode: 448106"""

    sboard = """
███▒████▒████ 
██        ███ 
██         ███
███   ███  ███
███▒▒▒█#█  ███
███  ▒███  █  
  █  ▒▒▒▒▒██  
  ███▒▒█▒▒▒   
   ██▒▒▒▒▒▒   
   ███  ██    
"""
    sboard = sboard[1:]

    box = Box(location=(3, 12))
    switches = {(0, 3): {'type': C_ORANGETILE, 'param': {}},
                (0, 8): {'type': C_ORANGETILE, 'param': {}},
                (4, 3): {'type': C_ORANGETILE, 'param': {}},
                (4, 4): {'type': C_ORANGETILE, 'param': {}},
                (4, 5): {'type': C_ORANGETILE, 'param': {}},
                (5, 5): {'type': C_ORANGETILE, 'param': {}},
                (6, 5): {'type': C_ORANGETILE, 'param': {}},
                (6, 6): {'type': C_ORANGETILE, 'param': {}},
                (6, 7): {'type': C_ORANGETILE, 'param': {}},
                (6, 8): {'type': C_ORANGETILE, 'param': {}},
                (6, 9): {'type': C_ORANGETILE, 'param': {}},
                (7, 5): {'type': C_ORANGETILE, 'param': {}},
                (7, 6): {'type': C_ORANGETILE, 'param': {}},
                (7, 8): {'type': C_ORANGETILE, 'param': {}},
                (7, 9): {'type': C_ORANGETILE, 'param': {}},
                (7, 10): {'type': C_ORANGETILE, 'param': {}},
                (8, 5): {'type': C_ORANGETILE, 'param': {}},
                (8, 6): {'type': C_ORANGETILE, 'param': {}},
                (8, 7): {'type': C_ORANGETILE, 'param': {}},
                (8, 8): {'type': C_ORANGETILE, 'param': {}},
                (8, 9): {'type': C_ORANGETILE, 'param': {}},
                (8, 10): {'type': C_ORANGETILE, 'param': {}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_14():
    """Passcode: 210362"""

    sboard = """
        ███   
   ███  ███   
█  ███████████
█  ███      X█
█           ██
█           ██
█       ██████
█████   ███   
 ██#█   ███   
  ███   █████X
"""
    sboard = sboard[1:]

    box = Box(location=(2, 4))
    switches = {(3, 12): {'type': C_HARDSWITCH,
                          'param': {'toggle': [(2, 1), (2, 2)]}},
                (9, 13): {'type': C_HARDSWITCH,
                          'param': {'toggle': [(3, 1), (3, 2)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_15():
    """Passcode: 098598"""

    sboard = """
       ███  ███
    ██████  X██
██  █  ███  ███
█████   O      
██             
 █     C       
 █     █       
███   ███  O██ 
████████████#█ 
███   ███  O██ 
"""
    sboard = sboard[1:]

    box = Box(location=(8, 1))
    switches = {(5, 7): {'type': C_TELEPORTSWITCH,
                         'param': {'first_half_coord': (1, 13),
                                   'second_half_coord': (8, 1)}},
                (7, 11): {'type': C_SOFTSWITCH,
                          'param': {'radio_off': [(8, 9), (8, 10)]}},
                (9, 11): {'type': C_SOFTSWITCH,
                          'param': {'radio_off': [(8, 9), (8, 10)]}},
                (3, 8): {'type': C_SOFTSWITCH,
                         'param': {'toggle': [(1, 5), (1, 6), (1, 10), (1, 11)]}},
                (1, 12): {'type': C_HARDSWITCH,
                          'param': {'toggle': [(1, 5), (1, 6), (2, 2), (2, 3)]}}}
    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)


def get_stage_23():
    """Passcode: 293486"""

    sboard = """
 ███        ███
 █X█        █O█
 ███   ████████
 ███   █#█  ██O
█   █  ███    █
O   █  ▒▒▒    █
█  ███▒▒▒▒▒████
   ███▒▒▒▒▒█C█ 
   ███▒▒▒▒▒███ 
   █████       
"""
    sboard = sboard[1:]
    box = Box(location=(7, 4))

    switches = {(5, 7): {'type': C_ORANGETILE, 'param': {}},
                (5, 8): {'type': C_ORANGETILE, 'param': {}},
                (5, 9): {'type': C_ORANGETILE, 'param': {}},
                (6, 6): {'type': C_ORANGETILE, 'param': {}},
                (6, 7): {'type': C_ORANGETILE, 'param': {}},
                (6, 8): {'type': C_ORANGETILE, 'param': {}},
                (6, 9): {'type': C_ORANGETILE, 'param': {}},
                (6, 10): {'type': C_ORANGETILE, 'param': {}},
                (7, 6): {'type': C_ORANGETILE, 'param': {}},
                (7, 7): {'type': C_ORANGETILE, 'param': {}},
                (7, 8): {'type': C_ORANGETILE, 'param': {}},
                (7, 9): {'type': C_ORANGETILE, 'param': {}},
                (7, 10): {'type': C_ORANGETILE, 'param': {}},
                (8, 6): {'type': C_ORANGETILE, 'param': {}},
                (8, 7): {'type': C_ORANGETILE, 'param': {}},
                (8, 8): {'type': C_ORANGETILE, 'param': {}},
                (8, 9): {'type': C_ORANGETILE, 'param': {}},
                (8, 10): {'type': C_ORANGETILE, 'param': {}},
                (1, 13): {'type': C_SOFTSWITCH,
                          'param': {'radio_on': [(6, 1), (6, 2)],
                                    'toggle': [(9, 8)]}},
                (3, 14): {'type': C_SOFTSWITCH,
                          'param': {'radio_off': [(2, 10), (2, 11), (6, 14)]}},
                (5, 0): {'type': C_SOFTSWITCH,
                         'param': {'radio_on': [(3, 0)],
                                   'radio_off': [(6, 1), (6, 2)]}},
                (1, 2): {'type': C_HARDSWITCH,
                         'param': {'radio_on': [(3, 4)]}},
                (7, 12): {'type': C_TELEPORTSWITCH,
                          'param': {'first_half_coord': (7, 12),
                                    'second_half_coord': (2, 2)}}
                }

    board = Board(strboard=sboard, switches=switches)
    return State(box=box, board=board)
