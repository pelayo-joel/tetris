import pygame
import random

vector = pygame.math.Vector2
pygame.mixer.init()

FPS = 60
CLOCK = 0
TIME_INTERVAL = 1000
FAST_TIME_INTERVAL = 100
LOCK_DELAY = 1.5
DISPLAY_BG = 0
PLAYFIELD_BG = 0


AUDIO_PATH = f"Audio/"
SFX_PATH = f"Audio/sfx/"
IMAGE_PATH = f"images-src/"
TILE_PATH = f"images-src/TetrominoBlock/"
FONT_PATH = "Fonts/yearone.ttf"


DISPLAY_RES = DISPLAY_W, DISPLAY_H = 650, 700

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

SoundEffects = {
    "Move":pygame.mixer.Sound(f"{SFX_PATH}move.wav"),
    "Rotate":pygame.mixer.Sound(f"{SFX_PATH}rotate.wav"),
    "Landed":pygame.mixer.Sound(f"{SFX_PATH}landed.wav"),
    "Drop":pygame.mixer.Sound(f"{SFX_PATH}drop.wav"),
    "Hold":pygame.mixer.Sound(f"{SFX_PATH}hold.wav"),
    "Pause":pygame.mixer.Sound(f"{SFX_PATH}pause.wav"),

    "ClearedLines":{
        "Single":pygame.mixer.Sound(f"{SFX_PATH}single.wav"),
        "Double":pygame.mixer.Sound(f"{SFX_PATH}double.wav"),
        "Triple":pygame.mixer.Sound(f"{SFX_PATH}triple.wav"),
        "Tetris":pygame.mixer.Sound(f"{SFX_PATH}tetris.wav")
    },

    "NICE":pygame.mixer.Sound(f"{SFX_PATH}NICE.mp3")
}


for sfx in SoundEffects:
    if type(SoundEffects[sfx]) is dict:
        for lineSound in SoundEffects[sfx]:
            SoundEffects[sfx][lineSound].set_volume(0.35)
    else:
        SoundEffects[sfx].set_volume(0.5)

SoundEffects["Pause"].set_volume(0.1)
SoundEffects["NICE"].set_volume(1.0)
