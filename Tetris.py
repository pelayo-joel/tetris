from const import *
from widgets import *
from tetrisObj import *

pygame.init()        
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}Tetris69-Logo.png'))
bg = pygame.image.load(f"{IMAGE_PATH}bgPlayfield.png")
bg = pygame.transform.smoothscale(bg, (DISPLAY_W, DISPLAY_H))
DISPLAY = pygame.display.set_mode(DISPLAY_RES)
DISPLAY.blit(bg, (0, 0))

clock = pygame.time.Clock()
speed = TIME_INTERVAL
#pygame.time.set_timer(pygame.USEREVENT+1 , TIME_INTERVAL)
#(200, DISPLAY_H - 30)
#gfxButtonTest = GfxButton(DISPLAY, 220, DISPLAY_H, posX=330, posY=0, buttonLabel="Button")
playfield = PlayField(DISPLAY, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 173, 50, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS, border=True, borderWidth=9, borderColor=(95, 250, 195))
tetromino = Tetromino(playfield)
GameUI= InGame_UI(DISPLAY, playfield)
tetrominoBag = []
tetroHold = None

pygame.display.flip()

def NewTetromino():
    global tetrominoBag, tetromino, running
    if len(tetrominoBag) >= (len(list(Tetrominoes.keys())) * 2) - 2:
        tetrominoBag = []

    nextTetromino = Tetromino(playfield)
    nextTetromino.RerollShape(tetrominoBag, tetromino.shape)
    tetrominoBag.append(tetromino.shape)
    return nextTetromino

def InGameControls():
    global tetromino, tetroHold, speed
    keys = pygame.key.get_pressed()

    if event.type == pygame.KEYDOWN:
        tetromino.TetroControls(event.key)
        
        if event.key == pygame.K_ESCAPE:
            pygame.mixer.Sound.play(SoundEffects["Pause"])
            tetromino = NewTetromino()
            playfield.ClearStack()

        if event.key == pygame.K_SPACE:
            pygame.mixer.Sound.play(SoundEffects["Hold"])
            if tetromino.Hold(tetroHold) == tetromino:
                tetroHold = tetromino
                tetromino = NewTetromino()
                GameUI.UpdateHoldWindow(tetroHold.shape)
            else:
                tetromino, tetroHold = tetromino.Hold(tetroHold), tetromino
                GameUI.UpdateHoldWindow(tetroHold.shape)


    if keys[pygame.K_DOWN]  and not tetromino.get_TouchedGround():
        speed = FAST_TIME_INTERVAL
    else:
        speed = TIME_INTERVAL






#image=pygame.image.load(f"{IMAGE_PATH}GameField-UI_cropped.png")
#image=pygame.image.load(f"{IMAGE_PATH}GameField-UI_score.png")

if __name__ == "__main__":
    running = True
    while running:
        GameUI.UpdateUI()
        timer = pygame.time.get_ticks()
        clock.tick(FPS)
        #print(clock.get_time())

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            InGameControls()

        if timer > CLOCK and not tetromino.get_TouchedGround():
            tetromino.TetrominoFall()
            CLOCK += speed

        elif tetromino.Landed(CLOCK):
            tetromino.AddToStack()
            playfield.ClearingLines()
            GameUI.UpdateStatusWindow()

            if playfield.PlayfieldLvlUp():
                TIME_INTERVAL -= 30
            if playfield.CheckLoss():
                TIME_INTERVAL = 1000
                playfield.ClearStack()

            tetromino = NewTetromino()
            #CLOCK = timer
        
        playfield.DrawStack()
        pygame.display.update()
