import pygame

vector = pygame.math.Vector2

FPS = 60
DISPLAY_BG = 0
PLAYFIELD_BG = 0


AUDIO_PATH = ""
IMAGE_PATH = "images-src/"
FONT_PATH = ""


DISPLAY_RES = DISPLAY_W, DISPLAY_H = 550, 690

PLAYFIELD_CELL_SIZE = 30
PLAYFIELD_COLUMNS, PLAYFIELD_ROWS = 10, 20
PLAYFIELD_RES = PLAYFIELD_W, PLAYFIELD_H = PLAYFIELD_COLUMNS * PLAYFIELD_CELL_SIZE, PLAYFIELD_ROWS * PLAYFIELD_CELL_SIZE
SIDE_PANEL_RES = DISPLAY_W - PLAYFIELD_W - 20, DISPLAY_H - PLAYFIELD_H - 20


Tetrominoes = {
    "I":[(0, 0), (0, 1), (0, -1), (0, -2)],
    "T":[(0, 0), (-1, -1), (0, 1), (1, 0)],
    "J":[(0, 0), (0, 1), (0, -1), (-1, -1)],
    "L":[(0, 0), (0, 1), (0, -1), (1, -1)],
    "S":[(0, 0), (0, 1), (-1, 1), (1, 0)],
    "Z":[(0, 0), (-1, 0), (0, 1), (1, 1)],
    "O":[(0, 0), (0, 1), (1, 0), (1, 1)],
}