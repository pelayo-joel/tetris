from const import *
from widgets import *
from tetrisObj import *

pygame.init()
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}Tetris69-Logo.png'))

DISPLAY = pygame.display.set_mode(DISPLAY_RES)

gameBg = pygame.image.load(f"{UI_PATH}Background/Tetris69-bgPlayfield.png")
gameBg = pygame.transform.smoothscale(gameBg, (DISPLAY_W, DISPLAY_H))
menuBg = None

GAME_SCENE = widgets.Frame(DISPLAY, (DISPLAY_W, DISPLAY_H), color=(1, 1, 1), surfImage=gameBg)
MENU_SCENE = pygame.Surface((DISPLAY_W, DISPLAY_H))

#GAME_SCENE.blit(bg, (0, 0))

clock = pygame.time.Clock()
speed = TIME_INTERVAL

playfield = PlayField(GAME_SCENE, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 173, 50, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS, border=True, borderWidth=9, borderColor=(95, 250, 195))
tetromino = Tetromino(playfield)
nextTetromino = Tetromino(playfield)
GameUI = InGame_UI(GAME_SCENE, playfield)

GameUI.UpdateNextWindow(nextTetromino.shape)
tetrominoBag = []
tetroHold = None
nextTetromino.RerollShape(tetrominoBag, tetromino.shape)

pygame.display.flip()
pygame.mixer.music.load(InGameMusic["PlayField"])
pygame.mixer.music.set_volume(0.125)
pygame.mixer.music.play(-1)


def NewTetromino():
    global tetrominoBag, tetromino, nextTetromino, GameUI

    if len(tetrominoBag) >= (len(list(Tetrominoes.keys())) * 2) - 3:
        tetrominoBag = []

    tetrominoBag.append(tetromino.shape)
    tetromino = nextTetromino
    nextTetromino = Tetromino(playfield)

    nextTetromino.RerollShape(tetrominoBag, tetromino.shape)
    GameUI.UpdateNextWindow(nextTetromino.shape)


def InGameControls():
    global tetromino, tetroHold, speed

    keys = pygame.key.get_pressed()

    if event.type == pygame.KEYDOWN:
        tetromino.TetroControls(event.key)
        
        if event.key == pygame.K_ESCAPE:
            pygame.mixer.Sound.play(SoundEffects["Pause"])
            NewTetromino()
            GameUI.UpdateHoldWindow()
            tetroHold = None
            playfield.ClearStatus()
            playfield.ClearStack()
            GameUI.UpdateStatusWindow()

        if event.key == pygame.K_SPACE:
            pygame.mixer.Sound.play(SoundEffects["Hold"])

            if tetromino.Hold(tetroHold) == tetromino:
                tetroHold = tetromino
                NewTetromino()
                GameUI.UpdateHoldWindow(tetroHold.shape)

            elif not tetromino.Hold(tetroHold):
                pass

            else:
                tetromino, tetroHold = tetromino.Hold(tetroHold), tetromino
                GameUI.UpdateHoldWindow(tetroHold.shape)


    if keys[pygame.K_DOWN] and not tetromino.get_TouchedGround():
        speed = FAST_TIME_INTERVAL
    else:
        speed = TIME_INTERVAL







if __name__ == "__main__":

    while RUNNING:
        GameUI.UpdateUI()
        timer = pygame.time.get_ticks()
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                
            InGameControls()

        if timer > CLOCK and not tetromino.get_TouchedGround():
            tetromino.TetrominoFall()
            CLOCK += speed

        elif tetromino.Landed(CLOCK):
            tetromino.AddToStack()
            playfield.ClearingLines()

            if playfield.PlayfieldLvlUp():
                TIME_INTERVAL -= 40

            if playfield.CheckLoss():
                TIME_INTERVAL = 1000
                GameUI.UpdateHoldWindow()
                tetroHold = None

            GameUI.UpdateStatusWindow()
            NewTetromino()
        
        playfield.DrawStack()

        GAME_SCENE.ActiveFrame()
        pygame.display.update()
