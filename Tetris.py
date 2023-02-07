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
playfield = GridMap(DISPLAY, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 15, 20, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS)
tetrominoBag = []
tetromino = Tetromino(playfield)

pygame.display.flip()

def NewTetromino():
    global tetrominoBag, tetromino
    if len(tetrominoBag) >= (len(list(Tetrominoes.keys())) * 2) - 2:
        tetrominoBag = []

    nextTetromino = Tetromino(playfield)
    nextTetromino.RerollShape(tetrominoBag, tetromino.shape)
    tetrominoBag.append(tetromino.shape)
    tetromino = nextTetromino

def Controls(key):
    if key == K_q and tetromino.shape != "O" and not tetromino.Landed():
        tetromino.Rotate("CounterClockwise")
        print("should rotate left")
    if key == K_w and tetromino.shape != "O" and not tetromino.Landed():
        tetromino.Rotate("Clockwise")
        print("should rotate right")
    if key == K_LEFT and not tetromino.Landed():
        tetromino.Move(DIRECTIONS["left"])
        print("should go left")
    if key == K_RIGHT and not tetromino.Landed():
        tetromino.Move(DIRECTIONS["right"])
        print("should go right")

running = True
while running:
    timer = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_DOWN]:
            TIME_INTERVAL = 100
        if event.type == KEYDOWN:
            Controls(event.key)

    if timer > CLOCK:
        tetromino.TetrominoFall()
        CLOCK += TIME_INTERVAL
    if tetromino.Landed():
        NewTetromino()
    
    pygame.display.update()
