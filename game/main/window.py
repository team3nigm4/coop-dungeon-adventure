# Game's initialisation : get the config, create the window, create gameManager, and init openGL / glfw

import time
import OpenGL.GL as gl
import glfw
import colorama
import sys
from PIL import Image 

from game.util.logger import Logger 
from game.main.config import Config
from game.screen import gamemanager as gm

class Window:
	SECOND = 1000000000
	TPS = 60.0
	TICK_TIME = SECOND / TPS
	beginTime = 0
	frame = 0


	# Sort of id of the window
	# We use this "id" to get the inputs state and do other things related to glfw
	window = None

	@staticmethod
	def init():
		colorama.init()
		Logger.info("Game", "Started")
		print("")
		Config.load()
		Window.beginTime = time.time()

		# Initializing GLFW
		if not glfw.init():
			Logger.error("GLFW", "Failed to init GLFW")
			exit()

		Window.create()  # the window

		# Init game manager
		gm.GameManager.init()

	@staticmethod
	def create():
		glfw.default_window_hints()
		glfw.window_hint(glfw.RESIZABLE, 0)  # 0 = false

		Window.window = glfw.create_window(Config.values["window"]["width"], Config.values["window"]["height"], "Coop Dungeon Adventure", None, None)

		if not Window.window:
			glfw.terminate()
			sys.exit(2)
			
		glfw.make_context_current(Window.window)
		glfw.set_window_icon(Window.window, 1, Image.open("game/resources/icon.png"))

		if Config.values["window"]["limFrameRate"]:
			glfw.swap_interval(1)		# max frame rate of the monitor
		else:
			glfw.swap_interval(0)		# No frame limit
		
		# Hints for OpenGL
		gl.glViewport(0, 0, Config.values["window"]["width"], Config.values["window"]["height"])
		gl.glEnable(gl.GL_TEXTURE_2D)
		gl.glActiveTexture(gl.GL_TEXTURE0)
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

	@staticmethod
	def run():
		Window.loop()
		Window.exit()
	
	# Start the main loop of the game
	@staticmethod
	def loop():
		gl.glClearColor(0.05, 0.05, 0.05, 1.0)  # Black color

		ticks = 0
		frames = 0

		frameTime = time.time_ns()
		secondTime = time.time_ns()

		lag = 0.0
		
		# This clock system enticipate lags
		while not glfw.window_should_close(Window.window):
			lag += time.time_ns() - frameTime
			frameTime = time.time_ns()

			gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT) # Clear the window

			if time.time_ns() - secondTime >= Window.SECOND:
				if Config.values["general"]["debug"]:
					glfw.set_window_title(Window.window,
										  "Coop Dungeon Adventure | FPS:" + str(frames) + "; TPS:" + str(ticks))
				ticks = 0
				frames = 0
				secondTime = time.time_ns()

			while lag >= Window.TICK_TIME:
				gm.GameManager.update()							# Update()

				lag -= Window.TICK_TIME
				ticks += 1

			gm.GameManager.display()							# Display()
			frames += 1
			
			glfw.swap_buffers(Window.window)
			glfw.poll_events()
			
			Window.frame += 1
			Logger.setFrame(Window.frame)

	@staticmethod
	def exit():
		gm.GameManager.unload()
		glfw.terminate()
		print("")
		Logger.info("Game", "Closed")
		sys.exit()
