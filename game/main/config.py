# Check, load and save the config (path)

from sys import exit

from game.util.logger import Logger

class Config:
	# Default value to prevent a mistake of configs's loading
	CONFIG_PATH = "data/config/config.json"
	INPUTS_PATH = "data/config/inputs.json"

	debug = None
	ratio = None
	inputs = None
	values = None

	@staticmethod
	def check():
		import os

		# Verification of the existence of the "data" folder
		path = "data"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			Logger.info("Config", "Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
				Logger.success("Config", "Done !")
			except OSError:
				Logger.error("Config", "Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the "data/config" folder
		path = "data/config"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			Logger.info("Config", "Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
				Logger.success("Config", "Done !")
			except OSError:
				Logger.error("Config", "Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the user-specific config file
		path = Config.CONFIG_PATH
		if not (os.path.exists(path)):
			Logger.info("Config", "Creating the user-specific configuration file...")
			Config.createDefaultConfig()

		# Verification of the existence of the user-specific key config file
		path = Config.INPUTS_PATH
		if not (os.path.exists(path)):
			Logger.info("Config", "Creating the user-specific key configuration file...")
			Config.createDefaultInputs()

	@staticmethod
	def load():
		Config.check()
		Config.loadConfig()
		Config.loadInputs()
		Config.ratio = Config.values["window"]["width"] / Config.values["window"]["height"]
		Config.debug = True

	@staticmethod
	def createDefaultConfig(overwrite=True):

		# We retrieve the user's screen resolution
		width = 0
		height = 0
		import glfw
		glfw.init()
		vm = glfw.get_video_modes(glfw.get_primary_monitor())
		nvm = len(vm) - 1
		monitorResolution = [vm[nvm][0][0], vm[nvm][0][1]]
		# We choose the highest resolution that can support the screen
		baseResolution = [576, 384]  # The minimum game display resolution
		for factor in range(1, 10):
			if (baseResolution[0] * factor < monitorResolution[0] and baseResolution[1] * factor < monitorResolution[
				1]): width = baseResolution[0] * factor; height = baseResolution[1] * factor

		# We retrieve the user's locale
		import locale
		userLanguage = locale.getdefaultlocale()[0][:2]
		languages = [['en', 'English'], ['fr', 'Français']]
		language = "en"
		# We choose the locale if present in the game, otherwise, we take the default one (English)
		for lang in languages:
			if lang[0] == userLanguage: language = lang[0]

		Config.values = {
			"general": {
				"language": language
			},
			"window": {
				"limFrameRate": 0,
				"fullScreen": 0,
				"width": width,
				"height": height
			},
			"audio": {
				"musicVolume": 0.5,
				"soundsVolume": 0.5
			}
		}

		if overwrite:
			Config.saveConfig()

	@staticmethod
	def createDefaultInputs(overwrite=True):

		Config.inputs = {
			"ECHAP": [[0, 256]],
			"RESET": [[0, 82]],
			"GO_LEFT_0": [[0, 65]],
			"GO_UP_0": [[0, 87]],
			"GO_RIGHT_0": [[0, 68]],
			"GO_DOWN_0": [[0, 83]],
			"INTERACT_0": [[0, 340]],
			"ITEM_0": [[0, 32]],
			"ITEM2_0": [[0, 70]],
			"GO_LEFT_1": [[0, 263]],
			"GO_UP_1": [[0, 265]],
			"GO_RIGHT_1": [[0, 262]],
			"GO_DOWN_1": [[0, 264]],
			"INTERACT_1": [[1, 1]],
			"ITEM_1": [[1, 0]],
			"ITEM2_1": [[0, 345]],
		}

		if overwrite:
			Config.saveInputs()

	@staticmethod
	def saveConfig():
		import json

		ConfigToSave = {
			"config": Config.values
		}

		with open(Config.CONFIG_PATH, 'w') as outfile:
			json.dump(ConfigToSave, outfile, indent="	")
			Logger.success("Config", "Configuration file saved successfully !")

	@staticmethod
	def saveInputs():
		import json

		InputsToSave = {
			"inputs": Config.inputs
		}

		with open(Config.INPUTS_PATH, 'w') as outfile:
			json.dump(InputsToSave, outfile, indent="	")
			Logger.success("Config", "Key configuration file saved successfully !")

	@staticmethod
	def loadConfig():
		import json
		try:
			configFile = json.load(open(Config.CONFIG_PATH))['config']
			Config.values = configFile
		except json.decoder.JSONDecodeError:
			Config.createDefaultConfig(Config.yes(Logger.format("Config", "Failed to parse the config file ! Do you want to recreate it and delete the old one ?")))

	@staticmethod
	def loadInputs():
		import json
		try:
			inputsFile = json.load(open(Config.INPUTS_PATH))['inputs']
			Config.inputs = inputsFile
		except json.decoder.JSONDecodeError:
			Config.createDefaultInputs(Config.yes(Logger.format("Config", "Failed to parse the key config file ! Do you want to recreate it and delete the old one ?")))

	@staticmethod
	def yes(sentence):
		choice = input(sentence + " (Answer \"yes\") : ").lower()
		if choice == "yes":
			return True
		else:
			return False
