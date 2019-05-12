# main file of the game, start the window

from game.main.window import Window

Window.init()

try:
	Window.run()
except KeyboardInterrupt:
	Window.exit()
