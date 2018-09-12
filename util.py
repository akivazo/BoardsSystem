
from keyboard import is_pressed
from os import path
from time import sleep
import logging


def logError(errorInst):
	logging.exception(errorInst)
	
	
def findPath(file):
    return path.dirname(path.abspath(__file__)) + "//" + file

def wait(t):
    sleep(t)
    pass


def openFile(file, mode):
    dir = path.dirname(path.abspath(__file__))
    return open(findPath(file), mode=mode)

def checkForkey(key):
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if is_pressed(key):  # if key 'q' is pressed
                return True
            else:
                return False
        except:
            break  # if user pressed a key other than the given key the loop will break


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


