import pygame
import numpy as np
from utils import *
from standard_search import DFGS, BestFS
import sys
import time



class Solution():
    def __init__(self, solver=None) -> None:
        self.time = 0
        self.pathcost = 0
        self.explore = 0
        self.res = []
        self.solver = solver

        self.__update()

    def __update(self):
        if self.solver:
            self.res, self.time, self.explore = make_profile(self.solver)
            self.pathcost = len(self.res) - 1

        
lvl_number = "1"
number = 1
s = get_stage(number=number)
# solver = BestFS(s, strategy='a-star')
# res = solver.solve()
dfs_solution = Solution(DFGS(s))
astar_solution = Solution(BestFS(s, strategy='a-star'))
monte_solution = Solution()

res = dfs_solution.res


# print(res[0].to_string())



pygame.init()
clock = pygame.time.Clock()


def getMaxRowCol(state):
    pass
    maxrow = 0
    maxcol = 0
    col = 0
    for i in range(0, len(state)):
        if (state[i] != '\n'):
            col += 1
        else:
            maxrow += 1
            if col > maxcol:
                maxcol = col
            col = 0

    return (maxrow, maxcol)

maxrow = getMaxRowCol(res[0].to_string())[0]
maxcol = getMaxRowCol(res[0].to_string())[1]

# print((maxrow, maxcol))

block_size_w = 500 // maxcol
block_size_h = 300 // maxrow

# Set up the display
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bloxorz")
screen.fill(color = (255, 255, 255))
pygame.display.update()

class objectIMG():
    def __init__(self, path):
        self.path = path
        self.img = pygame.image.load(path).convert_alpha()

    def scale(self, width, height):
        self.img = pygame.transform.scale(self.img, (width,height))

    def rescale(self, width, height):
        self.img = pygame.image.load(self.path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (width,height))
        
platform = objectIMG(r'asset\platform.bmp')
platform.scale(block_size_w, block_size_h)

platform_org = objectIMG(r'asset\org-plf.png')
platform_org.scale(block_size_w, block_size_h)

o_plf = objectIMG(r'asset\o-but.png')
o_plf.scale(block_size_w, block_size_h)

x_plf = objectIMG(r'asset\x-but.png')
x_plf.scale(block_size_w, block_size_h)

c_plf = objectIMG(r'asset\c-but.png')
c_plf.scale(block_size_w, block_size_h)

hole = objectIMG(r'asset\hole.png')
hole.scale(block_size_w, block_size_h)

block1 = objectIMG(r'asset\block.png')
pygame.display.set_icon(block1.img) #Set icon pygame window
block1.scale(block_size_w, block_size_h)

start_button = pygame.image.load(r'asset\start-button.png').convert_alpha()
start_button = pygame.transform.scale(start_button, (40 * 1.6375, 40))

start_button_rect = screen.blit(start_button, (15, 315))

next_button = pygame.image.load(r'asset\next-button.png').convert_alpha()
next_button = pygame.transform.scale(next_button, (40 * 1.6375, 40))

next_button_rect = screen.blit(next_button, (225, 315))

pause_button = pygame.image.load(r'asset\sm-pause-button.png').convert_alpha()
pause_button = pygame.transform.scale(pause_button, (40 * 1.6375, 40))

pause_button_rect = screen.blit(pause_button, (120, 315))

level = pygame.image.load(r'asset\lv-board.png').convert_alpha()
level = pygame.transform.scale(level, (50, 50 * 4.21))

screen.blit(level, (530, 50))

object = [platform, platform_org, hole, x_plf, o_plf, c_plf, block1]
def scaleObject(object, width, height):
    for obj in object:
        obj.rescale(width, height)

class Text():
    def __init__(self, font_name, size, outFont=False):
        self.font_name = font_name
        self.size = size
        self.font = None
        self.rect = None
        self.outFont = outFont

    def render(self, text, left=0, top=0, center=None):
        self.font = pygame.font.SysFont(self.font_name, self.size) if (self.outFont == False) else pygame.font.Font(self.font_name, self.size)
        display = self.font.render(text, True, 'black')
        self.rect = display.get_rect()
        self.rect.topleft = (left, top)
        if (center):
            self.rect.center = center
        screen.blit(display, self.rect)
        pygame.display.update()

class CheckBox():
    def __init__(self, surface, left, top, width, height):
        pass
        self.rect = pygame.Rect(left, top, width, height)
        self.checked = False
        self.surface = surface
    def draw(self, surface, color, border):
        pygame.draw.rect(surface, color, self.rect, border)
    
    def collipoint(self):
        if (self.checked == False):
            pygame.draw.rect(self.surface, 'black', (self.rect.x + 3, self.rect.y + 3,
                                                    14, 14))
            self.checked = True
        else:
            self.surface.fill('white', (self.rect.x + 3, self.rect.y + 3,
                                        14, 14))
            self.checked = False
    
    def deCheck(self):
        self.checked = True
        self.collipoint()
        
dfs_checkbox = CheckBox(screen, 600, 50 +50, 20, 20)
dfs_checkbox.draw(screen, 'black', 2)

astar_checkbox = CheckBox(screen, 600, 90 +50, 20, 20)
astar_checkbox.draw(screen, 'black', 2)

monte_checkbox = CheckBox(screen, 600, 130 +50, 20, 20)
monte_checkbox.draw(screen, 'black', 2)

#Add text to screen - BEGIN
""" Begin: Add Text to screen """
font = pygame.font.Font(r'asset\Bungee-Regular.ttf', 25)
text_2 = Text(r'asset\Bungee-Regular.ttf', 15, True)
text_2.render('Result', 15, 350 + 15)
text_2.render('Solution Path:', 120, 350 + 15)
text_2.render('Path Cost:', 350, 350 + 15)
text_2.render('Elapsed Time:', 480, 350 + 15)
text_2.render('Explore:', 630, 350 + 15)
text_2.render('DFS', 630, 102)
text_2.render('A-star (A*)', 630, 102 + 41)
text_2.render('Monte-Carlo', 630, 102 + 41*2)

text_3 = Text(r'asset\Rajdhani-Regular.ttf', 15, True)
text_3.render('DFS', 15, 390 + 15)
text_3.render('A-star (A*)', 15, 430 + 15)
text_3.render('Monte-Carlo', 15, 470 + 15)

#Solution Path box
box_solution_Dfs = pygame.Rect(120, 380 + 15, 210, 30)
box_solution_Astar = pygame.Rect(120, 420 + 15, 210, 30)
box_solution_Monte = pygame.Rect(120, 460 + 15, 210, 30)
pygame.draw.rect(screen, (42,42,42), box_solution_Dfs, 1)
pygame.draw.rect(screen, (42,42,42), box_solution_Astar, 1)
pygame.draw.rect(screen, (42,42,42), box_solution_Monte, 1)
pygame.display.update()
text_3.render('Placeholder DFS', 125, 385 + 15) #Solution DFS
text_3.render('Placeholder A-star', 125, 425 + 15) #Solution DFS
text_3.render('Placeholder Monte-Carlo', 125, 465 + 15) #Solution Monte-Carlo

def update_path_time_explore():
    #Path Cost
    screen.fill('white', (348, 391, 387, 120))
    text_3.render(str(dfs_solution.pathcost), center=(390, 410))
    text_3.render(str(astar_solution.pathcost), center=(390, 450))
    text_3.render(str(monte_solution.pathcost), center=(390, 490))

    #Elapsed time
    text_3.render(str(round(dfs_solution.time, 6)) + ' (s)', center=(390 + 150, 410))
    text_3.render(str(round(astar_solution.time, 6)) + ' (s)', center=(390 + 150, 450))
    text_3.render(str(round(monte_solution.time, 6)) + ' (s)', center=(390 + 150, 490))

    #Explore node
    text_3.render(str(dfs_solution.explore), center=(390 + 280, 410))
    text_3.render(str(astar_solution.explore), center=(390 + 280, 450))
    text_3.render(str(monte_solution.explore), center=(390 + 280, 490))

update_path_time_explore()

#

""" End: Add Text to screen """
#Add text to screen - END

pygame.draw.rect(screen, 'black', (0,0,510,310), 5, 5) #Draw BOX game

def drawBlock_Border(object, x, y, width, height, border_color=(42,42,42), border_size=2):
    screen.blit(object, (x, y))
    pygame.draw.rect(screen, border_color, [x,y,width,height], border_size)

def drawState(state=None, init=(0,0)):
    pass
    area_game = pygame.Rect(0, 0, 510, 310)
    screen.fill('white', area_game)
    pygame.draw.rect(screen, 'black', (0,0,510,310), 5, 5) #Draw BOX game

    init_x = init[0]
    init_y = init[1]
    for i in range(0, len(state)):
        if (state[i] == 'O'):
            drawBlock_Border(o_plf.img, init_x, init_y, block_size_w, block_size_h)
            init_x += block_size_w
        elif (state[i] == 'X'):
            drawBlock_Border(x_plf.img, init_x, init_y, block_size_w, block_size_h)
            init_x += block_size_w
        elif (state[i] == 'C'):
            drawBlock_Border(c_plf.img, init_x, init_y, block_size_w, block_size_h)
            init_x += block_size_w
        elif (state[i] == '█'):
            drawBlock_Border(platform.img, init_x, init_y, block_size_w, block_size_h,)
            init_x += block_size_w
        elif (state[i] == '▒'):
            drawBlock_Border(platform_org.img, init_x, init_y, block_size_w, block_size_h)
            init_x += block_size_w
        
        elif (state[i] == '1' or state[i] == '2'):
            screen.blit(block1.img, (init_x, init_y))
            init_x += block_size_w
        elif (state[i] == '#'):
            screen.blit(hole.img, (init_x, init_y))
            init_x += block_size_w
        elif (state[i] == '\n'):
            init_y += block_size_h
            init_x = init[0]
        elif (state[i] == ' '):
            init_x += block_size_w
  

state_index = [0]

def drawAllState(list_state):
    for state in list_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pause_button_rect.collidepoint(event.pos)):
                    return None
        
        area_game = pygame.Rect(0, 0, 510, 310)
        drawState(state.to_string(), init=(7,7))
        global state_index
        state_index[0] += 1

        pygame.display.update(area_game)
        clock.tick(5)

    state_index[0] = 0
    

drawState(res[0].to_string(), init=(7,7))

check_click = [False]
def checkClickEvent(object_rect, check_click):
    pass
    pos = pygame.mouse.get_pos()
    if (object_rect.collidepoint(pos)):
        if (pygame.mouse.get_pressed()[0] == 1 and check_click[0] == False):
            check_click[0] = True
            return True
        
        if (pygame.mouse.get_pressed()[0] == 0):
            check_click[0] = False

    return False

state_index = [0]
def checkEvent(object, event, state_index):
    if (checkClickEvent(object, check_click)):
        if (event == 'start'):
            state_index[0] = 0
            drawAllState(res)
            

        if (event == 'next'):
            # print('test')
            if (state_index[0] >= len(res)):
                state_index[0] = 0
            
            drawState(res[state_index[0]].to_string(), (7, 7))
            state_index[0] += 1
            


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            if (dfs_checkbox.rect.collidepoint(event.pos)):
                dfs_checkbox.collipoint()
                astar_checkbox.deCheck()
                monte_checkbox.deCheck()

                # solver = DFGS(s)
                # res = solver.solve()
                res = dfs_solution.res

            elif (astar_checkbox.rect.collidepoint(event.pos)):
                astar_checkbox.collipoint()
                dfs_checkbox.deCheck()
                monte_checkbox.deCheck()

                # solver = BestFS(s, strategy='a-star')
                # res = solver.solve()
                res = astar_solution.res

            elif (monte_checkbox.rect.collidepoint(event.pos)):
                monte_checkbox.collipoint()
                astar_checkbox.deCheck()
                dfs_checkbox.deCheck()

                # solver = BestFS(s, strategy='a-star')
                # res = solver.solve()
                res = monte_solution.res

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                lvl_number = lvl_number[:-1]
                screen.blit(level, (530, 50))

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Handle Enter key
                number = int(lvl_number)
                s = get_stage(number=number)
                # solver = BestFS(s, strategy='a-star')
                # res = solver.solve()
                dfs_solution = Solution(DFGS(s))
                astar_solution = Solution(BestFS(s, strategy='a-star'))
                monte_solution = Solution()

                res = dfs_solution.res
                if (dfs_checkbox.checked):
                    res = dfs_solution.res
                elif (astar_checkbox.checked):
                    res = astar_solution.res
                elif (monte_checkbox.checked):
                    res = monte_solution.res

                update_path_time_explore()

                # print(res[0].to_string())
                maxrow = getMaxRowCol(res[0].to_string())[0]
                maxcol = getMaxRowCol(res[0].to_string())[1]

                # print((maxrow, maxcol))

                block_size_w = 500 // maxcol
                block_size_h = 300 // maxrow

                scaleObject(object, block_size_w, block_size_h)
                # platform.scale(block_size_w, block_size_h)

                screen.fill('white', pygame.Rect(0, 0, 515, 315))
                pygame.draw.rect(screen, 'black', (0,0,510,310), 5, 5) #Draw BOX game
                
                drawState(res[0].to_string(), init=(7,7))

            temp = event.unicode
            if (temp in [str(i) for i in range(0, 10)]):
                if (int(lvl_number + temp) > 0 and int(lvl_number + temp) < 34):
                    lvl_number += event.unicode
                    
                else:
                    lvl_number = '33'
                
                screen.blit(level, (530, 50))
                
    checkEvent(start_button_rect, 'start', state_index)
    checkEvent(next_button_rect, 'next', state_index)

    level_number = font.render(lvl_number, True, (135, 29, 32))
    level_number_rect = level_number.get_rect(center=(555, (50 * 4.21 + 25)))
    screen.blit(level_number, level_number_rect)

    pygame.display.update()
