# Check, load and save the config (path)

# Default value to prevent a mistake of configs's loading
CONFIG_PATH = "data/config/config.json"
INPUTS_PATH = "data/config/inputs.json"


def check():
	import os

	# Verification of the existence of the "data" folder
	path = "data"
	if not(os.path.exists(path)) and not(os.path.isdir(path)):
		print("Creating '%s' folder..." % path)
		try:
			os.mkdir(path)
		except OSError:  
			print("Creation of the directory %s failed" % path)
			exit()

	# Verification of the existence of the "data/config" folder
	path = "data/config"
	if not(os.path.exists(path)) and not(os.path.isdir(path)):
		print("Creating '%s' folder..." % path)
		try:
			os.mkdir(path)
		except OSError:  
			print("Creation of the directory %s failed" % path)
			exit()

	# Verification of the existence of the user-specific config file
	path = CONFIG_PATH
	if not(os.path.exists(path)):
		print("Copying original config to new one...")
		import shutil
		try:
			shutil.copyfile('game/resources/config/originalConfig.json', path)
		except FileNotFoundError:
			print("Can't find original config file !")
			exit()

	# Verify the existence of the user-specific key config file
	path = INPUTS_PATH
	if not(os.path.exists(path)):
		print("Copying original key config file to new one...")
		import shutil
		try:
			shutil.copyfile('game/resources/config/originalInputs.json', path)
		except FileNotFoundError:
			print("Can't find original key config file !")
			exit()


def load():
	global debug, width, height, ratio, fullScreen, limFrameRate, inputs, language, noiseVolume, musicVolume
	# Default Values
	debug = True
	width = 1152
	height = 200
	ratio = width / height
	fullScreen = False
	limFrameRate = False
	ratio = 1
	inputs = []
	language = "en"
	noiseVolume = 0.0
	musicVolume = 0.0

	check()
	from game.util import reader as Reader
	Reader.loadConfig() 
	ratio = width / height
			

def close():
	pass
	# TODO: implements
