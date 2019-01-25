# Game's initialisation : get the config, create the window, create gameManager, and init openGL / glfw

from game.main import config as Config
import time
import OpenGL.GL as gl
import glfw

SECOND = 1000000
TPS = 60.0
TICK_TIME = SECOND / TPS
beginTime = 0
ratio = 0

def init():
	Config.check()
	Config.load()
	beginTime = time.time()

	# Initializing GLFW
	if not glfw.init():
		exit()

	create() # the window

	from game.screen import gameManager as gm
	global gameManager
	gameManager = gm.GameManager()


def create():
	global window

	glfw.default_window_hints()
	glfw.window_hint(glfw.RESIZABLE, 0) # 0 = false

	window = glfw.create_window(Config.width, Config.height, "Coop Dungeon Adventure", None, None)

	if not window:
		glfw.terminate()
		exit()

	glfw.make_context_current(window)	
		
	if Config.limFrameRate:
		glfw.swap_interval(1)
	else:
		glfw.swap_interval(0)
	
	gl.glViewport(0, 0, Config.width, Config.height);

	gl.glEnable(gl.GL_TEXTURE_2D)
	gl.glActiveTexture(gl.GL_TEXTURE0)
	gl.glEnable(gl.GL_BLEND)
	gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)	
	gl.glMatrixMode(gl.GL_PROJECTION)
	gl.glMatrixMode(gl.GL_MODELVIEW)
	gl.glEnable(gl.GL_DEPTH_TEST)
    # Enable Anti-aliasing
	gl.glEnable(gl.GL_MULTISAMPLE)


def run():
	loop()
	exit()


def loop():
	gl.glClearColor(0.05, 0.05, 0.05, 1.0) 	# Black color

	ticks = 0
	frames = 0

	from datetime import datetime

	frameTime = datetime.now().microsecond
	secondTime = datetime.now().microsecond

	lag = 0.0

	while not glfw.window_should_close(window):
		lag += datetime.now().microsecond - frameTime
		frameTime = datetime.now().microsecond
		print(frameTime)

		if datetime.now().microsecond - secondTime >= SECOND:
			if Config.debug:
				glfw.set_window_title(window, "Coop Dungeon Adventure | FPS:" + str(frames) + "; TPS:" + str(ticks))
			ticks = 0
			frames = 0
			secondTime = datetime.now().microsecond

		while lag >= TICK_TIME:
			gameManager.update()

			lag -= TICK_TIME
			ticks +=1

		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

		gameManager.display()
		frames += 1
		
		glfw.swap_buffers(window)
		glfw.poll_events()			


def exit():
	Config.close()
	gameManager.unload()
	glfw.terminate()
