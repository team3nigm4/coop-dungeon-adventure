# Check, load and save the config (path)


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
			print("[CONFIG] Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
			except OSError:
				print("[CONFIG] Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the "data/config" folder
		path = "data/config"
		if not (os.path.exists(path)) and not (os.path.isdir(path)):
			print("[CONFIG] Creating '%s' folder..." % path)
			try:
				os.mkdir(path)
			except OSError:
				print("[CONFIG] Creation of the directory %s failed" % path)
				exit()

		# Verification of the existence of the user-specific config file
		path = Config.CONFIG_PATH
		if not (os.path.exists(path)):
			print("[CONFIG] Creating the user-specific configuration file...")
			Config.createDefaultConfig()

		# Verification of the existence of the user-specific key config file
		path = Config.INPUTS_PATH
		if not (os.path.exists(path)):
			print("[CONFIG] Creating the user-specific key configuration file...")
			Config.createDefaultInputs()

	@staticmethod
	def load():
		Config.check()
		Config.loadConfig()
		Config.loadInputs()
		Config.ratio = Config.values["window"]["width"] / Config.values["window"]["height"]
		Config.debug = True

	@staticmethod
	def createDefaultConfig(overwrite = True):

		# We retrieve the user's screen resolution
		import glfw; glfw.init(); vm = glfw.get_video_modes(glfw.get_primary_monitor()); nvm = len(vm)-1; monitorResolution = [vm[nvm][0][0], vm[nvm][0][1]]
		# We choose the highest resolution that can support the screen
		baseResolution = [576, 384]  # The minimum game display resolution
		for factor in range(1, 10):
			if (baseResolution[0]*factor < monitorResolution[0] and baseResolution[1]*factor < monitorResolution[1]): width = baseResolution[0]*factor; height = baseResolution[1]*factor

		# We retrieve the user's locale
		import locale; userLanguage = locale.getdefaultlocale()[0][:2]; languages = [['en', 'English'], ['fr', 'Français']]; language = "en"
		# We choose the locale if present in the game, otherwise, we take the default one (English)
		for lang in languages:
			if lang[0] == userLanguage: language = lang[0]

		Config.values =  {
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

		if overwrite == True:
			Config.saveConfig()

	@staticmethod
	def createDefaultInputs(overwrite = True):

		Config.inputs = [[0, 256], [0, 81], [0, 87], [0, 65], [0, 68], [1, 1], [1, 0], [0, 70], [0, 82]]

		if overwrite == True:
			Config.saveInputs()

	@staticmethod
	def saveConfig():
		import json

		ConfigToSave = {
			"config": Config.values
		}

		with open(Config.CONFIG_PATH, 'w') as outfile:
			json.dump(ConfigToSave, outfile, indent="	")
			print("[CONFIG] Default configuration file created successfully !")

	@staticmethod
	def saveInputs():
		import json

		InputsToSave = {
			"inputs": Config.inputs
		}

		with open(Config.INPUTS_PATH, 'w') as outfile:
			json.dump(InputsToSave, outfile, indent="	")
			print("[CONFIG] Default key configuration file created successfully !")

	@staticmethod
	def loadConfig():
		import json
		try:
			configFile = json.load(open(Config.CONFIG_PATH))['config']
			Config.values = configFile
		except json.decoder.JSONDecodeError:
			Config.createDefaultConfig(Config.yes("[CONFIG] Failed to parse the config file ! Do you want to recreate it and delete the old one ?"))

	@staticmethod
	def loadInputs():
		import json
		try:
			inputsFile = json.load(open(Config.INPUTS_PATH))['inputs']
			Config.inputs = inputsFile
		except json.decoder.JSONDecodeError:
			Config.createDefaultInputs(Config.yes("[CONFIG] Failed to parse the key config file ! Do you want to recreate it and delete the old one ?"))

	@staticmethod
	def yes(sentence):
		choice = input(sentence + " (Answer \"yes\") : ").lower()
		if choice == "yes":
		   return True
		else:
			return False