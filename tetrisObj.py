import math
import widgets
from const import *


class PlayField(widgets.GridMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stackGroup = pygame.sprite.Group()
        self.stack = [[None] * self.nColumns for i in range(self.nRows)]

        self.__score = {"Single":100, "Double":300, "Triple":700, "Tetris":1200}
        self.__currentScore = 0
    
    def FillCell(self, landedTile):
        self.__stackGroup.add(landedTile)
        y, x = max(min(self.nRows, int(landedTile.pos.y)), 0), max(min(self.nColumns, int(landedTile.pos.x)), 0)
        print(y, x)
        self.stack[y][x] = landedTile

    def DrawStack(self):
        self.__stackGroup.draw(self.gridSurf)

    def ClearStack(self):
        self.__stackGroup.empty()
        self.stack = [[None] * self.nColumns for i in range(self.nRows)]

    def ClearLines(self):
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
                                self.stack[upperRow + comboLines][upperTile], self.stack[upperRow][upperTile] = self.stack[upperRow][upperTile], self.stack[upperRow + comboLines][upperTile]
                    
                    break

                else:
                    break

            if comboLines > 0:
                scoreKeys = list(self.__score.keys())
                self.__currentScore += self.__score[scoreKeys[comboLines - 1]]
                pygame.mixer.Sound.play(SoundEffects["ClearedLines"][scoreKeys[comboLines - 1]])

                if comboLines > 3:
                    pygame.mixer.Sound.play(SoundEffects["NICE"])

    def CheckLoss(self):
        for tile in self.__stackGroup:
            if tile.rect.y < 0:
                return True

        return False

    def GetScore(self):
        return self.__currentScore

        
    






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
        self.__landed = False
        
        self.rStateSelector = 0
        self.rOrientation = RotationState[self.rStateSelector]



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
                    break

        elif orientation == "CounterClockwise":
            for kick in WallKickData[kickSet][RotationState[(self.rStateSelector - 1) % len(RotationState)]]:
                testKick = [self.__tiles[0].pos - kick]
                for i in range(1, 4):
                    testKick.append(self.__tiles[i].TileRotation(self.__tiles[0].pos, orientation) - kick)
                
                if not self.__Colliding(testKick):
                    pygame.mixer.Sound.play(SoundEffects["Rotate"])
                    self.TetrominoUpdate(testKick)
                    break

    #Defines the Tetromino movement
    def __Move(self, direction:pygame.Vector2):
        nextPos = []
        for tile in self.__tiles:
            nextPos.append(tile.pos + direction)

        if not self.__Colliding(nextPos):
            self.TetrominoUpdate(nextPos)
        elif direction == DIRECTIONS['down']:
            self.__landed = True
            pygame.mixer.Sound.play(SoundEffects["Landed"])

    #Rotates the tetromino in clockwise or counterclockwise rotation
    def __Rotate(self, clockOrientation):
        nextPos = []
        for tile in self.__tiles:
            nextPos.append(tile.TileRotation(self.__tiles[0].pos, clockOrientation))

        if not self.__Colliding(nextPos):
            pygame.mixer.Sound.play(SoundEffects["Rotate"])
            self.TetrominoUpdate(nextPos)
            
            if clockOrientation == "Clockwise":
                self.rStateSelector += 1
            elif clockOrientation == "CounterClockwise":
                self.rStateSelector -= 1

        elif clockOrientation == "Clockwise":
            self.__WallKickTesting(clockOrientation)

        elif clockOrientation == "CounterClockwise":
            self.__WallKickTesting(clockOrientation)
            
        self.rOrientation = RotationState[(self.rStateSelector % len(RotationState))]

    def __Drop(self):
        while not self.__landed:
            self.__Move(DIRECTIONS["down"])
        #pygame.mixer.Sound.play(SoundEffects["Drop"])
    

    #Checks if pos is colliding
    def __Colliding(self, posToCheck):
        return any(map(Tile.TileCollision, self.__tiles, posToCheck))
    

    
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
        if key == pygame.K_q and self.shape != "O" and not self.Landed():
            self.__Rotate("CounterClockwise")
        if key == pygame.K_w and self.shape != "O" and not self.Landed():
            self.__Rotate("Clockwise")
        if key == pygame.K_LEFT and not self.Landed():
            self.__Move(DIRECTIONS["left"])
            pygame.mixer.Sound.play(SoundEffects["Move"])
        if key == pygame.K_RIGHT and not self.Landed():
            self.__Move(DIRECTIONS["right"])
            pygame.mixer.Sound.play(SoundEffects["Move"])
        if key == pygame.K_UP:
            self.__Drop()

    def Landed(self):
        return self.__landed

    def Hold(self, holdedTetro):
        if holdedTetro == None:
            return self
        else:
            translation = self.__tiles[0].pos - holdedTetro.__tiles[0].pos

            for tile in holdedTetro.__tiles:
                tile.pos += translation

            return holdedTetro
