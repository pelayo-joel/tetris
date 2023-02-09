import pygame
import random

vector = pygame.math.Vector2

FPS = 60
CLOCK = 0
TIME_INTERVAL = 1150
DISPLAY_BG = 0
PLAYFIELD_BG = 0


AUDIO_PATH = ""
IMAGE_PATH = f"images-src/"
TILE_PATH = f"images-src/TetrominoBlock/"
FONT_PATH = ""


DISPLAY_RES = DISPLAY_W, DISPLAY_H = 550, 690

PLAYFIELD_CELL_SIZE = 30
PLAYFIELD_COLUMNS, PLAYFIELD_ROWS = 10, 20
PLAYFIELD_RES = PLAYFIELD_W, PLAYFIELD_H = PLAYFIELD_COLUMNS * PLAYFIELD_CELL_SIZE, PLAYFIELD_ROWS * PLAYFIELD_CELL_SIZE
SIDE_PANEL_RES = DISPLAY_W - PLAYFIELD_W - 20, DISPLAY_H - PLAYFIELD_H - 20

DIRECTIONS = {"down":vector(0, 1), "left":vector(-1, 0), "right":vector(1, 0)}
SPAWN_POS = vector((PLAYFIELD_COLUMNS / 2) - 1, -1)

Tetrominoes = {
    "I":[(0, 0), (-1, 0), (1, 0), (2, 0)],
    "T":[(0, 0), (-1, 0), (0, -1), (1, 0)],
    "J":[(0, 0), (-1, 0), (1, 0), (-1, -1)],
    "L":[(0, 0), (-1, 0), (1, 0), (1, -1)],
    "S":[(0, 0), (-1, 0), (0, -1), (1, -1)],
    "Z":[(0, 0), (-1, -1), (0, -1), (1, 0)],
    "O":[(0, 0), (0, -1), (1, 0), (1, -1)]
}

RotationState = ["0", "R", "2", "L"]

WallKickData = {
    "IKick":{
        "0":[vector(-2, 0), vector(1, 0), vector(-2, 1), vector(1, -2)],
        "R":[vector(-1, 0), vector(2, 0), vector(-1,-2), vector(2, 1)],
        "2":[vector(2, 0), vector(-1, 0), vector(2, -1), vector(-1, 2)],
        "L":[vector(1, 0), vector(-2, 0), vector(1, 2), vector(-2, -1)],
    },
    "CommonKick":{
        "0":[vector(-1, 0), vector(-1, -1), vector(0, 2), vector(-1, 2)],
        "R":[vector(1, 0), vector(1, 1), vector(0,-2), vector(1, 2)],
        "2":[vector(1, 0), vector(1, -1), vector(0, 2), vector(1, 2)],
        "L":[vector(-1, 0), vector(-1, 1), vector(0, -2), vector(-1, -2)],
    }
}
