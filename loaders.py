import pygame
import os

class Image:
    def Load(filename, scene = "Game"):
        """
        Loads the image at `filename`, this needs to include the extension  
        If `scene` is the menu, just set it to "" (still put in the variable tho)
        """
        return pygame.image.load(os.path.join("images", scene, filename))
    
class Sound:
    def Load(filename):
        with open(os.path.join("sounds", filename)) as f:
            return pygame.mixer.Sound(f)