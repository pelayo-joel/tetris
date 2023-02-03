from const import *

class Tile:
    def __init__(self, pos:pygame.Vector2, sprite:pygame.image):
        self.pos = pos
        self.sprite = sprite




    def TileRotation(self, pivot:pygame.Vector2, clockOrientation):
        degree = 90
        if clockOrientation == "CounterClockwise":
            degree = -90
        origin = self.pos - pivot
        rotated = origin.rotate(degree)
        return rotated + pivot
    
    def TileCollision(self):
        if 0 <= self.pos.x <= PLAYFIELD_W and self.pos.y <= PLAYFIELD_H:
            return False
        return True





class Tetromino:
    def __init__(self, parent:pygame.Surface):
        self.frame = parent
        self.shape = random.choice(list(Tetrominoes.keys()))
        self.tileSPrite = pygame.image.load(f"{TILE_PATH}Block{self.shape}.png")
        self.tiles = self.__Tetromino()
        self.rStateSelector = 0
        self.spawnOrientation = RotationState[self.rStateSelector]


    """Private methods"""

    #Creates the tetromino itself
    def __Tetromino(self):
        TetrominoShape = []
        self.tileSprite = pygame.transform.smoothscale(self.frame, (PLAYFIELD_CELL_SIZE, PLAYFIELD_CELL_SIZE))
        
        for pos in Tetrominoes[self.shape]:
            tile = Tile(pos, self.tileSprite)
            TetrominoShape.append(tile)
        
        return TetrominoShape
    

    """Public methods"""

    #Defines the Tetromino movement
    def Move(self, direction:pygame.Vector2):
        nextPos = []
        for tile in self.tiles:
            nextPos.append(tile.pos + direction)

        if not self.Colliding(nextPos):
            for tile in self.tiles:
                tile.pos += direction

    def Rotate(self, clockOrientation):
        nextPos = []
        for tile in self.tiles:
            nextPos.append(tile.TileRotation(self.tiles[0].pos, clockOrientation))
        
        if not self.Colliding(nextPos):
            for tile in self.tiles:
                tile.TileRotation(self.tiles[0], clockOrientation)
            if clockOrientation == "Clockwise":
                self.rStateSelector += 1
            elif clockOrientation == "CounterClockwise":
                self.rStateSelector -= 1

        elif clockOrientation == "Clockwise":
            return None
        
        self.spawnOrientation = RotationState[self.rStateSelector]

            

    #Checks if pos is colliding
    def Colliding(self, posToCheck):
        return any(map(Tile.TileCollision, self.tiles, posToCheck))
            