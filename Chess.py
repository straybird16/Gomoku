import math
import time
import pygame as pg, sys
import pygame.freetype
from pygame.locals import *


class Chess:
    # basic chess configs
    BOARD_SIZE: int
    DIVIDE_NUM: int
    board_color: (0, 0, 0)
    line_color = (0, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    font_size = 20
    Gomoku: list

    isDraw: bool = False
    XO: str
    winner = None

    # window size
    width: int
    height: int
    # other parameters
    fps = 30
    CLOCK = None
    screen = None
    cover = None
    text_surfaceX, rect = (None, None)
    text_surfaceO, rect = (None, None)

    def __init__(self, board_size: int, color: tuple):
        self.BOARD_SIZE = board_size
        self.DIVIDE_NUM = self.BOARD_SIZE + 1
        self.board_color = color
        self.width = 700
        self.height = 700
        self.XO = 'x'
        pg.init()
        self.CLOCK = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32)
        self.Gomoku = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        pg.display.set_caption("GomoKu")

        # initializing pygame window
        pg.init()
        self.CLOCK = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32)
        pg.display.set_caption("GomoKu")

        # loading the images
        self.cover = pg.image.load('gomoku.png')
        self.cover = pg.transform.scale(self.cover, (self.width, self.height + 100))
        game_font = pygame.freetype.SysFont('Comic Sans', self.font_size)
        self.text_surfaceX, rect = game_font.render("X", (0, 0, 0))
        self.text_surfaceO, rect = game_font.render("O", (0, 0, 0))

    def exit(self):
        pg.quit()
        sys.exit()

    def getEvent(self):
        return pg.event.get()

    def updateDisplay(self):
        pg.display.update()

    def draw_status(self):
        if self.XO == 'x':
            player = "Black"
        else:
            player = "White"
        if self.winner is None:
            message = player + "'s Turn"
        elif self.winner == 'x':
            message = "Black won!"
        else:
            message = "White won!"
        if self.isDraw:
            message = 'Game Draw!'
        font = pg.font.Font(None, 30)
        text = font.render(message, 1, (255, 255, 255))
        # copy the rendered message onto the board
        self.screen.fill((0, 0, 0), (0, self.width, self.height + 100, 100))
        text_rect = text.get_rect(center=(self.width / 2, self.height + 100 - 50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def drawXO(self, row, col):
        posy = self.height / self.DIVIDE_NUM * (row + 1)
        posx = self.width / self.DIVIDE_NUM * (col + 1)
        self.Gomoku[row][col] = self.XO
        if self.XO == 'x':
            self.screen.blit(self.text_surfaceX, (posx, posy))
            pg.draw.circle(self.screen, self.black, (posx, posy), self.font_size, width=0)
            self.XO = 'o'
        else:
            self.screen.blit(self.text_surfaceO, (posx, posy))
            pg.draw.circle(self.screen, self.white, (posx, posy), self.font_size, width=0)
            self.XO = 'x'
        pg.display.update()

    # End of draw functions

    def game_opening(self):
        self.screen.blit(self.cover, (0, 0))
        pg.display.update()
        time.sleep(1)
        self.screen.fill(self.board_color)
        # Drawing vertical lines
        y1 = self.height / self.DIVIDE_NUM
        y2 = y1 * self.BOARD_SIZE
        for i in range(1, self.BOARD_SIZE + 1):
            x = self.width / self.DIVIDE_NUM * i
            pg.draw.line(self.screen, self.line_color, (x, y1),
                         (x, y2), 3)
        # Drawing horizontal lines
        x1 = self.width / self.DIVIDE_NUM
        x2 = x1 * self.BOARD_SIZE
        for i in range(1, self.BOARD_SIZE + 1):
            y = self.height / self.DIVIDE_NUM * i
            pg.draw.line(self.screen, self.line_color, (x1, y), (x2, y), 3)
        self.draw_status()


    def check_win(self):
        # check for winning rows
        self.draw_status()

    def userClick(self):
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()
        # get column of mouse click (1-BOARD_SIZE)
        if x < self.width:
            relative_pos = x / (self.width / self.BOARD_SIZE)
            col = math.floor(relative_pos)
        else:
            col = None
        # get row of mouse click (1-BOARD_SIZE)
        if y < self.height:
            row = math.floor(y / (self.height / self.BOARD_SIZE))
        else:
            row = None
        # print(row,col)
        if row is not None and col is not None and self.Gomoku[row][col] is None:
            # draw the x or o on screen
            self.drawXO(row, col)
            return row, col
        return -1, -1

    def get_color(self):
        if self.XO == 'x':
            return 1
        if self.XO == 'o':
            return 0

    def get_ticks(self):
        return pg.time.get_ticks()

    def reset_game(self):
        self.XO = 'x'
        self.isDraw = False
        self.game_opening()
        self.winner = None
        self.Gomoku = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]