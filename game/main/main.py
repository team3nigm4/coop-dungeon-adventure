# main file of the game

from game.main.window import Window

Window.init()

try:
	Window.run()
except KeyboardInterrupt:
	Window.exit()
