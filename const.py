import pygame
import random

vector = pygame.math.Vector2
pygame.mixer.init()


#Time/State variables

RUNNING = True
PAUSE = False
STATE = "Menu"
GAMEMODE = "Training"
FPS = 60
CLOCK = 0
TIME_INTERVAL = 1000
FAST_TIME_INTERVAL = 100
LOCK_DELAY = 1.5


#Path variables

MUSIC_PATH = f"Audio/Music/"
SFX_PATH = f"Audio/sfx/"
IMAGE_PATH = f"images-src/"
UI_PATH = f"images-src/Game-UI/"
TILE_PATH = f"images-src/TetrominoBlock/"
FONT_PATH = "Fonts/yearone.ttf"


#Resolution/Size variables

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 650, 700

PLAYFIELD_CELL_SIZE = 30
PLAYFIELD_COLUMNS, PLAYFIELD_ROWS = 10, 20
PLAYFIELD_RES = PLAYFIELD_W, PLAYFIELD_H = PLAYFIELD_COLUMNS * PLAYFIELD_CELL_SIZE, PLAYFIELD_ROWS * PLAYFIELD_CELL_SIZE
SIDE_PANEL_RES = DISPLAY_W - PLAYFIELD_W - 20, DISPLAY_H - PLAYFIELD_H - 20


#Tetromino data

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


#Sound variables

InGameMusic = {
    "PlayField":f"{MUSIC_PATH}NotTetris99-Tetris.mp3",
    "PlayFieldLvl25":f"{MUSIC_PATH}NotTetris99-Lvl25.mp3",
    "PlayFieldHELL":f"{MUSIC_PATH}NotTetris99-HELL.mp3",
    "Results":f"{MUSIC_PATH}NotTetris99-Results.mp3",
    "Menu":f"{MUSIC_PATH}NotTetris99-Menu.mp3"
}

SoundEffects = {
    "Move":pygame.mixer.Sound(f"{SFX_PATH}move.wav"),
    "Rotate":pygame.mixer.Sound(f"{SFX_PATH}rotate.wav"),
    "GroundTouch":pygame.mixer.Sound(f"{SFX_PATH}onground.wav"),
    "Landed":pygame.mixer.Sound(f"{SFX_PATH}landed.wav"),
    "Drop":pygame.mixer.Sound(f"{SFX_PATH}drop.wav"),
    "Hold":pygame.mixer.Sound(f"{SFX_PATH}hold.wav"),
    "Pause":pygame.mixer.Sound(f"{SFX_PATH}pause.wav"),
    "Clear":pygame.mixer.Sound(f"{SFX_PATH}clear.wav"),
    "Select":pygame.mixer.Sound(f"{SFX_PATH}select.wav"),
    "Confirm":pygame.mixer.Sound(f"{SFX_PATH}confirm.wav"),
    "Return":pygame.mixer.Sound(f"{SFX_PATH}return.wav"),
    "Save":pygame.mixer.Sound(f"{SFX_PATH}save.wav"),
    "GameOver":pygame.mixer.Sound(f"{SFX_PATH}gameover.wav"),

    "ClearedLines":{
        "Single":pygame.mixer.Sound(f"{SFX_PATH}single.wav"),
        "Double":pygame.mixer.Sound(f"{SFX_PATH}double.wav"),
        "Triple":pygame.mixer.Sound(f"{SFX_PATH}triple.wav"),
        "Tetris":pygame.mixer.Sound(f"{SFX_PATH}tetris.wav")
    },

    "LvlUp":pygame.mixer.Sound(f"{SFX_PATH}lvlup.wav"),
    "Lvl25":pygame.mixer.Sound(f"{SFX_PATH}lvl25.wav"),
    "HELL":pygame.mixer.Sound(f"{SFX_PATH}HELL.wav"),
    "NICE":pygame.mixer.Sound(f"{SFX_PATH}NICE.mp3")
}

for sfx in SoundEffects:

    if type(SoundEffects[sfx]) is dict:
        for lineSound in SoundEffects[sfx]:
            SoundEffects[sfx][lineSound].set_volume(0.35)

    else:
        SoundEffects[sfx].set_volume(0.5)

SoundEffects["LvlUp"].set_volume(0.3)
SoundEffects["Pause"].set_volume(0.1)
SoundEffects["NICE"].set_volume(1.0)
