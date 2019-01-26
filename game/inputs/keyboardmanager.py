# Manages key states

from game.main import window
import glfw


def getKey(key):
	return glfw.get_key(window.window, key)

# TODO: create the keyboardManager's functions keyPressed and keyReleased
