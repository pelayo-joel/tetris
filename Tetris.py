from const import *
from widgets import *
from tetrisObj import *

pygame.init()        
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}tetris69.png'))
clock = pygame.time.Clock()
clock.tick(FPS)
pygame.time.set_timer(pygame.USEREVENT+1 , TIME_INTERVAL)
DISPLAY = pygame.display.set_mode(DISPLAY_RES)
DISPLAY.fill((25, 25, 25))

gfxButtonTest = GfxButton(DISPLAY, 220, 690, posX=330, posY=0, buttonLabel="Button")
playfield = PlayField(DISPLAY, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 15, 20, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS)
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

"""def HoldTetromino():
    global tetroHold, tetromino
    if tetroHold == None:
        tetroHold = tetromino
        NewTetromino()
    else:
        tetroHold, tetromino = tetromino, tetroHold"""

def Controls(key):
    global tetromino, tetroHold
    
    tetromino.TetroControls(key)

    if key == pygame.K_ESCAPE:
        tetromino = NewTetromino()
        playfield.ClearStack()

    if key == pygame.K_SPACE:
        pygame.mixer.Sound.play(SoundEffects["Hold"])
        if tetromino.Hold(tetroHold) == tetromino:
            tetroHold = tetromino
            tetromino = NewTetromino()
        else:
            tetromino, tetroHold = tetromino.Hold(tetroHold), tetromino







if __name__ == "__main__":
    running = True
    while running:
        timer = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_DOWN]:
                TIME_INTERVAL = 100
            else:
                TIME_INTERVAL = 1150
            if event.type == pygame.KEYDOWN:
                Controls(event.key)

        if timer > CLOCK:
            tetromino.TetrominoFall()
            CLOCK += TIME_INTERVAL

        if tetromino.Landed():
            tetromino.AddToStack()
            playfield.ClearLines()

            if playfield.CheckLoss():
                playfield.ClearStack()

            tetromino = NewTetromino()
        
        playfield.DrawStack()
        pygame.display.update()
