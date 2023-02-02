from const import *
from widgets import *
import tetrisObj

pygame.init()
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}tetris69.png'))
DISPLAY = pygame.display.set_mode(DISPLAY_RES)
DISPLAY.fill((25, 25, 25))
gfxButtonTest = GfxButton(DISPLAY, 220, 690, posX=330, posY=0, buttonLabel="Button")
grid = GridMap(DISPLAY, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 15, 20, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
