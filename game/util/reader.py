# This file loads the config and input files

import game.main.config as Config

import json


def loadConfig():
	configFile = json.load(open(Config.CONFIG_PATH))['config']

	Config.language = configFile['general']['language']

	Config.width = configFile['window']['width']
	Config.height = configFile['window']['height']
	Config.ratio = Config.width / Config.height
	Config.fullScreen = configFile['window']['fullscreen']
	Config.limFrameRate = configFile['window']['framerate']

	Config.musicVolume = configFile['audio']['music']/100
	Config.soundsVolume = configFile['audio']['sounds']/100

	Config.inputs = json.load(open(Config.INPUTS_PATH))["inputs"]
