class Player:
    x = 0
    y = 0
    velocity = 0
    gravity = 18.5
    speed = 450

    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

    def updatePhysics(self):
        """
        You gotta do `velocity -= gravity` when the player is supposed to fall
        """
        self.y += self.velocity