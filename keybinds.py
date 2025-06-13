import pygame

jump = [pygame.K_w, pygame.K_SPACE, pygame.K_UP]

move_left = [pygame.K_a, pygame.K_LEFT]
move_right = [pygame.K_d, pygame.K_RIGHT]

def GetKeysPressed(keys : list[int]):
    """
    Checks if any of the keys in `keys` is currently pressed
    """
    for k in keys:
        if pygame.key.get_pressed()[k]:
            return True
    return False