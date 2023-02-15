import time
from const import *
from pygame.locals import *
from pygame import gfxdraw

"""Objects file, wanted to separate my classes with the main script to make it cleaner, each of these objects have customizable style and functionnalities"""

"""Created a 'Frame' object, it inherits the 'Surface' class from pygame"""
class Frame(pygame.Surface):
    """Constructor"""
    def __init__(self, parent:pygame.Surface, size:tuple, pos:tuple=(0, 0), color:tuple=(0, 0, 0), surfImage:pygame.image=None):
        pygame.Surface.__init__(self, size)
        self.set_colorkey((0, 0, 0))
        self.width, self.height = size[0], size[1]
        self.pos = (pos[0], pos[1])
        self.color = color
        self.parent = parent
        self.surfImage = surfImage
        self.fill(self.color)


    """Public methods"""

    #Returns the position of the Frame
    def get_SurfPos(self):
        return self.pos

    #Returns the Frame's color
    def get_SurfColor(self):
        return self.color
    
    def get_SurfSize(self):
        return (self.width, self.height)

    #Enables the frame, called every frame in pygame's mainloop and also in other objects
    def ActiveFrame(self, drawPos:tuple=(), image:pygame.image=None):
        if drawPos == ():
            drawPos = self.pos
    
        if image != None:
            self.surfImage = pygame.transform.smoothscale(image, (self.width, self.height))
            self.parent.blit(self.surfImage, drawPos)
        elif self.surfImage != None:
            self.surfImage = pygame.transform.smoothscale(self.surfImage, (self.width, self.height))
            self.parent.blit(self.surfImage, drawPos)
        else:
            self.parent.blit(self, drawPos)






"""'TextLabel' object, similar to the 'Label' object from tkinter it just displays text onto a surface by creating its own (which also serves as a background)"""
class TextLabel:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, text:str, size:int, font:str=None, color:tuple=(255, 255, 255), bgColor:tuple=None, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False):
        self.frame = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.textSize = size
        self.font = font
        self.text = text
        self.color = color
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY

        try:
            self.bg = self.frame.get_SurfColor()
            if bgColor != None:
                self.bg = bgColor
        except AttributeError:
            self.bg = (0, 0, 0)
            
        if self.font == None:
            self.textFont = pygame.font.Font(FONT_PATH, self.textSize)
        else:
            self.textFont = pygame.font.Font(self.font, self.textSize)
        
        self.myText = self.textFont.render(self.text, True, self.color)
        self.width, self.height = self.myText.get_width(), self.myText.get_height()
        self.__InitPos()
        self.textFrame = Frame(self.frame, (self.width, self.height), (self.left, self.top), color=self.bg)
        self.textFrame.blit(self.myText, (0, 0))
        self.textFrame.ActiveFrame((self.left, self.top))
        pygame.display.update()


    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        self.width, self.height = self.myText.get_width(), self.myText.get_height()
        if self.centerX and self.centerY == False:
            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY
        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX
        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)
        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        else:
            self.left = self.posX
            self.top = self.posY


    """Public methods"""

    #Changes the text by newText
    def NewText(self, newText):
        self.textFrame.fill(self.bg)
        self.textFrame.ActiveFrame((self.left, self.top))

        self.text = newText
        self.myText = self.textFont.render(self.text, True, self.color)
        self.width, self.height = self.myText.get_width(), self.myText.get_height()
        self.__InitPos()

        self.textFrame = Frame(self.frame, (self.width, self.height), (self.left, self.top), color=self.bg)
        self.textFrame.blit(self.myText, (0, 0))
        self.textFrame.ActiveFrame((self.left, self.top))
        pygame.display.update(self.textFrame.get_rect())

        


"""A 'Button' class, as its name implies it creates buttons :D"""
class Button:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, width:int, height:int, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=0, type:str="Bool", buttonLabel:str="Button", imageButton:str=None, func=None):

        self.frame = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.width, self.height = width, height
        self.__InitPos()

        self.borderRad = borderR
        self.fill = color
        self.buttonType = type
        self.state = False
        self.label, self.activeLab, self.unactiveLab = buttonLabel, buttonLabel, buttonLabel
        self.command = func
        self.buttonFormat = None

        if imageButton != None:
            self.buttonFormat = pygame.image.load(imageButton).convert_alpha()
            self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
            self.frame.blit(self.buttonFormat, (self.left, self.top))
            self.isImage = True
        elif imageButton == None:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.isImage = False


    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:
            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY
        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX
        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)
        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        else:
            self.left = self.posX
            self.top = self.posY

    #Sets up the label on the button wether if it's an image or a text
    def __DrawLabel(self, label, color=(0, 0, 0)):
        if isinstance(label, str) and "/" not in label:
            font = pygame.font.Font(FONT_PATH, 30)
            myText = font.render(label, True, color)
            self.frame.blit(myText, myText.get_rect(center=self.buttonFormat.center))
        else:
            img = pygame.image.load(label).convert_alpha()
            img = pygame.transform.smoothscale(img, (self.width/2, self.height/2))
            self.frame.blit(img, img.get_rect(center=self.buttonFormat.center))

    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, min:int, max:int):
        if value > max:
            value = max
        elif value < min:
            value = min
        return value


    """Public methods"""

    #Detects if the object has been clicked, different behaviour depending on its type
    def Click(self):
        if pygame.mouse.get_pressed()[0] and self.buttonType == "Bool":
            if self.state == False:
                self.label = self.activeLab
                self.state = True
            else:
                self.label = self.unactiveLab
                self.state = False
            self.__DrawLabel(self.label)
            pygame.display.update()
            self.command()
            time.sleep(0.07)
        if pygame.mouse.get_pressed()[0] and self.buttonType == "OnClick":
            self.command()
            time.sleep(0.5)

    #Enables the button, called every frame in pygame's mainloop
    def ActiveButton(self, buttonClicked=None):
        self.activeLab = buttonClicked
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1])
        if self.isImage:
            imgPos = self.buttonFormat.get_rect().move(self.left, self.top)
            if imgPos.collidepoint(mousePosToFrame):
                self.Click()
        elif self.isImage == False and self.buttonFormat.collidepoint(mousePosToFrame):
            hover = (self.__Cap(self.fill[0]*1.2, 0, 255), self.__Cap(self.fill[1]*1.2, 0, 255), self.__Cap(self.fill[2]*1.2, 0, 255))
            self.buttonFormat = pygame.draw.rect(self.frame, hover, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            pygame.display.update()
            self.__DrawLabel(self.label)
            self.Click() 
        elif self.isImage == False:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.__DrawLabel(self.label)
            pygame.display.update()

    #Changes the image
    def ImgChange(self, newImage:str):
        self.buttonFormat = pygame.image.load(newImage).convert_alpha()
        self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
        self.frame.blit(self.buttonFormat, (self.left, self.top))





"""Slider object"""
class Slider:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, length:int, total:int, axis:str, thickness:int=5, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=50, setterStyle:str="rect"):
        self.frame = parent
        self.length = length
        self.limit = total
        self.fill = color
        self.borderRad = borderR
        self.width, self.height = thickness, thickness
        frameW, frameH = self.width, self.height
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.orientation = axis
        self.setterStyle = setterStyle
        self.changing = False

        try:
            if setterStyle.lower() == "rect" or setterStyle.lower() == "circle":
                self.setterStyle = setterStyle
        except:
            exit(f"Variable 'setterStyle' must be either 'rect' or 'circle'")
        if self.orientation.lower() == "x":
            self.width = length
            frameW, frameH = self.width, self.height*3
        elif self.orientation.lower() == "y":
            self.height = length
            frameW, frameH = self.width*3, self.height
        self.__InitPos()

        self.slideFrame = Frame(self.frame, (frameW, frameH), (self.left, self.top), color=self.frame.get_SurfColor())
        self.slideValue = int((1/self.limit)*100)
        pygame.display.update()


    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:
            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY
        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX
        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)
        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        else:
            self.left = self.posX
            self.top = self.posY

    #Sets the value of the slider, the slider works with three rectangles that are growing/shrinking/moving depending on its value
    def __SetValue(self):
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0]-self.slideFrame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1]-self.slideFrame.get_SurfPos()[1])
        progressColor = (self.__Cap(self.fill[0]*15, 0, 255), self.__Cap(self.fill[1]*15, 0, 255), self.__Cap(self.fill[2]*15, 0, 255))
        
        if self.orientation.lower() == "x":
            if pygame.mouse.get_pressed()[0] and (self.changing or self.slideBar.collidepoint(mousePosToFrame) or self.slideBarValue.collidepoint(mousePosToFrame)):
                self.changing = True
                self.slideValue = int((self.__Cap((mouse_pos[0]-self.frame.get_SurfPos()[0]-self.left), 0, self.width)/self.width)*100)
            elif pygame.mouse.get_pressed()[0] == False:
                self.changing = False

            setValue = self.__Cap(int(self.width*(self.slideValue/100)), 0, self.width)
            self.slideBarValue = pygame.draw.rect(self.slideFrame, progressColor, pygame.Rect(0, ((self.slideFrame.get_rect().height/2)-self.height/2), setValue, self.height), border_radius=self.borderRad)
            self.slideBar = pygame.draw.rect(self.slideFrame, (10, 10, 10), pygame.Rect(setValue, ((self.slideFrame.get_rect().height/2)-self.height/2), (self.width-setValue), self.height), border_radius=self.borderRad)
            if self.setterStyle.lower() == "rect":
                pygame.draw.rect(self.slideFrame, (150, 150, 150), pygame.Rect(setValue, 0, 3, self.slideFrame.get_rect().height), 5)
            elif self.setterStyle.lower() == "circle":
                pygame.draw.circle(self.slideFrame, (150, 150, 150), (setValue, self.slideFrame.get_rect().height/2), 5)
                   
        elif self.orientation.lower() == "y":
            if pygame.mouse.get_pressed()[0] and (self.changing or self.slideBar.collidepoint(mousePosToFrame) or self.slideBarValue.collidepoint(mousePosToFrame)):
                self.changing = True
                self.slideValue = int((self.__Cap(self.height-(mouse_pos[1]-self.frame.get_SurfPos()[1]-self.top), 0, self.height)/self.height)*100)
            elif pygame.mouse.get_pressed()[0] == False:
                self.changing = False

            setValue = self.height - self.__Cap(int(self.height*(self.slideValue/100)), 0, self.height)
            self.slideBarValue = pygame.draw.rect(self.slideFrame, progressColor, pygame.Rect(((self.slideFrame.get_rect().width/2)-self.width/2), self.height, self.width, -self.height+setValue), border_radius=self.borderRad)
            self.slideBar = pygame.draw.rect(self.slideFrame, (10, 10, 10), pygame.Rect(((self.slideFrame.get_rect().width/2)-self.width/2), 0, self.width, setValue), border_radius=self.borderRad)
            if self.setterStyle.lower() == "rect":
                pygame.draw.rect(self.slideFrame, (150, 150, 150), pygame.Rect(0, setValue, self.slideFrame.get_rect().width, 3), 5)
            elif self.setterStyle.lower() == "circle":
                pygame.draw.circle(self.slideFrame, (150, 150, 150), (self.slideFrame.get_rect().width/2, setValue), 5)
    
    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, min:int= (-1000), max:int=0):
        if value > max:
            value = max
        elif value < min:
            value = min
        return value


    """Public methods"""

    #Update the value of the slider when called
    def Update(self, newTotal):
        self.limit = newTotal
        self.slideValue = 0
        progressColor = (self.__Cap(self.fill[0]*15, 0, 255), self.__Cap(self.fill[1]*15, 0, 255), self.__Cap(self.fill[2]*15, 0, 255))
        if self.orientation.lower() == "x":
            self.slideBarValue = pygame.draw.rect(self.frame, progressColor, pygame.Rect(self.left, self.top, int(self.width*(self.slideValue/100)), self.height), border_radius=self.borderRad)
        elif self.orientation.lower() == "y":
            self.slideBarValue = pygame.draw.rect(self.frame, progressColor, pygame.Rect(self.left, self.top, self.width, int(self.height*(self.slideValue/100))), border_radius=self.borderRad)
        self.slideBar = pygame.draw.rect(self.frame, (10, 10, 10), pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)

    #Enables the slider, called every frame in pygame's mainloop
    def ActiveSlider(self, progress:int=0):
        if progress != 0:
            self.slideValue = int((progress/self.limit)*100)
        self.__SetValue()
        self.slideFrame.ActiveFrame()
        self.slideFrame.fill(self.frame.get_SurfColor())
        pygame.display.update(self.slideFrame.get_rect())
    
    #Returns the slider's value
    def GetSlideValue(self):
        return self.slideValue

    #Returns if the slider is being clicked
    def GetChangingState(self):
        return self.changing




"""For anti-aliased rounded shapes"""
class GfxButton:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, width:int, height:int, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=0, type:str="Bool", buttonLabel:str="Button", imageButton:str=None, func=None):

        self.frame = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.width, self.height = width, height
        self.__InitPos()

        self.borderRad = borderR
        self.fill = color
        self.buttonType = type
        self.state = False
        self.label, self.activeLab, self.unactiveLab = buttonLabel, buttonLabel, buttonLabel
        self.command = func
        self.buttonFormat = None

        if imageButton != None:
            self.buttonFormat = pygame.image.load(imageButton).convert_alpha()
            self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
            self.frame.blit(self.buttonFormat, (self.left, self.top))
            self.isImage = True
        elif imageButton == None:
            if borderR != 0:
                cornerPosX = self.left
                cornerPosY = self.top
                for i in range(4):
                    if i == 1 or i == 2:
                        cornerPosX = self.left + self.width
                    else:
                        cornerPosX = self.left
                    if i == 2 or i == 3:
                        cornerPosY = self.top + self.height
                    else:
                        cornerPosY = self.top
                    gfxdraw.aacircle(self.frame, cornerPosX, cornerPosY, borderR-1, self.fill)
                    gfxdraw.filled_circle(self.frame, cornerPosX, cornerPosY, borderR-1, self.fill)
                gfxdraw.box(self.frame, pygame.Rect(self.left-borderR, self.top, self.width+(borderR*2), self.height), self.fill)
                gfxdraw.box(self.frame, pygame.Rect(self.left, self.top-borderR, self.width, self.height+(borderR*2)), self.fill)
            self.buttonFormat = gfxdraw.box(self.frame, pygame.Rect(self.left, self.top, self.width, self.height), self.fill)
            self.isImage = False


    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:
            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY
        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX
        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)
        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        else:
            self.left = self.posX
            self.top = self.posY

    #Sets up the label on the button wether if it's an image or a text
    def __DrawLabel(self, label, color=(0, 0, 0)):
        if isinstance(label, str) and "/" not in label:
            font = pygame.font.Font(FONT_PATH, 30)
            myText = font.render(self.label, True, color)
            self.frame.blit(myText, myText.get_rect(center=self.buttonFormat.center))
        else:
            img = pygame.image.load(label).convert_alpha()
            img = pygame.transform.smoothscale(img, (self.width/2, self.height/2))
            self.frame.blit(img, img.get_rect(center=self.buttonFormat.center))

    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, min:int, max:int):
        if value > max:
            value = max
        elif value < min:
            value = min
        return value


    """Public methods"""

    #Detects if the object has been clicked, different behaviour depending on its type
    def Click(self):
        if pygame.mouse.get_pressed()[0] and self.buttonType == "Bool":
            if self.state == False:
                self.label = self.activeLab
                self.state = True
            else:
                self.label = self.unactiveLab
                self.state = False
            self.__DrawLabel(self.label)
            pygame.display.update()
            self.command()
            time.sleep(0.07)
        if pygame.mouse.get_pressed()[0] and self.buttonType == "OnClick":
            self.command()
            time.sleep(0.5)

    #Enables the button, called every frame in pygame's mainloop
    def ActiveButton(self, buttonClicked=None):
        self.activeLab = buttonClicked
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1])
        if self.isImage:
            imgPos = self.buttonFormat.get_rect().move(self.left, self.top)
            if imgPos.collidepoint(mousePosToFrame):
                self.Click()
        elif self.isImage == False and self.buttonFormat.collidepoint(mousePosToFrame):
            hover = (self.__Cap(self.fill[0]*1.2, 0, 255), self.__Cap(self.fill[1]*1.2, 0, 255), self.__Cap(self.fill[2]*1.2, 0, 255))
            self.buttonFormat = pygame.draw.rect(self.frame, hover, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            pygame.display.update()
            self.__DrawLabel(self.label)
            self.Click() 
        elif self.isImage == False:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.__DrawLabel(self.label)
            pygame.display.update()

    #Changes the image
    def ImgChange(self, newImage:str):
        self.buttonFormat = pygame.image.load(newImage).convert_alpha()
        self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
        self.frame.blit(self.buttonFormat, (self.left, self.top))





class GridMap:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, cellSize:tuple, posX:int, posY:int, nColumns:int, nRows:int, centerX:bool=False, centerY:bool=False, pourcentMode:bool=False, 
    cellGap:int=0, gridBG:tuple=(5, 5, 5)):
        self.frame = parent
        self.__cell = cellSize
        self.__cellGap = cellGap
        self.__gridBG = gridBG
        self.__parentMidX, self.__parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.__centerX, self.__centerY, self.__pourcentMode, self.__posX, self.__posY = centerX, centerY, pourcentMode, posX, posY
        self.nColumns, self.nRows = nColumns, nRows
        self.__InitPos()

        self.gridSurf = Frame(self.frame, ((self.__cell[0]+self.__cellGap) * self.nColumns, (self.__cell[1]+self.__cellGap) * self.nRows), (self.left, self.top), self.__gridBG)
        self.__InitGrid()

        self.gridSurf.ActiveFrame()
    
    """Private methods (utility for the class)"""
    
    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.__centerX and self.__centerY == False:
            if self.__pourcentMode:
                self.left = self.__parentMidX-(self.nRows/2)
                self.top = int(self.frame.get_height() * ((self.__posY)/100)) - int(self.nRows/2)
            else:
                self.left = self.__parentMidX-(self.nRows/2)
                self.top = self.__posY
        elif self.__centerY and self.__centerX == False:
            if self.__pourcentMode:
                self.top = self.__parentMidY-(self.nRows/2)
                self.left = int(self.frame.get_width() * ((self.__posX)/100)) - int(self.nRows/2)
            else:
                self.top = self.__parentMidY-(self.nRows/2)
                self.left = self.__posX
        elif self.__centerX and self.__centerY:
            self.top = self.__parentMidY-(self.nRows/2)
            self.left = self.__parentMidX-(self.nRows/2)
        elif self.__pourcentMode:
            self.left = int(self.frame.get_width() * ((self.__posX)/100)) - int(self.nRows/2)
            self.top = int(self.frame.get_height() * ((self.__posY)/100)) - int(self.nRows/2)
        else:
            self.left = self.__posX
            self.top = self.__posY

    #Creates the grid depending on defined cell size and number of columns/rows
    def __InitGrid(self):
        for row in range(0, self.nColumns):
            for column in range(0, self.nRows):
                cellRect = pygame.Rect((self.__cell[0]+self.__cellGap) * row, (self.__cell[1]+self.__cellGap) * column, self.__cell[0], self.__cell[1])
                gfxdraw.rectangle(self.gridSurf, cellRect, (15, 15, 15))

    def GridUpdate(self):
        self.__InitGrid()
        self.gridSurf.ActiveFrame()
        self.gridSurf.fill(self.__gridBG)
        pygame.display.update(self.gridSurf.get_rect())



    