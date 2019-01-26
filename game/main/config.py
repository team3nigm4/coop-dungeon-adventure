# Check, load and save the config (path)


class Config:
	# Default value to prevent a mistake of configs's loading
	CONFIG_PATH = "data/config/config.json"
	INPUTS_PATH = "data/config/inputs.json"

	debug = None
	width = None
	height = None
	ratio = None
	fullScreen = None
	limFrameRate = None
	inputs = None
	language = None
	noiseVolume = None
	musicVolume = None

	@staticmethod
	def check():
		import os

		# Verification of the existence of the "data" folder
		path = "data"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			print("Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
			except OSError:
				print("Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the "data/config" folder
		path = "data/config"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			print("Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
			except OSError:
				print("Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the user-specific config file
		path = Config.CONFIG_PATH
		if not (os.path.exists(path)):
			print("Copying original config to new one...")
			import shutil
			try:
				shutil.copyfile('game/resources/config/originalConfig.json', path)
			except FileNotFoundError:
				print("Can't find original config file !")
				exit()

		# Verify the existence of the user-specific key config file
		path = Config.INPUTS_PATH
		if not (os.path.exists(path)):
			print("Copying original key config file to new one...")
			import shutil
			try:
				shutil.copyfile('game/resources/config/originalInputs.json', path)
			except FileNotFoundError:
				print("Can't find original key config file !")
				exit()

	@staticmethod
	def load():
		Config.check()
		from game.util import reader as Reader
		Reader.loadConfig()
		Config.ratio = Config.width / Config.height
		Config.debug = True

	@staticmethod
	def close():
		pass
# TODO: implements
