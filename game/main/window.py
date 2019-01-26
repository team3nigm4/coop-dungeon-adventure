# Game's initialisation : get the config, create the window, create gameManager, and init openGL / glfw

import time

import OpenGL.GL as gl
import glfw

from game.main.config import Config


class Window:
	SECOND = 1000000000
	TPS = 60.0
	TICK_TIME = SECOND / TPS
	beginTime = 0

	window = None

	@staticmethod
	def init():
		Config.load()
		Window.beginTime = time.time()

		# Initializing GLFW
		if not glfw.init():
			exit()

		Window.create()  # the window

		from game.screen import gamemanager as gm
		global gameManager
		gameManager = gm.GameManager()

	@staticmethod
	def create():
		glfw.default_window_hints()
		glfw.window_hint(glfw.RESIZABLE, 0)  # 0 = false

		Window.window = glfw.create_window(Config.values["window"]["width"], Config.values["window"]["height"],
										   "Coop Dungeon Adventure", None, None)

		if not Window.window:
			glfw.terminate()
			exit()

		glfw.make_context_current(Window.window)

		if Config.values["window"]["limFrameRate"]:
			glfw.swap_interval(1)
		else:
			glfw.swap_interval(0)

		gl.glViewport(0, 0, Config.values["window"]["width"], Config.values["window"]["height"])

		gl.glEnable(gl.GL_TEXTURE_2D)
		gl.glActiveTexture(gl.GL_TEXTURE0)
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glEnable(gl.GL_DEPTH_TEST)
		# Enable Anti-aliasing
		gl.glEnable(gl.GL_MULTISAMPLE)

	@staticmethod
	def run():
		Window.loop()
		Window.exit()

	@staticmethod
	def loop():
		gl.glClearColor(0.05, 0.05, 0.05, 1.0)  # Black color

		ticks = 0
		frames = 0

		frameTime = time.time_ns()
		secondTime = time.time_ns()

		lag = 0.0
		while not glfw.window_should_close(Window.window):
			lag += time.time_ns() - frameTime
			frameTime = time.time_ns()

			if time.time_ns() - secondTime >= Window.SECOND:
				if Config.debug:
					glfw.set_window_title(Window.window,
										  "Coop Dungeon Adventure | FPS:" + str(frames) + "; TPS:" + str(ticks))
				ticks = 0
				frames = 0
				secondTime = time.time_ns()

			while lag >= Window.TICK_TIME:
				gameManager.update()

				lag -= Window.TICK_TIME
				ticks += 1

			gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

			gameManager.display()
			frames += 1

			glfw.swap_buffers(Window.window)
			glfw.poll_events()

	@staticmethod
	def exit():
		gameManager.unload()
		glfw.terminate()
