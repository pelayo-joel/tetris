import widgets
from const import *
from pygame import gfxdraw


class PlayField(widgets.GridMap):
    def __init__(self, *args, border:bool=False, borderWidth:int=0, borderColor:tuple=(255, 255, 255), **kwargs):
        super().__init__(*args, **kwargs)
        
        self.border = borderWidth
        offset = borderWidth - 2
        self.rect = pygame.Rect(self.left - offset, self.top - offset, self.gridSurf.get_width() + (offset * 2), self.gridSurf.get_height() + (offset * 2))
        if border:
            pygame.draw.rect(self.frame, borderColor, self.rect, borderWidth)
        
        self.__stackGroup = pygame.sprite.Group()
        self.stack = [[None] * self.nColumns for i in range(self.nRows)]

        self.__score = {"Single":100, "Double":300, "Triple":700, "Tetris":1200}
        self.__currentScore = 0
        self.__clearedLines = 0
        self.__getScoredPoints = 0
        self.__playfieldLvl = 1

        self.multiplierTSpin = 1.0
    

    def FillCell(self, landedTile):
        self.__stackGroup.add(landedTile)
        y, x = max(min(self.nRows, int(landedTile.pos.y)), 0), max(min(self.nColumns, int(landedTile.pos.x)), 0)
        self.stack[y][x] = landedTile

    def DrawStack(self):
        self.__stackGroup.draw(self.gridSurf)

    def ClearStack(self):
        self.__stackGroup.empty()
        self.stack = [[None] * self.nColumns for i in range(self.nRows)]

    def ClearingLines(self):
        for row in range((len(self.stack) - 1), 0, -1):
            comboLines = 0
            for comboRow in range(row, 0, -1):

                if None not in self.stack[comboRow]:
                    comboLines += 1
                    for tile in self.stack[comboRow]:
                        tile.kill()
                    self.stack[comboRow] = [None] * self.nColumns

                elif None in self.stack[comboRow] and comboLines > 0:
                    for upperRow in range(comboRow, 0, -1):
                        for upperTile in range(self.nColumns):

                            if self.stack[upperRow][upperTile] != None:
                                self.stack[upperRow][upperTile].rect.y += comboLines * PLAYFIELD_CELL_SIZE
                                self.stack[upperRow + comboLines][upperTile], self.stack[upperRow][upperTile] = \
                                    self.stack[upperRow][upperTile], self.stack[upperRow + comboLines][upperTile]
                    
                    break

                else:
                    break

            if comboLines > 0:
                self.__getScoredPoints = 0
                scoreKeys = list(self.__score.keys())

                self.__clearedLines += comboLines
                self.__getScoredPoints = self.__score[scoreKeys[comboLines - 1]]

                print(max(min(3.0, self.multiplierTSpin), 1.0))
                self.__currentScore += int(self.__getScoredPoints * max(min(3.0, self.multiplierTSpin), 1.0))
                pygame.mixer.Sound.play(SoundEffects["ClearedLines"][scoreKeys[comboLines - 1]])

                '''if self.__playfieldLvl * 10 <= self.__clearedLines:
                    self.__playfieldLvl += 1'''

                if comboLines > 3:
                    pygame.mixer.Sound.play(SoundEffects["NICE"])

                self.multiplierTSpin = 1.0

    def CheckLoss(self):
        for tile in self.__stackGroup:
            if tile.rect.y < 0:
                self.__playfieldLvl = 1
                self.__currentScore = 0
                LOCK_DELAY = 1.5
                return True

        return False

    def GetScoredPoints(self):
        return None

    def GetFullScore(self):
        return self.__currentScore
    
    def GetPlayfieldLvl(self):
        return self.__playfieldLvl
    
    def PlayfieldLvlUp(self):
        print(self.__playfieldLvl, self.__clearedLines)
        if self.__playfieldLvl * 5 <= self.__clearedLines:
            self.__playfieldLvl += 1

            if self.__playfieldLvl % 10 == 0:
                LOCK_DELAY -= 0.2

            return True
    

        
    













class Tile(pygame.sprite.Sprite):
    def __init__(self, tilePos:pygame.Vector2, sprite:pygame.image, spriteGroup:pygame.sprite.Group, playfield:PlayField):
        pygame.sprite.Sprite.__init__(self, spriteGroup)
        self.pos = tilePos + SPAWN_POS
        self.image = sprite
        self.playfield = playfield
        self.rect = self.image.get_rect(topleft=self.pos * PLAYFIELD_CELL_SIZE)
        


    def TileUpdate(self):
        self.rect.topleft = self.pos * PLAYFIELD_CELL_SIZE

    def TileRotation(self, pivot:pygame.Vector2, clockOrientation:str):
        degree = 90
        if clockOrientation == "CounterClockwise":
            degree = -90

        origin = self.pos - pivot
        rotated = origin.rotate(degree)
        return rotated + pivot
    
    '''def TileDrop(self):
        while not self.TileCollision(self.pos):
            self.pos += DIRECTIONS["down"]'''
    
    def TileCollision(self, posToCheck):
        posX, posY = posToCheck.x * PLAYFIELD_CELL_SIZE, posToCheck.y * PLAYFIELD_CELL_SIZE
        if 0 <= posX < PLAYFIELD_W and posY < PLAYFIELD_H and (self.playfield.stack[int(posToCheck.y)][int(posToCheck.x)] is None or (posX, posY) != self.playfield.stack[int(posToCheck.y)][int(posToCheck.x)].rect.topleft):
            return False
        return True





class Tetromino:
    def __init__(self, parent:PlayField):
        self.playfield = parent
        self.shape = random.choice(list(Tetrominoes.keys()))
        self.tileSprite = pygame.image.load(f"{TILE_PATH}Block{self.shape}.png").convert_alpha()
        self.__tileSpriteGroup = pygame.sprite.Group()
        self.__tiles = self.__Tetromino()
        self.__touchedGround = False
        self.__landed = False
        self.__dropping = False
        self.__lockDelay = 1000
        
        self.rStateSelector = 0
        self.rOrientation = RotationState[self.rStateSelector]
        self.wallKicked = False
        self.spinComboLap = 0



    """Private methods"""

    #Creates the tetromino itself
    def __Tetromino(self):
        TetrominoShape = []
        self.tileSprite = pygame.transform.smoothscale(self.tileSprite, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE))
        
        for pos in Tetrominoes[self.shape]:
            TetrominoShape.append(Tile(pos, self.tileSprite, self.__tileSpriteGroup, self.playfield))
        
        return TetrominoShape
    
    #Kicks the tetromino if basic rotation is invalid according to SRS standard
    def __WallKickTesting(self, orientation:str):
        kickSet = "CommonKick"
        if self.shape == "I":
            kickSet = "IKick"

        if orientation == "Clockwise":
            for kick in WallKickData[kickSet][RotationState[(self.rStateSelector + 1) % len(RotationState)]]:
                testKick = [self.__tiles[0].pos + kick]
                for i in range                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      (1, 4):
                    testKick.append(self.__tiles[i].TileRotation(self.__tiles[0].pos, orientation) + kick)
                
                if not self.__Colliding(testKick):
                    pygame.mixer.Sound.play(SoundEffects["Rotate"])
                    self.TetrominoUpdate(testKick)
                    self.wallKicked = True
                    if self.wallKicked:
                        self.playfield.multiplierTSpin += 0.5

                    break

        elif orientation == "CounterClockwise":
            for kick in WallKickData[kickSet][RotationState[(self.rStateSelector - 1) % len(RotationState)]]:
                testKick = [self.__tiles[0].pos - kick]
                for i in range(1, 4):
                    testKick.append(self.__tiles[i].TileRotation(self.__tiles[0].pos, orientation) - kick)
                
                if not self.__Colliding(testKick):
                    pygame.mixer.Sound.play(SoundEffects["Rotate"])
                    self.TetrominoUpdate(testKick)
                    self.wallKicked = True
                    if self.wallKicked:
                        self.playfield.multiplierTSpin += 0.5

                    break

    """def __LockDelay(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.__landed = True
                pygame.mixer.Sound.play(SoundEffects["Landed"])"""
            

    #Defines the Tetromino movement
    def __Move(self, direction:pygame.Vector2):
        nextPos = []
        for tile in self.__tiles:
            nextPos.append(tile.pos + direction)

        if not self.__Colliding(nextPos):
            self.TetrominoUpdate(nextPos)
        elif direction == DIRECTIONS['down']:
            self.__touchedGround = True
            self.playfield.GridUpdate()
            self.__tileSpriteGroup.update()
            self.__tileSpriteGroup.draw(self.playfield.gridSurf)
            #pygame.mixer.Sound.play(SoundEffects["Landed"])

            """timeEvent = pygame.USEREVENT + 1
            pygame.time.set_timer(timeEvent, (LOCK_DELAY * 1000))
            print(timeEvent, LOCK_DELAY, pygame.event.get())
            for event in pygame.event.get():
                if event.type == timeEvent:
                    self.__landed = True
                    pygame.mixer.Sound.play(SoundEffects["Landed"])"""
            #self.__LockDelay()

    #Rotates the tetromino in clockwise or counterclockwise rotation
    def __Rotate(self, clockOrientation):
        nextPos = []
        for tile in self.__tiles:
            nextPos.append(tile.TileRotation(self.__tiles[0].pos, clockOrientation))

        if not self.__Colliding(nextPos):
            pygame.mixer.Sound.play(SoundEffects["Rotate"])
            self.TetrominoUpdate(nextPos)
            self.wallKicked = False
            self.playfield.multiplierTSpin = 1.0
            
            if clockOrientation == "Clockwise":
                self.rStateSelector += 1
            elif clockOrientation == "CounterClockwise":
                self.rStateSelector -= 1

        elif clockOrientation == "Clockwise":
            self.__WallKickTesting(clockOrientation)

        elif clockOrientation == "CounterClockwise":
            self.__WallKickTesting(clockOrientation)
            
        self.rOrientation = RotationState[(self.rStateSelector % len(RotationState))]
        print(self.playfield.multiplierTSpin)

    def __Drop(self):
        self.__lockDelay = 0
        self.__dropping = True
        print(self.__lockDelay)
        while not self.__touchedGround:
            self.__Move(DIRECTIONS["down"])
            self.playfield.DrawStack()

        #pygame.mixer.Sound.play(SoundEffects["Drop"])
    

    #Checks if pos is colliding
    def __Colliding(self, posToCheck):
        return any(map(Tile.TileCollision, self.__tiles, posToCheck))
    
    def __IsStuck(self):
        leftCollide = []
        rightCollide = []

        for tile in self.__tiles:
            leftCollide.append(tile.pos + DIRECTIONS["left"])
            rightCollide.append(tile.pos + DIRECTIONS["right"])


        if self.__Colliding(leftCollide) and self.__Colliding(rightCollide):
            return True
        
        return False
    

    
    """Public methods"""
    

    def TetrominoUpdate(self, newTile):
        for i in range(4):
            self.__tiles[i].pos = newTile[i]
            self.__tiles[i].TileUpdate()
        self.playfield.GridUpdate()
        self.__tileSpriteGroup.update()
        self.__tileSpriteGroup.draw(self.playfield.gridSurf)

    def TetrominoFall(self):
        self.__Move(DIRECTIONS["down"])
        self.spinComboLap += 1

        if self.spinComboLap == 2:
            self.spinComboLap = 0
            self.wallKicked = False
            self.playfield.multiplierTSpin = 1.0

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            pygame.mixer.Sound.play(SoundEffects["Move"])

    def RerollShape(self, bag, current):
        while bag.count(self.shape) >= 2 or self.shape == current:
            self.shape = random.choice(list(Tetrominoes.keys()))
        self.tileSprite = pygame.image.load(f"{TILE_PATH}Block{self.shape}.png").convert_alpha()
        self.__tileSpriteGroup = pygame.sprite.Group()
        self.__tiles = self.__Tetromino()

    def AddToStack(self):
        for tile in self.__tiles:
            self.playfield.FillCell(tile)

    def TetroControls(self, key):
        if key == pygame.K_q and self.shape != "O" and not self.__landed:
            self.__Rotate("CounterClockwise")
        if key == pygame.K_w and self.shape != "O" and not self.__landed:
            self.__Rotate("Clockwise")
        if key == pygame.K_LEFT and not self.__landed:
            self.__Move(DIRECTIONS["left"])
            pygame.mixer.Sound.play(SoundEffects["Move"])
        if key == pygame.K_RIGHT and not self.__landed:
            self.__Move(DIRECTIONS["right"])
            pygame.mixer.Sound.play(SoundEffects["Move"])
        if key == pygame.K_UP:
            self.__Drop()

    def get_TouchedGround(self):
        return self.__touchedGround

    def Landed(self, currentTime=0):
        if self.__touchedGround:
            delay = currentTime + (LOCK_DELAY * self.__lockDelay)

            touchingGround = []
            for tile in self.__tiles:
                touchingGround.append(tile.pos + DIRECTIONS["down"])
            

            if self.__dropping:
                delay = pygame.time.get_ticks()


            if pygame.time.get_ticks() >= delay or self.__IsStuck():
                pygame.mixer.Sound.play(SoundEffects["Landed"])
                self.__landed = True
                self.__touchedGround = False
                self.__lockDelay = 1000
                self.__dropping = False

            elif not self.__Colliding(touchingGround):
                self.__touchedGround = False
        
        return self.__landed

    def Hold(self, holdedTetro):
        if holdedTetro == None:
            return self
        else:
            translation = self.__tiles[0].pos - holdedTetro.__tiles[0].pos

            for tile in holdedTetro.__tiles:
                tile.pos += translation

            while holdedTetro.rOrientation != "0":
                holdedTetro.__Rotate("Clockwise")

            return holdedTetro






class InGame_UI:
    def __init__(self, frame:pygame.Surface, playfieldToMonitor:PlayField):
        self.frame = frame
        self.playfield = playfieldToMonitor
        self.panelsWidth = 150
        self.panelsHeightMax = self.playfield.rect.height

        sidePanelImage = pygame.image.load(f"{IMAGE_PATH}GameField-UI_cropped(2).png")
        holdWindowBorderImage = pygame.image.load(f"{IMAGE_PATH}GameField-UI_hold(2).png")

        self.__sidePanel = widgets.Frame(self.frame, (self.panelsWidth, self.panelsHeightMax), pos=(self.playfield.left + self.playfield.gridSurf.get_width(), self.playfield.top - self.playfield.border + 2), surfImage=sidePanelImage)
        #self.__scoreWindow = widgets.Frame(self.__sidePanel, (self.width - 10, self.height / 2), (0, self.height / 2), color=(10, 10, 10))
        self.__holdWindowBorder = widgets.Frame(self.frame, (self.panelsWidth, self.panelsHeightMax / 4), pos=(self.playfield.left - self.panelsWidth, self.playfield.top - self.playfield.border + 2), surfImage=holdWindowBorderImage)
        self.holdWindowEraser = pygame.Surface((PLAYFIELD_CELL_SIZE * 2.5, PLAYFIELD_CELL_SIZE * 3.5))
        self.__scoreSurface = widgets.Frame(self.__sidePanel.surfImage, (self.panelsWidth - (self.playfield.border * 3), self.panelsHeightMax /2), pos=(self.playfield.border, self.playfield.border * 3), color=(1, 1, 1))
        
        self.holdLabel = widgets.TextLabel(self.__holdWindowBorder.surfImage, "Hold", 17, FONT_PATH, color=(1, 1, 1), pourcentMode=True, posX=33, posY=8)
        self.sidePanelLabel = widgets.TextLabel(self.__sidePanel.surfImage, "Status", 17, FONT_PATH, color=(1, 1, 1), pourcentMode=True, centerX=True, posY=2)
        self.scoreLabel = widgets.TextLabel(self.__scoreSurface, f"Score: ", 17, FONT_PATH, color=(255, 255, 255), pourcentMode=True, posX=38, posY=24)
        self.score = widgets.TextLabel(self.__scoreSurface, f"{self.playfield.GetFullScore()}", 17, FONT_PATH, color=(255, 255, 255), pourcentMode=True, centerX=True, posY=32)
        self.lvlLabel = widgets.TextLabel(self.__scoreSurface, f"Lvl: {self.playfield.GetPlayfieldLvl()}", 25, FONT_PATH, color=(255, 255, 255), pourcentMode=True, posX=39, posY=8)
        
        #pygame.draw.rect(self, (100, 100, 180), pygame.Rect(0, 0, self.width - 10, self.height - 10), 3)
        #self.__holdWindow = PlayField(self.parent, (PLAYFIELD_CELL_SIZE - 10, PLAYFIELD_CELL_SIZE - 10), self.playfield.left - (self.width - 6), self.playfield.top + 20, 6, 6)
        #self.__nextWindow
        #self.__pauseWindow

    def UpdateUI(self):
        #self.__holdWindowBorder.surfImage = pygame.transform.smoothscale(self.__holdWindowBorder.surfImage, (self.__holdWindowBorder.width, self.playfield.gridSurf.height + self.playfield.border + 1))

        self.__holdWindowBorder.ActiveFrame()

        self.__sidePanel.ActiveFrame()
        self.__scoreSurface.ActiveFrame()
        self.__sidePanel.surfImage.blit(self.__scoreSurface, (self.playfield.border, self.playfield.border * 3))
        #self.__scoreWindow.ActiveFrame(image=pygame.image.load(f"{IMAGE_PATH}GameField-UI_score.png"))
        
        #self.label.textFrame.ActiveFrame()
        #pygame.display.flip()

    def UpdateHoldWindow(self, shape):
        if shape != None:
            holdImage = pygame.image.load(f"{TILE_PATH}{shape}-Shape.png")
            holdImage = pygame.transform.smoothscale(holdImage, (PLAYFIELD_CELL_SIZE * 2.5, PLAYFIELD_CELL_SIZE * 3.5))
            self.holdWindowEraser.fill((0, 0, 0))
            self.__holdWindowBorder.surfImage.blit(self.holdWindowEraser, ((self.__holdWindowBorder.width / 2 - (holdImage.get_width() / 2)), (self.__holdWindowBorder.height / 2 - (holdImage.get_height() / 2) + 10)))
            self.__holdWindowBorder.surfImage.blit(holdImage, ((self.__holdWindowBorder.width / 2 - (holdImage.get_width() / 2)), (self.__holdWindowBorder.height / 2 - (holdImage.get_height() / 2) + 10)))

    def UpdateStatusWindow(self):
        print(self.playfield.GetFullScore())
        #{self.playfield.GetFullScore()}
        self.score.NewText(f"{self.playfield.GetFullScore()}")
        self.lvlLabel.NewText(f"Lvl: {self.playfield.GetPlayfieldLvl()}")