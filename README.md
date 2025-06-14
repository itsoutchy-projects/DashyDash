# DashyDash
A simple platformer game made fully in Python using PyGame-ce

> [!WARNING]
> This game is in BETA, so it has no official releases yet, you can download this code and test it yourself, but it does have bugs (mainly collision but still)

## How to use
This game is made in Python, so all you really have to do is install python and run [Get Dependencies.sh](Get%20Dependencies.sh). This will help you download the dependencies automatically.

You can just play it using the copy of Python you installed earlier, but if you want to make a binary, read more.

Start off by running the command below:
```
pyinstaller game.py
```

This'll make a binary, but it (probably) wont have the images, so next, head into the `game.spec` file that pyinstaller made.
(first, check by attempting to run the game binary, if it fails or crashes, proceed to the steps ahead)

Next, add:
```python
addedfiles = [
    ("images", "images"),
    ("version.txt", ".")
]
```

Then finally, under `a = Analysis()`, find the line `datas=[]`, replace it with:
```python
datas=addedfiles
```

## KNOWN BUGS
- [ ] Only first platform is collideable
  - Might need some extra help with this one, been going at this for AGES