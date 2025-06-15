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
import static_values
import datetime

if getattr(sys, 'frozen', False):
    os.chdir(pathlib.Path(__file__).parent)

pygame.init()
size = (1280, 720)
actualWindowSize = (1280, 720)
screen = pygame.display.set_mode(actualWindowSize)

running = True

player = Player(200, 500)

jumpHeight = 750

jumpJustPressed = False # jump has not been held down

gameTitle = "DashyDash"

#shadow_offset = 10

touchingGround = False

menuBg = pygame.image.load(os.path.join("images", "bg.png"))
logo = pygame.image.load(os.path.join("images", "logo.png"))

player_size = 100

clock = pygame.time.Clock()

play = Button(screen, "PLAY", pygame.Color(255, 255, 255), ((screen.get_width() / 2) - 250, 500), 500, 100)

playerImg = loaders.Image.Load("player.png")
player_rect = playerImg.get_rect()

ground_img = loaders.Image.Load("ground.png")
ground_rect = ground_img.get_rect()

groundHeight = ground_img.get_height() # orig: 100

bg = loaders.Image.Load("bg.png")
bg_rect = ground_img.get_rect()

pygame.mixer.init()
gameBg = pygame.mixer.music.load(os.path.join("sounds", "music", "bg_mystery_night.mp3"))

fpsFont = pygame.font.Font(pygame.font.get_default_font(), 16)
exitFont = pygame.font.Font(pygame.font.get_default_font(), 32)

fps = 120
heldFrames = 0

exitAlpha = 255

def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    if 'pdb' in sys.modules:
        return True
    elif 'IPython' in sys.modules:
        return True
    elif 'pydevd' in sys.modules:
        return True
    elif 'ptvsd' in sys.modules:
        return True
    elif 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
        return True
    return False

DEBUG = False
# if true, enables debugging features
# these include free camera movement
# (maybe) visualisers of special stuff
if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        DEBUG = True
#if debugger_is_active():
    #DEBUG = True

class coord:
    x:int
    y:int

    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

camera = {
    "x": 0,
    "y": 0,
    "zoom": 1
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
    color:pygame.typing.ColorLike = "#2c0070"
    width = 500
    height = 250

    def __init__(self, x : int, y : int, color:pygame.typing.ColorLike = "#2c0070", width = 400, height = 100):
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
                    url = f"https://github.com/{username}/{repo}/releases/latest"
                    #print(url)
                    webbrowser.open(url)
                    return

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

musicLooping = True
musicPlaying = False

def changeScene(name):
    global scene
    alpha = 0
    fadeDuration = 500 # idk what this is in.. ;-;
    fading = True
    while fading:
        newSurf = pygame.Surface(size)
        newSurf.fill("black")
        newSurf.set_alpha(alpha)
        screen.blit(newSurf)
        alpha += 255 / fadeDuration
        if alpha >= 255:
            fading = False
    scene = name
    if name == "Game":
        loops = 0
        if musicLooping:
            loops = -1
        if shouldAudioPlay:
            pygame.mixer.music.play(loops)
            global musicPlaying
            musicPlaying = True

mouseScrollDelta = 1

fullscreened = False

prevWIndowSize = actualWindowSize

shouldAudioPlay = True

debugStrCaption = ""
if DEBUG:
    debugStrCaption = " [DEBUG]"

shotSurf:pygame.Surface

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.WINDOWFOCUSGAINED:
            focused = True
            if musicPlaying and shouldAudioPlay:
                loops = 0
                if musicLooping:
                    loops = -1
                pygame.mixer.music.play(loops)
        if e.type == pygame.WINDOWFOCUSLOST:
            focused = False
            if musicPlaying and shouldAudioPlay:
                pygame.mixer.music.pause()
        if e.type == pygame.MOUSEWHEEL:
            mouseScrollDelta = e.y
    if focused:
        if not fullscreened:
            actualWindowSize = pygame.display.get_window_size()
        justPressedKeys = pygame.key.get_just_pressed()
        if justPressedKeys[pygame.K_F2]:
            if not os.path.exists("screenshots"):
                os.mkdir("screenshots")
            now = datetime.datetime.now()
            pathScreenshot = f"screenshots/screenshot {now.day}-{now.month}-{now.year} {now.hour}-{now.minute}-{now.second}.png"
            pygame.image.save(screen, pathScreenshot)
            logger.message(f"Saved your screenshot to {pathScreenshot}")
            scaledownby = 4
            shotSurf = pygame.transform.scale(screen, (int(size[0] / scaledownby), int(size[1] / scaledownby)))
        if justPressedKeys[pygame.K_f]:
            if not fullscreened:
                prevWIndowSize = actualWindowSize
                disp = pygame.display.get_desktop_sizes()[0]
                size = disp
                actualWindowSize = disp
            else:
                size = (1280, 720)
                actualWindowSize = prevWIndowSize
            fullscreened = not fullscreened
            pygame.display.toggle_fullscreen()
        screen.fill("black")
        pygame.display.set_caption(f"{gameTitle} - {scene}{debugStrCaption}")
        if scene == "MainMenu":
            screen.blit(menuBg, (0, 0))
            logCentered = ScreenCenter(screen, logo, "x")
            logCentered.y = 100
            screen.blit(logo, (logCentered.x, logCentered.y))
            #pygame.draw.rect(screen, "white", ((screen.get_width() / 2) - 250, 500, 500, 100))
            
            play.draw()
            if play.onPressed:
                changeScene("Game")
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
                if DEBUG:
                    pygame.draw.rect(screen, "white", (player.x, window["height"] - player.y, player_size, player_size))
                screen.blit(playerImg, (player.x - camera["x"] - sceneOff["x"], window["height"] - player.y - camera["y"] - sceneOff["y"]))
                #pygame.draw.rect(screen, "blue", (player.x - camera["x"] - sceneOff["x"], window["height"] - player.y - camera["y"] - sceneOff["y"], player_size, player_size)) # draw player
                # pygame.draw.rect(screen, "red", (0, window["height"] - groundHeight, window["width"], groundHeight))
                groundX = ScreenCenter(screen, ground_img, "x").x
                screen.blit(ground_img, (groundX - camera["x"] - sceneOff["x"], window["height"] - groundHeight - camera["y"] - sceneOff["y"]))

                player.velocity -= player.gravity * static_values.deltatime
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
                    if DEBUG:
                        pygame.draw.rect(screen, "white", (g.x, g.y, g.width, g.height))
                    pygame.draw.rect(screen, g.color, (g.x - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], g.width, g.height))
                    if DEBUG:
                        scaleDots = 10
                        print(f"{((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and (player.y > g.y and player.y < g.y + g.height)} for {i}")
                        pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots + 6, scaleDots + 6))
                        pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                        pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                        pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                    if (player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width:
                        if DEBUG:
                            scaleDots = 20
                            pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots + 6, scaleDots + 6))
                            pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                            pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                            pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                        #if player.x + player_size > g.x:
                        print(f"{i} is {player.y > g.y and player.y < g.y + g.height}")
                        if player.y > g.y and player.y < g.y + g.height:
                            if DEBUG:
                                scaleDots = 30
                                pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots + 6, scaleDots + 6))
                                pygame.draw.rect(screen, "white", (g.x - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                                pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y + g.height - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                                pygame.draw.rect(screen, "white", (g.x + g.width - camera["x"] - sceneOff["x"], g.y - camera["y"] - sceneOff["y"], scaleDots, scaleDots))
                            print(f"collision detecting platform {i}")
                            logger.message("touching box :D")
                            player.y -= player.velocity
                            if playerMovesCamera:
                                camera["y"] += player.velocity
                            player.velocity = 0
                            touchingGround = True
                        print(f"did it even get here??? for {i}")
                    i += 1
                #print(touchingGround)
                keys = pygame.key.get_pressed()
                if keybinds.GetKeysPressed(keybinds.jump) and touchingGround:
                    if not jumpJustPressed:
                        player.velocity = jumpHeight * static_values.deltatime
                        jumpJustPressed = True
                else:
                    jumpJustPressed = False
                if keybinds.GetKeysPressed(keybinds.move_left):
                    player.x -= player.speed * static_values.deltatime
                    if playerMovesCamera:
                        camera["x"] -= player.speed * static_values.deltatime
                if keybinds.GetKeysPressed(keybinds.move_right):
                    player.x += player.speed * static_values.deltatime
                    if playerMovesCamera:
                        camera["x"] += player.speed * static_values.deltatime
                gobjedhwIDX = 0
                for g in objects:
                    if DEBUG:
                        print(player.y < g.y or player.y + player_size > g.y)
                    print(gobjedhwIDX)
                    # (player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width
                    #(player.x + player_size > g.x or player.x < g.x + g.width) and (player.y < g.y or player.y + player_size > g.y)
                    if ((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and ((player.y > g.y and player.y < g.y + g.height) or ((player.y < g.y + g.height and player.y < g.y + g.height))):
                    #if player.x > g.x and player.x < g.x + g.width:
                            logger.message("horizontal collision! :D")
                            player.x -= player.speed * static_values.deltatime
                            if playerMovesCamera:
                                camera["x"] -= player.speed * static_values.deltatime
                            if ((player.x > g.x or player.x + player_size > g.x) and player.x < g.x + g.width) and ((player.y > g.y and player.y < g.y + g.height) or ((player.y < g.y + g.height and player.y < g.y + g.height))):
                                player.x += player.speed * static_values.deltatime * 2 # move out to compensate
                                if playerMovesCamera:
                                    camera["x"] += player.speed * static_values.deltatime * 2
                    gobjedhwIDX += 1
                if DEBUG:
                    if keys[pygame.K_p]:
                        player.gravity += 0.01
                    if keys[pygame.K_SEMICOLON]:
                        player.gravity -= 0.01
                    if keys[pygame.K_j]:
                        camera["x"] -= player.speed * static_values.deltatime
                    if keys[pygame.K_l]:
                        camera["x"] += player.speed * static_values.deltatime
                    if keys[pygame.K_i]:
                        camera["y"] -= player.speed * static_values.deltatime
                    if keys[pygame.K_k]:
                        camera["y"] += player.speed * static_values.deltatime
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
                    if heldFrames == 3 * fps:
                        running = False
                    heldFrames += 1
                    logger.message(f"exitAlpha: {10 / (3 * fps)}")
                    # math.ceil(100 / (5 * fps)) # thrown here in case you wanna use it. i couldnt figure it out
                    exitAlpha -= 1
                    if exitAlpha < 0:
                        exitAlpha = 0 # alpha cant be negative because... duh
                    logger.message(f"exitAlpha: {exitAlpha}")
                else:
                    heldFrames = 0
                    exitAlpha = 255
                #shader.render(display) #Render the display onto the OpenGL display with the shaders!
                # buggy camera zoom feature, error: invalid rectstyle argument
                #if DEBUG:
                #    camera["zoom"] += mouseScrollDelta
                #zoomed = screen.subsurface((size[0] * camera["zoom"], size[1] * camera["zoom"]))
                #screen.blit(pygame.transform.scale(camera["zoom"], size))
                #if not actualWindowSize == size:
                #    scaled = pygame.transform.scale(screen, size)
                #    screen.fill("black")
                #    screen.blit(scaled, ((actualWindowSize[0] / 2) - (size[0] / 2), (actualWindowSize[1] / 2) - (size[1] / 2)))
                #pygame.display.flip()
            except Exception as e:
                logger.crash(e)
                running = False
        try:
            alphaShot = shotSurf.get_alpha()
            print(alphaShot)
            #borderSize = 5
            #pygame.draw.rect(shotSurf, "white", (0, 0, shotSurf.get_width() + borderSize, shotSurf.get_height() + borderSize))
            if not alphaShot == 0 and not alphaShot == None:
                alphaShot -= 1
            elif alphaShot == None:
                alphaShot = 255
            elif alphaShot == 0:
                shotSurf = None # shouldnt blit a screenshot thats already faded
            shotSurf.set_alpha(alphaShot)
            screen.blit(shotSurf)
        except:
            # just dont blit it. we probably removed the screenshot by now.. or we havent taken a screenshot yet
            pass
        pygame.display.flip()
    static_values.deltatime = clock.tick(fps) / 1000

pygame.quit()