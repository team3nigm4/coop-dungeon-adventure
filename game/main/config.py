# Class to create, check, load and save the differents configurations

from sys import exit
import json

from game.util.logger import Logger

class Config:
	
	# Set the different paths of configuration files
	DATA_FOLDER = "data"
	MAIN_CONFIG_PATH = "data/config/config.json"
	KEYBOARD_CONFIG_PATH = "data/config/inputs.json"
	SERVER_CONFIG_PATH = "data/server.json"

	ratio = 0
	server = []
	inputs = {}
	values = {}

	@staticmethod
	def check():
		
		import os

		# Check if the "data" folder exists (and create it if necessary)
		path = Config.DATA_FOLDER
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			Logger.info("Config", "Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
				Logger.success("Config", "Done !")
			except OSError:
				Logger.error("Config", "Creation of the directory %s failed" % path)
				exit()

		# Check if the "data/config" folder exists (and create it if necessary) 
		path = Config.DATA_FOLDER + "/config"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			Logger.info("Config", "Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
				Logger.success("Config", "Done !")
			except OSError:
				Logger.error("Config", "Creation of the directory %s failed" % path)
				exit()

		# Check if the main configuration file exists (and create it if necessary)
		path = Config.MAIN_CONFIG_PATH
		if not (os.path.exists(path)):
			Logger.info("Config", "Creating the user-specific configuration file...")
			Config.createDefaultConfig()

		# Check if the keyboard configuration file exists (and create it if necessary)
		path = Config.KEYBOARD_CONFIG_PATH
		if not (os.path.exists(path)):
			Logger.info("Config", "Creating the user-specific key configuration file...")
			Config.createDefaultInputs()

	@staticmethod
	def checkServerConfig():
		
		import os

		# Check if the "data" folder exists (and create it if necessary) 
		path = Config.DATA_FOLDER
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			Logger.info("Config", "Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
				Logger.success("Config", "Done !")
			except OSError:
				Logger.error("Config", "Creation of the directory %s failed" % path)
				exit()

		# Check if the server configuration file exists (and create it if necessary) 
		path = Config.SERVER_CONFIG_PATH
		if not (os.path.exists(path)):
			Logger.info("Config", "A configuration file needs to be created to connect to the server")
			Config.createDefaultServerConfig()

	@staticmethod
	def load():
		Config.check()
		Config.loadConfig()
		Config.loadInputs()
		Config.ratio = Config.values["window"]["width"] / Config.values["window"]["height"]

	@staticmethod
	def loadServer():
		Config.checkServerConfig()
		Config.loadServerConfig()

	@staticmethod
	def createDefaultConfig(overwrite=True):

		# We retrieve the user's screen resolution using the GLFW library
		width = 576
		height = 384
		import glfw
		glfw.init()
		vm = glfw.get_video_modes(glfw.get_primary_monitor())
		nvm = len(vm) - 1
		monitorRes = [vm[nvm][0][0], vm[nvm][0][1]]
		
		# We choose the highest resolution that can support the screen
		baseRes = [576, 384]  # The minimum game display resolution (18 tiles * 32 pixels and 12 tiles * 32 pixels)
		for factor in range(1, 10): # Test differents zoom factors to find the maximum that can be used
			if (baseRes[0] * factor < monitorRes[0] and baseRes[1] * factor < monitorRes[1]):
				width = baseRes[0] * factor
				height = baseRes[1] * factor

		# We retrieve the user's locale
		import locale
		userLanguage = locale.getdefaultlocale()[0][:2]
		languages = [['en', 'English'], ['fr', 'Français']]
		language = "en"
		# We choose the locale if present in the game, otherwise, we take the default one (English)
		for lang in languages:
			if lang[0] == userLanguage: language = lang[0]

		# We set the values for the configuration
		Config.values = {
			"general": {
				"language": language,
				"debug": False
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

		# We overwrite the configuration if needed
		if overwrite: Config.saveConfig()

	
	@staticmethod
	def createDefaultInputs(overwrite=True):
		
		# We set default values for the keyboard configuration 
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

		# We overwrite the keyboard configuration if needed
		if overwrite: Config.saveInputs()

	@staticmethod
	def createDefaultServerConfig(overwrite=True):
		
		if Config.yes(Logger.format("Config", "Do you want to use the default server configuration ? ")):	
			# We set default values for the server configuration
			Config.server = {
				"ip": "127.0.0.1",
				"port": 34141
			}
		else :	
			# We ask for server configuration values
			Config.server = {
				"ip": input("[1/2] What is the IP or the domain name of the server ? "),
				"port": input("[2/2] On which port runs the server (by default, 34141) ? ")
			}

		# We overwrite the server configuration if needed
		if overwrite: Config.saveServerConfig()

	# Method to save the configuration into a file
	@staticmethod
	def saveConfig():

		ConfigToSave = {
			"config": Config.values
		}

		with open(Config.MAIN_CONFIG_PATH, 'w') as outfile:
			json.dump(ConfigToSave, outfile, indent="	")
			Logger.success("Config", "Configuration file saved successfully !")

	# Method to save the keyboard configuration into a file
	@staticmethod
	def saveInputs():

		InputsToSave = {
			"inputs": Config.inputs
		}

		with open(Config.KEYBOARD_CONFIG_PATH, 'w') as outfile:
			json.dump(InputsToSave, outfile, indent="	")
			Logger.success("Config", "Key configuration file saved successfully !")

	# Method to save the server configuration into a file
	@staticmethod
	def saveServerConfig():

		with open(Config.SERVER_CONFIG_PATH, 'w') as outfile:
			json.dump(Config.server, outfile, indent="	")
			Logger.success("Config", "Server configuration file saved successfully !")

	@staticmethod
	def loadConfig():
		
		try: # Try to load the configuration from file
			configFile = json.load(open(Config.MAIN_CONFIG_PATH))['config']
			Config.values = configFile
		except json.decoder.JSONDecodeError: # If it fails, ask for overwrite (or it will use a default configuration)
			Config.createDefaultConfig(Config.yes(Logger.format("Config", "Failed to parse the config file ! Do you want to recreate it and delete the old one ?")))

	@staticmethod
	def loadInputs():
		
		try: # Try to load the keyboard configuration from file
			inputsFile = json.load(open(Config.KEYBOARD_CONFIG_PATH))['inputs']
			Config.inputs = inputsFile
		except json.decoder.JSONDecodeError: # If it fails, ask for overwrite (or it will use a default keyboard configuration)
			Config.createDefaultInputs(Config.yes(Logger.format("Config", "Failed to parse the key config file ! Do you want to recreate it and delete the old one ?")))

	@staticmethod
	def loadServerConfig():
		
		try: # Try to load the server configuration from file
			Config.server = json.load(open(Config.SERVER_CONFIG_PATH))
		except json.decoder.JSONDecodeError: # If it fails, ask for overwrite (or it will use a default server configuration)
			Config.createDefaultServerConfig(Config.yes(Logger.format("Config", "Failed to parse the server config file ! Do you want to recreate it and delete the old one ?")))

	# Simple method that allow to ask questions to the user
	@staticmethod
	def yes(sentence):
		
		choice = input(sentence + " (Answer \"yes\") : ").lower()
		
		if choice == "yes":
			return True
		else:
			return False
