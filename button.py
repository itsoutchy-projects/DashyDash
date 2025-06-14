import pygame
import pygame.font

class Button:
    surface:pygame.Surface
    text = ""
    color = pygame.Color(255, 255, 255)
    pos = (0, 0)
    width = 500
    height = 100
    hovered = False
    pressed = False
    outlineThickness = 10
    outline = pygame.Color(0, 0, 0)

    onPressed = False # use an if statement to detect this event

    font:pygame.font.Font

    def __init__(self, surface : pygame.Surface, text : str, color : pygame.Color, pos : tuple[int, int], width : int, height : int, outlineThickness = 10, outline = pygame.Color(0, 0, 0)):
        self.surface = surface
        self.text = text
        self.color = color
        self.pos = pos
        self.width = width
        self.height = height
        self.font = pygame.font.Font(pygame.font.get_default_font(), 70)
        self.outlineThickness = outlineThickness
        self.outline = outline

    def draw(self):
        col = self.color
        mpos = pygame.mouse.get_pos()
        if mpos[0] > self.pos[0] and mpos[0] < self.pos[0] + self.width:
            if mpos[1] > self.pos[1] and mpos[1] < self.pos[1] + self.height:
                self.hovered = True
                col = pygame.Color(col.r - 50, col.g - 50, col.b - 50)
            else:
                self.hovered = False
        else:
            self.hovered = False
        if pygame.mouse.get_pressed()[0] and self.hovered:
            self.pressed = True
            col = pygame.Color(col.r - 100, col.g - 100, col.b - 100)
            if not self.onPressed == True:
                self.onPressed = True
            else:
                self.onPressed = False
        else:
            self.pressed = False
            self.onPressed = False
        pygame.draw.rect(self.surface, self.outline, (self.pos[0] - (self.outlineThickness / 2), self.pos[1] - (self.outlineThickness / 2), self.width + self.outlineThickness, self.height + self.outlineThickness))
        pygame.draw.rect(self.surface, col, (self.pos[0], self.pos[1], self.width, self.height))
        txt = self.font.render(self.text, True, "black")
        #textPos = (self.pos[0] + (self.width / 2), (self.pos[1] / 2) + (self.font.size(self.text)[1] / 2))
        textPos = ((self.pos[0] + (self.width / 2)) - (self.font.size(self.text)[0] / 2), (self.pos[1] + (self.height / 2)) - (self.font.size(self.text)[1] / 2))
        self.surface.blit(txt, textPos)