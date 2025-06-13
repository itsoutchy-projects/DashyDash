import pygame
import os
from button import Button
import loaders
from classes import *
import keybinds
import save
import logger
import os
import sys
import math
import requests
import webbrowser
import github
import pathlib
import network_utils

if getattr(sys, 'frozen', False):
    os.chdir(pathlib.Path(__file__).parent)

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)

running = True

player = Player(200, 500)

jumpHeight = 6

jumpJustPressed = False # jump has not been held down

gameTitle = "DashyDash"

#shadow_offset = 10

touchingGround = False

menuBg = pygame.image.load(os.path.join("images", "bg.png"))
logo = pygame.image.load(os.path.join("images", "logo.png"))

player_size = 100

clock = pygame.time.Clock()

play = Button(screen, "PLAY", pygame.Color(255, 255, 255), ((screen.get_width() / 2) - 250, 500), 500, 100)

ground_img = loaders.Image.Load("ground.png")
ground_rect = ground_img.get_rect()

groundHeight = ground_img.get_height() # orig: 100

bg = loaders.Image.Load("bg.png")
bg_rect = ground_img.get_rect()

fpsFont = pygame.font.Font(pygame.font.get_default_font(), 16)
exitFont = pygame.font.Font(pygame.font.get_default_font(), 32)

fps = 60
heldFrames = 0

exitAlpha = 255

DEBUG = False
# if true, enables debugging features
# these include free camera movement
# (maybe) visualisers of special stuff
if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        DEBUG = True

class coord:
    x:int
    y:int

    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

camera = {
    "x": 0,
    "y": 0
}

def ScreenCenter(screen : pygame.Surface, img : pygame.Surface, axis : str = "xy") -> coord:
    """
    Returns the position of `img` centered on `screen`  
    `Axis` - Represents the axis to center `img` on ("x", "y", or "xy")
    """
    x = 0
    y = 0
    if "x" in axis.lower():
        x = (screen.get_width() / 2) - (img.get_width() / 2)
    if "y" in axis.lower():
        y = (screen.get_height() / 2) - (img.get_height() / 2)
    return coord(x - camera["x"], y - camera["y"])

scene = "MainMenu" # change this when you need

sceneOff = {
    "x": 0,
    "y": -220
}

class GameObject:
    x = 0
    y = 0
    color = "#2c0070"
    width = 500
    height = 250

    def __init__(self, x : int, y : int, color = "#2c0070", width = 400, height = 100):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        pass

objects = [
    GameObject(500, 360),
    GameObject(1000, 200),
    GameObject(400, 130)
]

playerMovesCamera = True
# if true, when the player moves, the camera also moves

focused = True

playerCamMovToggleWasPressed = False

# replace these with the details of your repo
# so the url would go {username}/{repo}
username = "itsoutchy-projects"
repo = "DashyDash"

#region Update Checker
def waitUntilKey(key, ucheck = True):
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == key:
                    return
                if event.key == pygame.K_LSHIFT and ucheck:
                    url = github.GetRelease(username, repo)["url"]
                    webbrowser.open(url)

#if network_utils.hasConnection(): # no need, we good
try:
    verResp = requests.get(f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/main/version.txt")
    githubVer = str(verResp._content).removeprefix("b'").removesuffix("'")
    localVer = ""
    with open("version.txt") as f:
        localVer = f.read()
    if float(localVer.removeprefix("v")) < float(githubVer.removeprefix("v")):
        text = fpsFont.render(f"{githubVer} is available!\n\nPress SPACE to continue or Press LEFT SHIFT to go to GitHub", True, "white")
        cent = ScreenCenter(screen, text)
        screen.blit(text, (cent.x, cent.y))
        pygame.display.flip()
        waitUntilKey(pygame.K_SPACE)
except Exception as e:
    logger.warn("Couldn't get latest version because player has no WiFi")
    logger.error(f"Actual error: {e}")
#endregion
#else:
    #logger.warn("Couldn't get latest version because player has no WiFi")

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.WINDOWFOCUSGAINED:
            focused = True
        if e.type == pygame.WINDOWFOCUSLOST:
            focused = False
    if focused:
        screen.fill("black")
        pygame.display.set_caption(f"{gameTitle} - {scene}")
        if scene == "MainMenu":
            screen.blit(menuBg, (0, 0))
            logCentered = ScreenCenter(screen, logo, "x")
            logCentered.y = 100
            screen.blit(logo, (logCentered.x, logCentered.y))
            #pygame.draw.rect(screen, "white", ((screen.get_width() / 2) - 250, 500, 500, 100))
            
            play.draw()
            if play.onPressed:
                scene = "Game" # switch to game (or level select)
                play.onPressed = False
        elif scene == "Game":
            # game scene
            try:
                #pygame_shaders.clear((100, 100, 100))
                #screen.fill((0, 0, 0)) #Fill with the color you set in the colorkey
                window = {
                    "width": pygame.display.get_window_size()[0],
                    "height": pygame.display.get_window_size()[1]
                }
                slowness = 5 # how much slower the background move compared to everything else
                bgOffsetDefault = {
                    "x": -500,
                    "y": 0
                }
                bg_rect.x = bgOffsetDefault["x"] - (camera["x"] / slowness)
                bg_rect.y = bgOffsetDefault["y"] - (camera["y"] / slowness)
                screen.blit(bg, bg_rect)
                #pygame.draw.rect(screen, pygame.Color(0, 0, 0, 80), (player.x + shadow_offset, pygame.display.get_window_size()[1] - player.y, 100, 100))
                pygame.draw.rect(screen, "blue", (player.x - camera["x"] - sceneOff["x"], window["height"] - player.y - camera["y"] - sceneOff["y"], player_size, player_size)) # draw player
                # pygame.draw.rect(screen, "red", (0, window["height"] - groundHeight, window["width"], groundHeight))
                groundX = ScreenCenter(screen, ground_img, "x").x
                screen.blit(ground_img, (groundX - camera["x"] - sceneOff["x"], window["height"] - groundHeight - camera["y"] - sceneOff["y"]))

                player.velocity -= player.gravity
                player.updatePhysics()
                if playerMovesCamera:
                    camera["y"] -= player.velocity
                if window["height"] - player.y + player_size > window["height"] - groundHeight:
                    # player is in the ground.. oops
                    # player.y = pygame.display.get_window_size()[1] - groundHeight - 100 # set it equal to the ground y
                    player.y -= player.velocity
                    if playerMovesCamera:
                        camera["y"] += player.velocity
                    player.velocity = 0
                    touchingGround = True
                else:
                    if not player.y + player_size - window["height"] == window["height"] - groundHeight:
                        touchingGround = False

                i = 0
                for g in objects:
                    # why is it only doing the first one???????????????????????????????????????????????????????????
                    # pythonn pleaseplsplspls before i tear this code apart D:
                    #g = objects[i]
                    pygame.draw.rect(screen, g.color, (g.x - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], g.width, g.height))
                    if DEBUG:
                        print(((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and (player.y > g.y and player.y < g.y + g.height))
                    if (player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width:
                        #if player.x + player_size > g.x:
                        if player.y > g.y and player.y < g.y + g.height:
                            print(f"collision detecting platform {i}")
                            logger.message("touching box :D")
                            player.y -= player.velocity
                            if playerMovesCamera:
                                camera["y"] += player.velocity
                            player.velocity = 0
                            touchingGround = True
                    i += 1
                #print(touchingGround)
                keys = pygame.key.get_pressed()
                if keybinds.GetKeysPressed(keybinds.jump) and touchingGround:
                    if not jumpJustPressed:
                        player.velocity = jumpHeight
                        jumpJustPressed = True
                else:
                    jumpJustPressed = False
                if keybinds.GetKeysPressed(keybinds.move_left):
                    player.x -= player.speed
                    if playerMovesCamera:
                        camera["x"] -= player.speed
                if keybinds.GetKeysPressed(keybinds.move_right):
                    player.x += player.speed
                    if playerMovesCamera:
                        camera["x"] += player.speed
                for g in objects:
                    if DEBUG:
                        print(player.y < g.y or player.y + player_size > g.y)
                    # (player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width
                    #(player.x + player_size > g.x or player.x < g.x + g.width) and (player.y < g.y or player.y + player_size > g.y)
                    if ((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and (player.y > g.y and player.y < g.y + g.height):
                    #if player.x > g.x and player.x < g.x + g.width:
                            logger.message("horizontal collision! :D")
                            player.x -= player.speed
                            if playerMovesCamera:
                                camera["x"] -= player.speed
                            if ((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and player.y > g.y and player.y < g.y + g.height:
                                player.x += player.speed * 2 # move out to compensate
                                if playerMovesCamera:
                                    camera["x"] += player.speed * 2
                if DEBUG:
                    if keys[pygame.K_p]:
                        player.gravity += 0.01
                    if keys[pygame.K_SEMICOLON]:
                        player.gravity -= 0.01
                    if keys[pygame.K_j]:
                        camera["x"] -= player.speed
                    if keys[pygame.K_l]:
                        camera["x"] += player.speed
                    if keys[pygame.K_i]:
                        camera["y"] -= player.speed
                    if keys[pygame.K_k]:
                        camera["y"] += player.speed
                    scale = (10, 10)
                    pygame.draw.rect(screen, "white", ((screen.get_width() / 2) - scale[0], (screen.get_height() / 2) - scale[1], scale[0], scale[1]))
                    if keys[pygame.K_b]:
                        if not playerCamMovToggleWasPressed:
                            playerMovesCamera = not playerMovesCamera
                            playerCamMovToggleWasPressed = True
                    else:
                        playerCamMovToggleWasPressed = False
                    #region Debug Overlay
                    overlayTxt = f"""DEBUG KEYS
Change Gravity: P - Up | Semicolon - Down
Move Camera: IJKL - Move the camera offset
Lock/unlock camera: B - Stops player from moving camera
OTHER INFO
Mouse Position: X: {pygame.mouse.get_pos()[0]}, Y:{pygame.mouse.get_pos()[1]}
Camera Offset: X: {camera['x']}, Y: {camera["y"]}
Player Position: X: {player.x}, Y: {player.y}
Gravity: {player.gravity}
"""
                    txtSize = (500, 160)
                    #bg = pygame.Surface(size)
                    pygame.draw.rect(screen, pygame.Color(30, 30, 30), (0, 50, txtSize[0], txtSize[1]))
                    #bg.set_alpha(0.5)
                    #screen.blit(bg, (0, 0))
                    txt = fpsFont.render(overlayTxt, True, "white")
                    screen.blit(txt, (0, 50))
                    #endregion

                # pls keep this last.. thx
                screen.blit(fpsFont.render(f"FPS: {round(clock.get_fps())}", True, "white"), (0, 0)) # draw fps
                if keys[pygame.K_ESCAPE]:
                    txt = exitFont.render("EXITTING...", True, "white")
                    txt.set_alpha(exitAlpha)
                    screen.blit(txt, (0, 16))
                    if heldFrames == 5 * fps:
                        running = False
                    heldFrames += 1
                    logger.message(f"exitAlpha: {10 / (5 * fps)}")
                    # math.ceil(100 / (5 * fps)) # thrown here in case you wanna use it. i couldnt figure it out
                    exitAlpha -= 1
                    if exitAlpha < 0:
                        exitAlpha = 0 # alpha cant be negative because... duh
                    logger.message(f"exitAlpha: {exitAlpha}")
                else:
                    heldFrames = 0
                    exitAlpha = 255
                #shader.render(display) #Render the display onto the OpenGL display with the shaders!
                pygame.display.flip()
            except Exception as e:
                logger.crash(e)
                running = False

        pygame.display.flip()
    clock.tick(fps)

pygame.quit()