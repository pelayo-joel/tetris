from const import *
import widgets



class PlayField(widgets.GridMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stackGroup = pygame.sprite.Group()
        self.stack = []

    def FillCell(self, landedTile):
        self.__stackGroup.add(landedTile)
        self.stack.append(landedTile.rect.topleft)

    def DrawStack(self):
        self.__stackGroup.draw(self.gridSurf)

    def ClearStack(self):
        self.__stackGroup.empty()
        self.stack = []

    def CheckLoss(self):
        for tile in self.__stackGroup:
            if tile.rect.y < 0:
                return True

        return False

        
    






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
    
    def TileCollision(self, posToCheck):
        posX, posY = posToCheck.x * PLAYFIELD_CELL_SIZE, posToCheck.y * PLAYFIELD_CELL_SIZE
        if 0 <= posX < PLAYFIELD_W and posY < PLAYFIELD_H and ((posX, posY) not in self.playfield.stack):
            return False
        return True





class Tetromino:
    def __init__(self, parent:PlayField):
        self.playfield = parent
        self.shape = random.choice(list(Tetrominoes.keys()))
        self.tileSprite = pygame.image.load(f"{TILE_PATH}Block{self.shape}.png").convert_alpha()
        self.__tileSpriteGroup = pygame.sprite.Group()
        
        self.tiles = self.__Tetromino()
        self.rStateSelector = 0
        self.rOrientation = RotationState[self.rStateSelector]
        self.__landed = False


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
                testKick = [self.tiles[0].pos + kick]
                for i in range                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      (1, 4):
                    testKick.append(self.tiles[i].TileRotation(self.tiles[0].pos, orientation) + kick)
                
                if not self.Colliding(testKick):
                    self.TetrominoUpdate(testKick)
                    break

        elif orientation == "CounterClockwise":
            for kick in WallKickData[kickSet][RotationState[(self.rStateSelector - 1) % len(RotationState)]]:
                testKick = [self.tiles[0].pos - kick]
                for i in range(1, 4):
                    testKick.append(self.tiles[i].TileRotation(self.tiles[0].pos, orientation) - kick)
                
                if not self.Colliding(testKick):
                    self.TetrominoUpdate(testKick)
                    break


    """Public methods"""

    #Defines the Tetromino movement
    def Move(self, direction:pygame.Vector2):
        nextPos = []
        for tile in self.tiles:
            nextPos.append(tile.pos + direction)

        if not self.Colliding(nextPos):
            self.TetrominoUpdate(nextPos)
        elif direction == DIRECTIONS['down']:
            self.__landed = True

    #Rotates the tetromino in clockwise or counterclockwise rotation
    def Rotate(self, clockOrientation):
        nextPos = []
        for tile in self.tiles:
            nextPos.append(tile.TileRotation(self.tiles[0].pos, clockOrientation))
        print(nextPos)
        if not self.Colliding(nextPos):
            self.TetrominoUpdate(nextPos)
            
            if clockOrientation == "Clockwise":
                self.rStateSelector += 1
            elif clockOrientation == "CounterClockwise":
                self.rStateSelector -= 1

        elif clockOrientation == "Clockwise":
            print("Trying wallkick")
            self.__WallKickTesting(clockOrientation)

        elif clockOrientation == "CounterClockwise":
            print("Trying wallkick")
            self.__WallKickTesting(clockOrientation)
            
        self.rOrientation = RotationState[(self.rStateSelector % len(RotationState))]

    #Checks if pos is colliding
    def Colliding(self, posToCheck):
        return any(map(Tile.TileCollision, self.tiles, posToCheck))
    
    def TetrominoUpdate(self, newTile):
        for i in range(4):
            self.tiles[i].pos = newTile[i]
            self.tiles[i].TileUpdate()
        self.playfield.GridUpdate()
        self.__tileSpriteGroup.update()
        self.__tileSpriteGroup.draw(self.playfield.gridSurf)

    def TetrominoFall(self):
        self.Move(DIRECTIONS["down"])

    def Landed(self):
        return self.__landed
    
    def RerollShape(self, bag, current):
        while bag.count(self.shape) >= 2 or self.shape == current:
            self.shape = random.choice(list(Tetrominoes.keys()))
        self.tileSprite = pygame.image.load(f"{TILE_PATH}Block{self.shape}.png").convert_alpha()
        self.__tileSpriteGroup = pygame.sprite.Group()
        self.tiles = self.__Tetromino()

    def AddToStack(self):
        for tile in self.tiles:
            self.playfield.FillCell(tile)


