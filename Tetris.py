from const import *
from widgets import *
from tetrisObj import *

pygame.init()        
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}tetris69.png'))
bg = pygame.image.load(f"{IMAGE_PATH}bgPlayfield.png")
bg = pygame.transform.smoothscale(bg, (DISPLAY_W + 230, DISPLAY_H))
DISPLAY = pygame.display.set_mode(DISPLAY_RES)
DISPLAY.blit(bg, (-230, 0))

clock = pygame.time.Clock()
speed = TIME_INTERVAL
#pygame.time.set_timer(pygame.USEREVENT+1 , TIME_INTERVAL)

#gfxButtonTest = GfxButton(DISPLAY, 220, DISPLAY_H, posX=330, posY=0, buttonLabel="Button")
playfield = PlayField(DISPLAY, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 30, 30, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS)
sidePanel = InGame_UI(DISPLAY, (250, DISPLAY_H - 30), (345, 20), (0, 0, 0), playfieldToMonitor=playfield)
tetrominoBag = []
tetromino = Tetromino(playfield)
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

def InGameControls(keyEvent):
    global tetromino, tetroHold, speed
    keys = pygame.key.get_pressed()

    if event.type == pygame.KEYDOWN:
        tetromino.TetroControls(event.key)
        
        if event.key == pygame.K_ESCAPE:
            tetromino = NewTetromino()
            playfield.ClearStack()

        if event.key == pygame.K_SPACE:
            pygame.mixer.Sound.play(SoundEffects["Hold"])
            if tetromino.Hold(tetroHold) == tetromino:
                tetroHold = tetromino
                tetromino = NewTetromino()
            else:
                tetromino, tetroHold = tetromino.Hold(tetroHold), tetromino


    if keys[pygame.K_DOWN]:
        speed = FAST_TIME_INTERVAL
    else:
        speed = TIME_INTERVAL








if __name__ == "__main__":
    running = True
    while running:
        sidePanel.ActiveFrame()
        timer = pygame.time.get_ticks()
        clock.tick(FPS)
        #print(clock.get_time())

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            InGameControls(event.type)

        if timer > CLOCK:
            #print(timer, CLOCK)
            tetromino.TetrominoFall()
            CLOCK += speed

        if tetromino.Landed():
            tetromino.AddToStack()
            playfield.ClearLines()

            if playfield.CheckLoss():
                playfield.ClearStack()

            tetromino = NewTetromino()
        
        playfield.DrawStack()
        pygame.display.update()
