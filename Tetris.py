from const import *
from tetrisObj import *

class Game:
    def __init__(self, scene:pygame.Surface, mode:str):
        global CLOCK, TIME_INTERVAL
        self.scene = scene
        self.__mode = mode
        self.__restart = False

        self.playfield = PlayField(self.scene, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE), 173, 50, PLAYFIELD_COLUMNS, PLAYFIELD_ROWS, mode=self.__mode, border=True, borderWidth=9, borderColor=(95, 250, 195))
        self.tetromino = Tetromino(self.playfield)
        self.nextTetromino = Tetromino(self.playfield)
        self.GameUI = InGame_UI(self.scene, self.playfield)

        self.clock = pygame.time.Clock()
        CLOCK = pygame.time.get_ticks()

        self.sec = 0
        self.speed = TIME_INTERVAL

        self.GameUI.UpdateNextWindow(self.nextTetromino.shape)
        self.tetrominoBag = []
        self.tetroHold = None
        self.nextTetromino.RerollShape(self.tetrominoBag, self.tetromino.shape)

        pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


        if self.__mode != "Training":
            self.GameUI.UpdateUI()
            self.__StartupCountdown()
            CLOCK = pygame.time.get_ticks()

        if self.__mode == "Marathon":
            TIME_INTERVAL -= 675
            pygame.mixer.music.load(InGameMusic["PlayFieldLvl25"])
            pygame.mixer.music.set_volume(0.3)
        else:
            pygame.mixer.music.load(InGameMusic["PlayField"])
            pygame.mixer.music.set_volume(0.2)

        pygame.mixer.music.play(-1)

    def __ChangeGameState(self):
        global STATE, MENUSTATE, PAUSE
        PAUSE, STATE, MENUSTATE = False, "Menu", "Game Modes"

    def __StartupCountdown(self):
        start = pygame.time.get_ticks()
        startTimer = 0
        pygame.mixer.Sound.play(SoundEffects["Ready"])

        while pygame.time.get_ticks() < start + 5000:
            startTimer = pygame.time.get_ticks() - start

            if pygame.time.get_ticks() >= start + 4000:
                pygame.mixer.Sound.play(SoundEffects["Go"])
            else:
                pygame.mixer.Sound.play(SoundEffects["Count"])


            self.playfield.GridUpdate()
            countdownImage, sceneCenter = self.GameUI.Countdown()
            self.scene.blit(countdownImage, sceneCenter)
            self.GameUI.UpdateUI()
            self.scene.parent.blit(self.scene.surfImage, (0, 0))
            self.scene.ActiveFrame()
            pygame.display.update()
            pygame.time.wait(1000)

        self.playfield.start += startTimer

    def __Clear(self):
        global PAUSE, CLOCK
        self.__NewTetromino()
        self.GameUI.UpdateHoldWindow()
        self.tetroHold = None
        self.playfield.ClearStatus()
        self.playfield.ClearStack()
        self.GameUI.UpdateStatusWindow()
        #self.playfield.start += pauseTimer
        CLOCK = pygame.time.get_ticks()
        PAUSE = False
        pygame.mixer.Sound.play(SoundEffects["Clear"])

    def __WillRestart(self):
        self.__restart = True
        self.playfield.ClearStatus()
        self.playfield.ClearStack()

    def __NewTetromino(self):

        if len(self.tetrominoBag) >= (len(list(Tetrominoes.keys())) * 2) - 3:
            self.tetrominoBag = []

        self.tetrominoBag.append(self.tetromino.shape)
        self.tetromino = self.nextTetromino
        self.nextTetromino = Tetromino(self.playfield)

        self.nextTetromino.RerollShape(self.tetrominoBag, self.tetromino.shape)
        self.GameUI.UpdateNextWindow(self.nextTetromino.shape)

    def __GamePause(self):
        global PAUSE, CLOCK, RUNNING, STATE
        pauseStart = pygame.time.get_ticks()


        while PAUSE:
            self.GameUI.pauseArrowNav[0].Command(self.__ChangeGameState)
            self.GameUI.pauseArrowNav[1].Command(self.__Clear)

            pauseTimer = int(pygame.time.get_ticks() - pauseStart)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False
                    STATE = None
                    PAUSE = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        pygame.mixer.music.unpause()
                        pygame.mixer.Sound.play(SoundEffects["Pause"])
                        self.playfield.start += pauseTimer
                        CLOCK = pygame.time.get_ticks()
                        PAUSE = False

                    if event.key == pygame.K_UP:
                        self.GameUI.pauseSelector -= 1
                        self.GameUI.pauseSelector = (self.GameUI.pauseSelector % len(self.GameUI.pauseArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])

                    if event.key == pygame.K_DOWN:
                        self.GameUI.pauseSelector += 1
                        self.GameUI.pauseSelector = (self.GameUI.pauseSelector % len(self.GameUI.pauseArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])

                    if event.key == pygame.K_RETURN:
                        self.GameUI.pauseArrowNav[self.GameUI.pauseSelector].Click(input=True)
                        pygame.mixer.Sound.play(SoundEffects["Confirm"])
            
            self.GameUI.PauseScreen()
            self.scene.ActiveFrame()
            pygame.display.update()

    def __GameOver(self):
        global RUNNING, STATE
        gameOver = True
        timeSpent = self.playfield.DisplayClock()
        pygame.mixer.Sound.play(SoundEffects["GameOver"])
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.time.wait(5000)

        pygame.mixer.Sound.play(SoundEffects["Save"])
        pygame.mixer.music.load(InGameMusic["Results"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        while gameOver:
            self.GameUI.gameOverArrowNav[0].Command(self.__ChangeGameState)
            self.GameUI.gameOverArrowNav[1].Command(self.__WillRestart)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False
                    STATE = None
                    gameOver = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.GameUI.gameOverSelector -= 1
                        self.GameUI.gameOverSelector = (self.GameUI.gameOverSelector % len(self.GameUI.gameOverArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])

                    if event.key == pygame.K_RIGHT:
                        self.GameUI.gameOverSelector += 1
                        self.GameUI.gameOverSelector = (self.GameUI.gameOverSelector % len(self.GameUI.gameOverArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])

                    if event.key == pygame.K_RETURN:
                        gameOver = False
                        self.GameUI.gameOverArrowNav[self.GameUI.gameOverSelector].Click(input=True)
                        pygame.mixer.Sound.play(SoundEffects["Confirm"])

            self.GameUI.GameOverScreen(self.__mode, timeSpent)
            self.scene.ActiveFrame()
            pygame.display.update()

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

            if event.key == pygame.K_ESCAPE and self.__mode == "Training":
                PAUSE = True
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SoundEffects["Pause"])

            if event.key == pygame.K_BACKSPACE and self.__mode == "Training":
                self.__Clear()

        if keys[pygame.K_DOWN] and not self.tetromino.get_TouchedGround():
            self.speed = FAST_TIME_INTERVAL
        else:
            self.speed = TIME_INTERVAL


    def GameLoop(self):
        global CLOCK, RUNNING, TIME_INTERVAL, STATE
        timer = pygame.time.get_ticks()
        self.clock.tick(FPS)
        self.GameUI.UpdateUI()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                STATE = None

            self.__InGameControls(event)
        
        self.__GamePause()

        if timer > CLOCK and not self.tetromino.get_TouchedGround():
            self.tetromino.TetrominoFall()
            CLOCK += self.speed


        elif self.tetromino.Landed(CLOCK):
            self.tetromino.AddToStack()
            self.playfield.ClearingLines()

            if self.playfield.PlayfieldLvlUp():
                if self.playfield.GetPlayfieldLvl() >= 25:
                    TIME_INTERVAL -= 50
                elif self.playfield.GetPlayfieldLvl() >= 31:
                    TIME_INTERVAL -= 95
                else:
                    TIME_INTERVAL -= 25

                TIME_INTERVAL = max(30, TIME_INTERVAL)

            if self.playfield.CheckLoss():
                TIME_INTERVAL = 1000
                self.tetroHold = None

                if self.__mode == "Training":
                    self.GameUI.UpdateHoldWindow()
                else:
                    self.tetromino.TetroKill()
                    self.playfield.DrawStack()
                    self.__GameOver()

            self.__NewTetromino()

        elif self.__mode == "Marathon" and self.playfield.sec == 61:
            self.tetromino.TetroKill()
            self.playfield.DrawStack()
            self.__GameOver()
        
        self.GameUI.UpdateStatusWindow()
        self.playfield.DrawStack()
        self.scene.ActiveFrame()
        pygame.display.update()

    def Restart(self):
        return self.__restart

    def GetStates(self):
        return RUNNING, STATE, MENUSTATE





class Menu:
    def __init__(self, scene:pygame.Surface, state:str):
        self.scene = scene

        self.mainLogo = pygame.image.load(f"{IMAGE_PATH}Tetris69-Logo.png")
        self.mainLogo = pygame.transform.smoothscale(self.mainLogo, (450, 430))
        self.focusedButton = pygame.image.load(f"{UI_PATH}Button2(focused).png")
        self.focusedButton = pygame.transform.smoothscale(self.focusedButton, (320, 80))


        self.mainMenuGame = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=55, type="OnClick", buttonLabel="Game Modes", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Game Modes"))
        self.mainMenuScore = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=70, type="OnClick", buttonLabel="Score Board", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Score Board"))
        self.mainMenuCredits = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=85, type="OnClick", buttonLabel="Credits", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Credits"))

        self.gameMenuTraining = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=25, type="OnClick", buttonLabel="Training", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Training"))
        self.gameMenuClassic = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=40, type="OnClick", buttonLabel="Classic", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Classic"))
        self.gameMenuMarathon = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=55, type="OnClick", buttonLabel="Marathon", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Marathon"))
        self.gameMenuSurvival = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=70, type="OnClick", buttonLabel="Survival", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Survival"))


        self.menuState = state
        self.mainMenuArrowNav = [self.mainMenuGame, self.mainMenuScore, self.mainMenuCredits]
        self.gameMenuArrowNav = [self.gameMenuTraining, self.gameMenuClassic, self.gameMenuMarathon, self.gameMenuSurvival]
        self.currentMenu = []
        self.arrowSelector = 0
        self.menuDepth = 0

        pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(InGameMusic["Menu"])
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

    def __ChangeMenuState(self, nextState:str):
        self.menuState = nextState
        self.arrowSelector = 0
        self.scene.parent.blit(self.scene.surfImage, (0, 0))
        self.scene.ActiveFrame()
        pygame.display.update()

    def __ChangeGameState(self, gameMode:str):
        global STATE, GAMEMODE
        GAMEMODE = gameMode
        STATE = "Game"

    def __MenuControls(self):
        global RUNNING, STATE

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                STATE = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.arrowSelector -= 1
                    pygame.mixer.Sound.play(SoundEffects["Select"])

                if event.key == pygame.K_DOWN:
                    self.arrowSelector += 1
                    pygame.mixer.Sound.play(SoundEffects["Select"])

                if event.key == pygame.K_RETURN:
                    self.currentMenu[self.arrowSelector].Click(input=True)
                    pygame.mixer.Sound.play(SoundEffects["Confirm"])

                if event.key == pygame.K_BACKSPACE:
                    self.__ChangeMenuState("Main Menu")
                    pygame.mixer.Sound.play(SoundEffects["Return"])
                
                self.arrowSelector = (self.arrowSelector % len(self.currentMenu))

    def __MainMenu(self):
        self.scene.parent.blit(self.mainLogo, ((self.scene.parent.get_width() / 2) - (self.mainLogo.get_width() / 2), -50))
        self.currentMenu = self.mainMenuArrowNav
        self.__MenuControls()

        for mainMenuButton in self.currentMenu:
            mainMenuButton.ActiveButton()

        self.currentMenu[self.arrowSelector].ActiveButton(focused=True, focusedImage=self.focusedButton)

    def __ScoreMenu(self):
        self.__MenuControls()
        self.mainMenuGame.ActiveButton()
        self.mainMenuScore.ActiveButton()
        self.mainMenuCredits.ActiveButton()

    def __GameMenu(self):
        self.currentMenu = self.gameMenuArrowNav
        self.__MenuControls()

        for gameMenuButton in self.currentMenu:
            gameMenuButton.ActiveButton()

        self.currentMenu[self.arrowSelector].ActiveButton(focused=True, focusedImage=self.focusedButton)

    def MenuLoop(self):
        self.scene.ActiveFrame()

        if self.menuState == "Main Menu":
            self.__MainMenu()
        elif self.menuState == "Game Modes":
            self.__GameMenu()
        elif self.menuState == "Score Board":
            self.__ScoreMenu()

        pygame.display.update()

    def GetStates(self):
        return RUNNING, STATE, GAMEMODE