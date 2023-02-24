import Tetris
from const import *
from widgets import *

pygame.init()
pygame.display.set_caption('Tetris69')
pygame.display.set_icon(pygame.image.load(f'{IMAGE_PATH}Tetris69-Logo.png'))

DISPLAY = pygame.display.set_mode(DISPLAY_RES)

gameBg = pygame.image.load(f"{UI_PATH}Background/Tetris69-bgPlayfield.png")
gameBg = pygame.transform.smoothscale(gameBg, (DISPLAY_W, DISPLAY_H))
menuBg = pygame.image.load(f"{UI_PATH}Background/Tetris69-MENU.jpg")
menuBg = pygame.transform.smoothscale(menuBg, (DISPLAY_W + 300, DISPLAY_H))

GAME_SCENE = Frame(DISPLAY, (DISPLAY_W, DISPLAY_H), color=(1, 1, 1), surfImage=gameBg)
MENU_SCENE = Frame(DISPLAY, (DISPLAY_W, DISPLAY_H), color=(1, 1, 1), surfImage=menuBg)

SCORE_MANAGER = Tetris.ScoreManager(MENU_SCENE)

clock = pygame.time.Clock()
speed = TIME_INTERVAL




if __name__ == "__main__":

    while RUNNING:

        if STATE == "Game":
            Game = Tetris.Game(GAME_SCENE, GAMEMODE, SCORE_MANAGER)

            while STATE == "Game":
                Game.GameLoop()
                RUNNING, STATE, MENUSTATE = Game.GetStates()
                
                if Game.Restart():
                    break

            GAME_SCENE.blit(GAME_SCENE.surfImage, (0, 0))
            GAME_SCENE.ActiveFrame()
            pygame.display.update()

        elif STATE == "Menu":
            Menu = Tetris.Menu(MENU_SCENE, MENUSTATE, SCORE_MANAGER)

            while STATE == "Menu":
                Menu.MenuLoop()
                RUNNING, STATE, GAMEMODE = Menu.GetStates()

            
