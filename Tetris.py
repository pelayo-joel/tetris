from const import *
from tetrisObj import *

class Game:
    def __init__(self, scene:pygame.Surface, mode:str):
        self.scene = scene
        self.mode = mode

        self.playfield = PlayField(self.scene, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 173, 50, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS, border=True, borderWidth=9, borderColor=(95, 250, 195))
        self.tetromino = Tetromino(self.playfield)
        self.nextTetromino = Tetromino(self.playfield)
        self.GameUI = InGame_UI(self.scene, self.playfield)

        self.clock = pygame.time.Clock()
        self.speed = TIME_INTERVAL

        self.GameUI.UpdateNextWindow(self.nextTetromino.shape)
        self.tetrominoBag = []
        self.tetroHold = None
        self.nextTetromino.RerollShape(self.tetrominoBag, self.tetromino.shape)

        pygame.display.flip()
        pygame.mixer.music.load(InGameMusic["PlayField"])
        pygame.mixer.music.set_volume(0.125)
        pygame.mixer.music.play(-1)

    def __NewTetromino(self):

        if len(self.tetrominoBag) >= (len(list(Tetrominoes.keys())) * 2) - 3:
            self.tetrominoBag = []

        self.tetrominoBag.append(self.tetromino.shape)
        self.tetromino = self.nextTetromino
        self.nextTetromino = Tetromino(self.playfield)

        self.nextTetromino.RerollShape(self.tetrominoBag, self.tetromino.shape)
        self.GameUI.UpdateNextWindow(self.nextTetromino.shape)

    def __GamePause(self):
        global PAUSE, CLOCK
        
        while PAUSE:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        pygame.mixer.music.unpause()
                        pygame.mixer.Sound.play(SoundEffects["Pause"])
                        CLOCK = pygame.time.get_ticks()
                        PAUSE = False

    def __InGameControls(self, event):
        global PAUSE

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            self.tetromino.TetroControls(event.key)
            

            if event.key == pygame.K_SPACE:

                if self.tetromino.Hold(self.tetroHold) == self.tetromino:
                    self.tetroHold = self.tetromino
                    self.__NewTetromino()
                    self.GameUI.UpdateHoldWindow(self.tetroHold.shape)
                    pygame.mixer.Sound.play(SoundEffects["Hold"])

                elif not self.tetromino.Hold(self.tetroHold):
                    pass

                else:
                    self.tetromino, self.tetroHold = self.tetromino.Hold(self.tetroHold), self.tetromino
                    self.GameUI.UpdateHoldWindow(self.tetroHold.shape)
                    pygame.mixer.Sound.play(SoundEffects["Hold"])

            if event.key == pygame.K_ESCAPE:
                PAUSE = True
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SoundEffects["Pause"])

            if event.key == pygame.K_BACKSPACE:
                self.__NewTetromino()
                self.GameUI.UpdateHoldWindow()
                self.tetroHold = None
                self.playfield.ClearStatus()
                self.playfield.ClearStack()
                self.GameUI.UpdateStatusWindow()
                pygame.mixer.Sound.play(SoundEffects["Clear"])

        if keys[pygame.K_DOWN] and not self.tetromino.get_TouchedGround():
            self.speed = FAST_TIME_INTERVAL
        else:
            self.speed = TIME_INTERVAL



    def GameLoop(self):
        global CLOCK, RUNNING, TIME_INTERVAL
        self.GameUI.UpdateUI()
        timer = pygame.time.get_ticks()
        self.clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False

            self.__InGameControls(event)
        
        self.__GamePause()


        if timer > CLOCK and not self.tetromino.get_TouchedGround():
            self.tetromino.TetrominoFall()
            CLOCK += self.speed


        elif self.tetromino.Landed(CLOCK):
            self.tetromino.AddToStack()
            self.playfield.ClearingLines()

            if self.playfield.PlayfieldLvlUp():
                TIME_INTERVAL -= 40

            if self.playfield.CheckLoss():
                TIME_INTERVAL = 1000
                self.GameUI.UpdateHoldWindow()
                self.tetroHold = None

            self.GameUI.UpdateStatusWindow()
            self.__NewTetromino()
        

        self.playfield.DrawStack()

        self.scene.ActiveFrame()
        pygame.display.update()





class Menu:
    def __init__(self, scene:pygame.Surface):
        self.scene = scene
        #self.playButton = widgets.Button

        pygame.display.flip()
        pygame.mixer.music.load(InGameMusic["Menu"])
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    def MenuLoop(self):
        return None