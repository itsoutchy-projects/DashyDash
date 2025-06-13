import datetime
import os
from tkinter import messagebox
import pathlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

log = ""
colours = {
    "info": bcolors.OKBLUE,
    "warn": bcolors.WARNING,
    "error": bcolors.FAIL
}


def message(msg : str):
    global log
    res = f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] MESSAGE: {msg}"
    log += res + "\n"
    print(res.replace("MESSAGE", f"{colours['info']}MESSAGE{bcolors.ENDC}"))

def error(msg : str):
    global log
    res = f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] ERROR: {msg}"
    log += res + "\n"
    print(res.replace("ERROR", f"{colours['error']}ERROR{bcolors.ENDC}"))

def warn(msg : str):
    global log
    res = f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] WARN: {msg}"
    log += res + "\n"
    print(res.replace("WARN", f"{colours['warn']}WARN{bcolors.ENDC}"))

def write():
    global log
    if log != "" and log != "\n": # we dont need to write a blank log. only write one if its necessary
        if not os.path.exists("logs"):
            os.mkdir("logs")
        with open(os.path.join("logs", str(len(os.listdir("logs")) + 1)), "x") as f:
            f.write(log)

def crash(err : Exception):
    error(err)
    write()
    messagebox.showerror("Fatal Error", f"{err}\n\nYour logs are in: {os.path.join(str(pathlib.Path(__file__).parent), "logs")}")