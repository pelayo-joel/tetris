import json
import hashlib
from const import *
from tetrisObj import *



class ScoreManager:
    def __init__(self, scene):
        with open("Scores.json") as playersScoreData:
            self.__scoresData = json.load(playersScoreData)
        
        self.scene = scene
        self.centerX, self.centerY = self.scene.width / 2, self.scene.height / 2
        window = pygame.image.load(f"{UI_PATH}GameField-UI_PauseWindow.png")
        self.__focusedButton = pygame.image.load(f"{UI_PATH}Button2(focused).png")
        self.__modeFocused = pygame.image.load(f"{UI_PATH}Button1(focused).png")

        self.__playerList = list(self.__scoresData.keys())
        self.currentPlayer = ""
        self.__passLab = ""
        self.__password = ""
        self.__playerScores = None


        self.__loginWindow = widgets.Frame(self.scene, (450, 350), (self.centerX - 200, self.centerY - 175), color=(1, 1, 1), surfImage=window)

        self.__playerLabel = widgets.TextLabel(self.__loginWindow, "Name: ", 16, FONT_PATH, pourcentMode=True, posX=25, posY=29, bgColor=(1, 1, 1))
        self.__passwordLabel = widgets.TextLabel(self.__loginWindow, "Password: ", 16, FONT_PATH, pourcentMode=True, posX=25, posY=42, bgColor=(1, 1, 1))
        self.__loginAdd = widgets.GfxButton(self.__loginWindow, 190, 40, pourcentMode=True, centerX=True, posY=67, type="OnClick", buttonLabel="Add player", labelSize=14, imageButton=f"{UI_PATH}Button2.png", func=self.__NewPlayer)
        self.__loginStart = widgets.GfxButton(self.__loginWindow, 190, 40, pourcentMode=True, centerX=True, posY=82, type="OnClick", buttonLabel="Login", labelSize=14, imageButton=f"{UI_PATH}Button2.png", func=self.__Login)
        self.__loginMessage = widgets.TextLabel(self.__loginWindow, "", 14, FONT_PATH, pourcentMode=True, centerX=True, posY=53, bgColor=(0, 0, 0))
        
        self.__nameInput = widgets.TextLabel(self.__loginWindow, self.currentPlayer, 16, FONT_PATH, pourcentMode=True, posX=65, posY=29, bgColor=(0, 0, 0))
        self.__passInput = widgets.TextLabel(self.__loginWindow, self.__passLab, 35, FONT_PATH, pourcentMode=True, posX=65, posY=42, bgColor=(0, 0, 0))
    
        self.__loginEntries = [self.__nameInput, self.__passInput]
        self.__loginSelection = [self.__playerLabel, self.__passwordLabel, self.__loginAdd, self.__loginStart]
        self.__loginEntrySelector = 0
        self.__loginValidation = False


        self.__scoreBoardWindow = widgets.Frame(self.scene, (600, 400), (self.centerX - 300, self.centerY - 175), color=(1, 1, 1), surfImage=window)

        self.__scoreBoardClassic = widgets.GfxButton(self.scene, 160, 40, pourcentMode=True, posX=13, posY=15, type="OnClick", buttonLabel="Classic", labelSize=14, imageButton=f"{UI_PATH}Button1.png")
        self.__scoreBoardMarathon = widgets.GfxButton(self.scene, 160, 40, pourcentMode=True, posX=37, posY=15, type="OnClick", buttonLabel="Marathon", labelSize=14, imageButton=f"{UI_PATH}Button1.png")
        self.__scoreBoardRush = widgets.GfxButton(self.scene, 160, 40, pourcentMode=True, posX=62, posY=15, type="OnClick", buttonLabel="100-Lines Rush", labelSize=14, imageButton=f"{UI_PATH}Button1.png")
        self.__scoreBoardSurvival = widgets.GfxButton(self.scene, 160, 40, pourcentMode=True, posX=87, posY=15, type="OnClick", buttonLabel="Survival", labelSize=14, imageButton=f"{UI_PATH}Button1.png")
        self.__scoreWindowLabel = widgets.TextLabel(self.__scoreBoardWindow, "Classic", 20, FONT_PATH, pourcentMode=True, centerX=True, posY=8, color=(0, 0, 0), bgColor=(86, 222, 187))

        self.__scoreModeSelection = [self.__scoreBoardClassic, self.__scoreBoardMarathon, self.__scoreBoardRush, self.__scoreBoardSurvival]
        self.__scoreMode = ["Classic", "Marathon", "100-Lines Rush", "Survival"]
        self.__scoreSelector = 0

        self.__forbiddenKeys = [pygame.K_CAPSLOCK, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_TAB, pygame.K_ESCAPE, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_MODE, pygame.K_LEFT, pygame.K_RIGHT, \
                                pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]





    def DefineCurrentPlayer(self):
        global RUNNING, STATE

        self.__loginWindow.ActiveFrame()
        widgets.TextLabel(self.__loginWindow, "Login", 20, FONT_PATH, pourcentMode=True, centerX=True, posY=8, color=(0, 0, 0), bgColor=(1, 1, 1))


        for i in range(len(self.__loginSelection)):
            if isinstance(self.__loginSelection[i], widgets.GfxButton):
                self.__loginSelection[i].ActiveButton()

                if i == self.__loginEntrySelector:
                    self.__loginSelection[i].ActiveButton(focused=True, focusedImage=self.__focusedButton)

            else:
                self.__loginSelection[i].NewText(self.__loginSelection[i].text, color=(255, 255, 255))

                if i == self.__loginEntrySelector:
                    self.__loginSelection[i].NewText(self.__loginSelection[i].text, color=(95, 250, 195))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                STATE = None


            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_BACKSPACE:
                    pygame.mixer.Sound.play(SoundEffects["Key"])

                    if self.__loginEntrySelector != 1:
                        self.currentPlayer = self.currentPlayer[:-1]
                        self.__nameInput.NewText(self.currentPlayer)

                    else:
                        self.__password = self.__password[:-1]
                        self.__passLab = self.__passLab[:-1]
                        self.__passInput.NewText(self.__passLab)

                elif event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(SoundEffects["Select"])
                    self.__loginEntrySelector -= 1

                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(SoundEffects["Select"])
                    self.__loginEntrySelector += 1

                elif event.key == pygame.K_RETURN:
                    if isinstance(self.__loginSelection[self.__loginEntrySelector], widgets.GfxButton):
                        self.__loginSelection[self.__loginEntrySelector].Click(input=True)

                    else:
                        self.__loginStart.Click(input=True)

                    return self.__loginValidation
                    
                elif self.__loginEntrySelector < 2 and (event.key not in self.__forbiddenKeys and event.key != pygame.K_RETURN and event.key != pygame.K_DOWN and event.key != pygame.K_UP):
                    pygame.mixer.Sound.play(SoundEffects["Key"])
                    if self.__loginEntrySelector != 1 and len(self.currentPlayer) < 10:
                        self.currentPlayer += event.unicode
                        self.__nameInput.NewText(self.currentPlayer)

                    elif self.__loginEntrySelector == 1 and len(self.__passLab) < 15:
                        self.__password += event.unicode
                        self.__passLab += "*"
                        self.__passInput.NewText(self.__passLab)


        self.__loginEntrySelector = max(min(self.__loginEntrySelector, 3), 0)



    def ScoreBoard(self):
        global RUNNING, STATE
        self.__scoreBoardWindow.ActiveFrame()
        widgets.TextLabel(self.scene, "ScoreBoard", 22, FONT_PATH, pourcentMode=True, centerX=True, posY=6, color=(255, 255, 255), bgColor=(1, 1, 1))
        self.__ScoreBoardData(self.__scoreMode[self.__scoreSelector])


        for i in range(len(self.__loginSelection)):
            self.__scoreModeSelection[i].ActiveButton()
            self.__scoreWindowLabel.NewText(self.__scoreMode[self.__scoreSelector])

            if i == self.__scoreSelector:
                self.__scoreModeSelection[i].ActiveButton(focused=True, focusedImage=self.__modeFocused)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                STATE = None


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.play(SoundEffects["Select"])
                    self.__scoreBoardWindow.blit(self.__scoreBoardWindow.surfImage, (0, 0))
                    self.__scoreSelector -= 1

                elif event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.play(SoundEffects["Select"])
                    self.__scoreBoardWindow.blit(self.__scoreBoardWindow.surfImage, (0, 0))
                    self.__scoreSelector += 1

                elif event.key == pygame.K_RETURN:
                    return None

                elif event.key == pygame.K_BACKSPACE:
                    self.__scoreSelector = 0
                    pygame.mixer.Sound.play(SoundEffects["Return"])
                    self.__scoreBoardWindow.blit(self.__scoreBoardWindow.surfImage, (0, 0))
                    return False

        self.__scoreSelector = max(min(self.__scoreSelector, 3), 0)
        return True



    def UserClear(self):
        self.currentPlayer = ""
        self.__passLab = ""
        self.__password = ""
        self.__loginValidation = False
        self.__playerScores = None

        self.entriesData = [self.currentPlayer, self.__password]


        for i in range(len(self.__loginEntries)):
            self.__loginEntries[i].NewText(self.entriesData[i])

        self.__loginMessage.NewText("", color=(255, 255, 255))
        self.__loginEntrySelector = 0



    def SaveScore(self, mode, newLines, newTime, newScore):
        hours, minutes, sec = newTime.split(":")
        timeScore = (int(hours) * 3600) + (int(minutes) * 60) + int(sec)


        if mode != "Marathon":

            if newScore >= self.__playerScores[mode]["Score"]:
                self.__playerScores[mode]["Score"] = newScore
                self.__playerScores[mode]["Lines Cleared"] = newLines
                self.__playerScores[mode]["Time"] = timeScore
        
        elif mode == "100-Lines Rush":

            if newLines - 70 >= self.__playerScores[mode]["Lines Cleared"] and timeScore < self.__playerScores[mode]["Time"]:
                self.__playerScores[mode]["Score"] = newScore
                self.__playerScores[mode]["Lines Cleared"] = newLines - 70
                self.__playerScores[mode]["Time"] = timeScore

        else:

            if newScore >= self.__playerScores[mode]["Score"]:
                self.__playerScores[mode]["Score"] = newScore
                self.__playerScores[mode]["Lines Cleared"] = newLines - 120

        self.__scoresData[self.currentPlayer].update(self.__playerScores)
        self.__UpdateJSON()
        


    def GetPlayerScores(self):
        return self.__playerScores





    def __NewPlayer(self):
        formatName = self.currentPlayer.lower()


        if self.__password == "":
            self.__loginMessage.NewText("Please enter a password", color=(160, 50, 50))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None
        
        elif " " in self.currentPlayer or self.currentPlayer == "":
            self.__loginMessage.NewText("Invalid username", color=(160, 50, 50))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None
        
        elif formatName in self.__playerList:
            self.__loginMessage.NewText("We already know you", color=(255, 255, 255))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None
        

        password = hashlib.sha256(self.__password.encode()).hexdigest()

        self.__scoresData.update({formatName:{
            "Classic":{
                "Score":0, 
                "Time":0, 
                "Lines Cleared":0
            },
            "Marathon":{
                "Score":0,
                "Lines Cleared":0
            },
            "100-Lines Rush":{
                "Score":0,
                "Lines Cleared": 0,
                "Time":0
            },
            "Survival":{
                "Score":0,
                "Time":0,
                "Lines Cleared":0
            },
            "Password":password
        }})

        self.__UpdateJSON()
        self.__playerList = list(self.__scoresData.keys())

        self.__loginMessage.NewText("You've been added, now log in !", color=(20, 130, 20))
        pygame.mixer.Sound.play(SoundEffects["Confirm"])

    

    def __Login(self):
        if self.__password == "":
            self.__loginMessage.NewText("Please enter a password", color=(160, 50, 50))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None

        password = hashlib.sha256(self.__password.encode()).hexdigest()
        formatName = self.currentPlayer.lower()

        if formatName not in self.__playerList:
            self.__loginMessage.NewText("New user ? Add yourself !", color=(255, 255, 255))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None
        
        elif formatName in self.__playerList and password != self.__scoresData[formatName]["Password"]:
            self.__loginMessage.NewText("Wrong password", color=(130, 20, 20))
            pygame.mixer.Sound.play(SoundEffects["Message"])
            return None
        
        else:
            self.__playerScores = self.__scoresData[formatName]
            pygame.mixer.Sound.play(SoundEffects["Confirm"])
            self.__loginValidation = True



    def __UpdateJSON(self):
        with open("Scores.json", "w") as playersScoreData:
            json.dump(self.__scoresData, playersScoreData, indent=4, separators=(",",": "))



    def __ConvertTimeScore(self, time:int):
        minutes, timeScore = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)

        return "%d:%02d:%02d" % (hours, minutes, timeScore)



    def __SortingScoreData(self, mode:str):
        if mode == "100-Lines Rush":
            sortedScores = sorted(self.__scoresData, key=lambda x: (-self.__scoresData[x][mode]["Lines Cleared"], self.__scoresData[x][mode]["Time"]))

        else:
            sortedScores = sorted(self.__scoresData, key=lambda x: self.__scoresData[x][mode]["Score"], reverse=True)


        return sortedScores



    def __ScoreBoardData(self, scoreMode:str):
        self.__scoreBoardWindow.ActiveFrame()
        rankColumn, nameColumn = 10, 27
        labelRow = 30
        scoreColumn = [45, 65, 85]
        rankRows = [45, 60, 75]
        labels = ["Score", "Lines", "Time"]
        
        sortedNames = self.__SortingScoreData(scoreMode)

        widgets.TextLabel(self.__scoreBoardWindow, "no.", 18, FONT_PATH, pourcentMode=True, posX=rankColumn, posY=labelRow, color=(255, 255, 255), bgColor=(1, 1, 1))
        widgets.TextLabel(self.__scoreBoardWindow, "Name", 15, FONT_PATH, pourcentMode=True, posX=nameColumn, posY=labelRow, color=(255, 255, 255), bgColor=(1, 1, 1))


        for i in range(3):
            widgets.TextLabel(self.__scoreBoardWindow, labels[i], 13, FONT_PATH, pourcentMode=True, posX=scoreColumn[i], posY=labelRow, color=(255, 255, 255), bgColor=(0, 0, 0))
            widgets.TextLabel(self.__scoreBoardWindow, sortedNames[i], 15, FONT_PATH, pourcentMode=True, posX=nameColumn, posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))
            widgets.TextLabel(self.__scoreBoardWindow, "---", 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[2], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))            
            
            
            if self.__scoresData[sortedNames[i]][scoreMode]["Score"] == 0 and self.__scoresData[sortedNames[i]][scoreMode]["Score"] == 0 and self.__scoresData[sortedNames[i]][scoreMode]["Score"] == 0:
                widgets.TextLabel(self.__scoreBoardWindow, "---", 22, FONT_PATH, pourcentMode=True, posX=rankColumn, posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))

            else:
                widgets.TextLabel(self.__scoreBoardWindow, str(i + 1), 22, FONT_PATH, pourcentMode=True, posX=rankColumn, posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))


            if self.currentPlayer == sortedNames[i]:
                widgets.TextLabel(self.__scoreBoardWindow, sortedNames[i], 15, FONT_PATH, pourcentMode=True, posX=nameColumn, posY=rankRows[i], color=(86, 222, 187), bgColor=(0, 0, 0))


            if scoreMode != "Marathon":
                widgets.TextLabel(self.__scoreBoardWindow, self.__ConvertTimeScore(self.__scoresData[sortedNames[i]][scoreMode]["Time"]), 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[2], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))


            if scoreMode == "100-Lines Rush":
                widgets.TextLabel(self.__scoreBoardWindow, "---", 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[0], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))
                rushLinesLab = widgets.TextLabel(self.__scoreBoardWindow, str(self.__scoresData[sortedNames[i]][scoreMode]["Lines Cleared"]), 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[1], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))
            
                if self.__scoresData[sortedNames[i]][scoreMode]['Lines Cleared'] == 100:
                    rushLinesLab.NewText(f"{self.__scoresData[sortedNames[i]][scoreMode]['Lines Cleared']}", color=(235, 175, 30))

            else:
                widgets.TextLabel(self.__scoreBoardWindow, str(self.__scoresData[sortedNames[i]][scoreMode]["Score"]), 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[0], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))
                widgets.TextLabel(self.__scoreBoardWindow, str(self.__scoresData[sortedNames[i]][scoreMode]["Lines Cleared"]), 15, FONT_PATH, pourcentMode=True, posX=scoreColumn[1], posY=rankRows[i], color=(255, 255, 255), bgColor=(0, 0, 0))


        pygame.display.update()






    






class Game:
    def __init__(self, scene:pygame.Surface, mode:str, scoreManager:ScoreManager):
        global CLOCK, TIME_INTERVAL
        self.scene = scene
        self.scoreManager = scoreManager
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

        elif self.__mode == "100-Lines Rush":
            TIME_INTERVAL -= 375
            pygame.mixer.music.load(InGameMusic["PlayField"])
            pygame.mixer.music.set_volume(0.2)

        else:
            TIME_INTERVAL = 1000
            pygame.mixer.music.load(InGameMusic["PlayField"])
            pygame.mixer.music.set_volume(0.2)

        pygame.mixer.music.play(-1)






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
        

        #print(self.playfield.addFlag)
        if self.__mode == "Survival" and self.playfield.addFlag:
            self.tetromino.TetrominoUp(self.playfield.GetAddedLines())
            self.playfield.addFlag = False


        self.GameUI.UpdateStatusWindow(self.scoreManager.GetPlayerScores())
        self.playfield.DrawStack()


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
                    self.__Clear()
                else:
                    #self.tetromino.TetroKill()
                    self.playfield.DrawStack()
                    self.__GameOver()

            self.__NewTetromino()

        elif self.__mode == "Marathon" and self.playfield.sec == 61:
            self.tetromino.TetroKill()
            self.playfield.DrawStack()
            self.__GameOver()

        elif self.__mode == "100-Lines Rush" and (170 - self.playfield.GetClearedLines()) <= 0:
            #self.tetromino.TetroKill()
            self.playfield.DrawStack()
            self.__GameOver()
        
        self.scene.ActiveFrame()
        pygame.display.update()



    def Restart(self):
        return self.__restart



    def GetStates(self):
        return RUNNING, STATE, MENUSTATE
    




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
        self.GameUI.UpdateStatusWindow(self.scoreManager.GetPlayerScores())
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
        global CLOCK, RUNNING, STATE
        pauseStart = pygame.time.get_ticks()
        pause = True

        self.GameUI.pauseArrowNav[0].Command(self.__ChangeGameState)
        self.GameUI.pauseArrowNav[1].Command(self.__Clear)

        while pause:

            pauseTimer = int(pygame.time.get_ticks() - pauseStart)


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False
                    STATE = None
                    pause = False


                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        pygame.mixer.music.unpause()
                        pygame.mixer.Sound.play(SoundEffects["Pause"])
                        self.playfield.start += pauseTimer
                        CLOCK = pygame.time.get_ticks()
                        pause = False


                    if event.key == pygame.K_UP:
                        self.GameUI.pauseSelector -= 1
                        self.GameUI.pauseSelector = (self.GameUI.pauseSelector % len(self.GameUI.pauseArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])


                    if event.key == pygame.K_DOWN:
                        self.GameUI.pauseSelector += 1
                        self.GameUI.pauseSelector = (self.GameUI.pauseSelector % len(self.GameUI.pauseArrowNav))
                        pygame.mixer.Sound.play(SoundEffects["Select"])


                    if event.key == pygame.K_RETURN:
                        pause = False
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

        self.scoreManager.SaveScore(self.__mode, self.playfield.GetClearedLines(), timeSpent, self.playfield.GetFullScore())

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


            self.GameUI.GameOverScreen(timeSpent, self.scoreManager.GetPlayerScores())
            self.scene.ActiveFrame()
            pygame.display.update()



    def __InGameControls(self, event):

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
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SoundEffects["Pause"])
                self.__GamePause()

            if event.key == pygame.K_BACKSPACE and self.__mode == "Training":
                self.__Clear()


        if keys[pygame.K_DOWN] and not self.tetromino.get_TouchedGround():
            self.speed = FAST_TIME_INTERVAL

        else:
            self.speed = TIME_INTERVAL














class Menu:
    def __init__(self, scene:pygame.Surface, state:str, score:ScoreManager):
        self.scene = scene
        self.scoreManager = score

        self.mainLogo = pygame.image.load(f"{IMAGE_PATH}Tetris69-Logo.png")
        self.mainLogo = pygame.transform.smoothscale(self.mainLogo, (450, 430))
        self.focusedButton = pygame.image.load(f"{UI_PATH}Button2(focused).png")
        self.focusedButton = pygame.transform.smoothscale(self.focusedButton, (320, 80))


        self.__simultaneousFallingPiece = random.randint(12, 17)
        self.__nStarFall = random.randint(80, 90)
        self.__starSprites = [pygame.image.load(f"{IMAGE_PATH}star1.png"), pygame.image.load(f"{IMAGE_PATH}star2.png")]
        self.__fall = 0

        self.__rndTetroLeftPosition = []
        self.__rndTetroTopPosition = []
        self.__rndTetroSpeed = []
        self.__fallingPieces = []

        self.__rndStarLeftPosition = []
        self.__rndStarTopPosition = []
        self.__rndStarSpeed = []
        self.__fallingStar = []

        self.__RandomGeneration()
        

        self.mainMenuGame = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=55, type="OnClick", buttonLabel="Game Modes", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Game Modes"))
        self.mainMenuScore = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=70, type="OnClick", buttonLabel="Score Board", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Score Board"))
        self.mainMenuCredits = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=85, type="OnClick", buttonLabel="Credits", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeMenuState("Credits"))

        self.gameMenuTraining = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=20, type="OnClick", buttonLabel="Training", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Training"))
        self.gameMenuClassic = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=35, type="OnClick", buttonLabel="Classic", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Classic"))
        self.gameMenuMarathon = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=50, type="OnClick", buttonLabel="Marathon", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Marathon"))
        self.gameMenuRush = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=65, type="OnClick", buttonLabel="100-Lines Rush", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("100-Lines Rush"))
        self.gameMenuSurvival = widgets.GfxButton(self.scene, 320, 80, pourcentMode=True, centerX=True, posY=80, type="OnClick", buttonLabel="Survival", imageButton=f"{UI_PATH}Button2.png", func=lambda:self.__ChangeGameState("Survival"))


        self.menuState = state
        self.mainMenuArrowNav = [self.mainMenuGame, self.mainMenuScore, self.mainMenuCredits]
        self.gameMenuArrowNav = [self.gameMenuTraining, self.gameMenuClassic, self.gameMenuMarathon, self.gameMenuRush, self.gameMenuSurvival]
        self.currentMenu = []
        self.arrowSelector = 0
        self.menuDepth = 0

        pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        

        if self.menuState != "Login":
            pygame.mixer.music.load(InGameMusic["Menu"])
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)





    def MenuLoop(self):
        self.scene.ActiveFrame()
        self.__fall += 2

        if self.menuState != "Login":
            self.__BackgroundAnimation()

        
        if self.menuState == "Login":
            self.__LoginMenu()

        elif self.menuState == "Main Menu":
            self.__MainMenu()

        elif self.menuState == "Game Modes":
            self.__GameMenu()

        elif self.menuState == "Score Board":
            self.__ScoreMenu()

        elif self.menuState == "Credits":
            self.__Credits()


        pygame.display.update()



    def GetStates(self):
        return RUNNING, STATE, GAMEMODE
    





    def __BackgroundAnimation(self):
        i, j = 0, 0
        self.scene.blit(self.scene.surfImage, (0, 0))

        while j < self.__nStarFall:
            self.__rndStarTopPosition[j] += self.__rndStarSpeed[j]
            self.__rndStarLeftPosition[j] += random.randint(-1, 1)

            self.scene.blit(self.__fallingStar[j], (self.__rndStarLeftPosition[j], self.__rndStarTopPosition[j]))
            

            if self.__rndStarTopPosition[j] >= 720:
                self.__RandomStarDataGeneration(j)

            
            if i < self.__simultaneousFallingPiece:
                self.__rndTetroTopPosition[i] += self.__rndTetroSpeed[i]
                self.scene.blit(self.__fallingPieces[i], (self.__rndTetroLeftPosition[i], self.__rndTetroTopPosition[i]))

                rndOneActiveRotation = random.randint(100, 600)
                rndTwoActiveRotation = random.randint(100, 600)
                #rndThreeActiveRotation = random.randint(100, 600)

                if self.__rndTetroTopPosition[i] == rndOneActiveRotation or self.__rndTetroTopPosition[i] == rndTwoActiveRotation:
                    self.__fallingPieces[i] = pygame.transform.rotate(self.__fallingPieces[i], random.choice([90, 270]))
            

                if self.__rndTetroTopPosition[i] >= 720:
                    self.__RandomPieceGeneration(i)

                i += 1


            j += 1



    def __RandomPieceGeneration(self, index):
        pieceShape = random.choice(list(Tetrominoes.keys()))
        self.__fallingPieces[index] = pygame.image.load(f"{TILE_PATH}{pieceShape}-Shape.png")

        rndRotation = random.choice([0, 90, 180, 270])
        rndSide = random.choice([200, 650])
        rndSpeed = random.randint(1, 3)
        rndX = random.randint((rndSide - 200), rndSide)
        rndY = random.randint(-1600, 0)

        rndWidth, rndHeight = random.randint(70, 85), random.randint(90, 115)
        self.__fallingPieces[index] = pygame.transform.smoothscale(self.__fallingPieces[index], (rndWidth, rndHeight))
        self.__fallingPieces[index] = pygame.transform.rotate(self.__fallingPieces[index], rndRotation)

        self.__rndTetroSpeed[index] = rndSpeed
        self.__rndTetroLeftPosition[index] = rndX
        self.__rndTetroTopPosition[index] = rndY



    def __RandomStarDataGeneration(self, index):
        star = random.choice(self.__starSprites)

        rndRotation = random.randint(0, 180)
        rndSpeed = random.randint(3, 5)
        rndX = random.randint(0, DISPLAY_W)
        rndY = random.randint(-1000, 0)

        rndWidth, rndHeight = random.randint(5, 25), random.randint(5, 15)
        star = pygame.transform.smoothscale(star, (rndWidth, rndHeight))
        star = pygame.transform.rotate(star, rndRotation)

        self.__rndStarSpeed[index] = rndSpeed
        self.__rndStarLeftPosition[index] = rndX
        self.__rndStarTopPosition[index] = rndY
        self.__fallingStar[index] = star



    def __RandomGeneration(self):
        i, j = 0, 0

        while j < self.__nStarFall:

            if i < self.__simultaneousFallingPiece:
                pieceShape = random.choice(list(Tetrominoes.keys()))
                piece = pygame.image.load(f"{TILE_PATH}{pieceShape}-Shape.png")

                rndRotation = random.choice([0, 90, 180, 270])
                rndSide = random.choice([200, 650])
                rndSpeed = random.randint(1, 3)
                rndX = random.randint((rndSide - 200), rndSide)
                rndY = random.randint(-1000, 0)

                rndWidth, rndHeight = random.randint(70, 85), random.randint(90, 115)
                piece = pygame.transform.smoothscale(piece, (rndWidth, rndHeight))
                piece = pygame.transform.rotate(piece, rndRotation)

                self.__fallingPieces.append(piece)
                self.__rndTetroLeftPosition.append(rndX)
                self.__rndTetroTopPosition.append(rndY)
                self.__rndTetroSpeed.append(rndSpeed)

                i += 1


            star = random.choice(self.__starSprites)

            rndRotation = random.randint(0, 180)
            rndSpeed = random.randint(3, 5)
            rndX = random.randint(0, DISPLAY_W)
            rndY = random.randint(-1000, 0)

            rndWidth, rndHeight = random.randint(5, 25), random.randint(5, 25)
            star = pygame.transform.smoothscale(star, (rndWidth, rndHeight))
            star = pygame.transform.rotate(star, rndRotation)

            self.__fallingStar.append(star)
            self.__rndStarLeftPosition.append(rndX)
            self.__rndStarTopPosition.append(rndY)
            self.__rndStarSpeed.append(rndSpeed)

            j += 1



    def __ChangeMenuState(self, nextState:str):
        if nextState == "Login":
            self.scoreManager.UserClear()
            pygame.mixer.music.stop()

        self.menuState = nextState
        self.arrowSelector = 0

        self.scene.blit(self.scene.surfImage, (0, 0))
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

                if event.key == pygame.K_ESCAPE:
                    self.scoreManager.UserClear()
                    self.__ChangeMenuState("Login")
                    pygame.mixer.Sound.play(SoundEffects["Return"])
                
                self.arrowSelector = (self.arrowSelector % len(self.currentMenu))



    def __LoginMenu(self):
        if self.scoreManager.DefineCurrentPlayer():
            pygame.mixer.music.load(InGameMusic["Menu"])
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            self.__ChangeMenuState("Main Menu")



    def __MainMenu(self):
        self.scene.blit(self.mainLogo, ((self.scene.parent.get_width() / 2) - (self.mainLogo.get_width() / 2), -50))
        self.currentMenu = self.mainMenuArrowNav

        for mainMenuButton in self.currentMenu:
            mainMenuButton.ActiveButton()

        self.currentMenu[self.arrowSelector].ActiveButton(focused=True, focusedImage=self.focusedButton)
        
        self.__MenuControls()



    def __GameMenu(self):
        self.currentMenu = self.gameMenuArrowNav

        for gameMenuButton in self.currentMenu:
            gameMenuButton.ActiveButton()

        self.currentMenu[self.arrowSelector].ActiveButton(focused=True, focusedImage=self.focusedButton)
        self.__MenuControls()



    def __ScoreMenu(self):
        if not self.scoreManager.ScoreBoard():
            self.__ChangeMenuState("Main Menu")



    def __Credits(self):
        self.__MenuControls()
        #self.__CreditsBackGround() 







