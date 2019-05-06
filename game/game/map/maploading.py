# Import test map
import json
import os
from sys import exit

from game.util.logger import Logger

class MapLoading:

	@staticmethod
	def loadMap(zone, name):
		path = "game/resources/map/" + zone + "/" + name + ".json"

		try:
			getValues = json.load(open(path))

			returnValues = []
			returnValues.append([int(getValues["entries"]["default"]), int(getValues["map"]["events"])])

			returnValues.append(getValues["collision"][0])
			returnValues.append(getValues["entries"])

			returnValues.append(getValues["entities"][0])

			returnValues.append(getValues["layers"])

			returnValues.append(getValues["map"]["tileset"])

			return returnValues
		except json.decoder.JSONDecodeError:
			Logger.error("MapLoading", "Can't load the map " + path)
			exit()

	@staticmethod
	def isMap(zone, map, entry):
		path = "game/resources/map/" + zone + "/" + map + ".json"
		state = os.path.isfile(path)
		if not state:
			Logger.error("MapLoading", "The map : " + str(map) + " in zone: " + str(zone) + " doesn't exists")
			return False
		else:
			value = json.load(open(path))
			try:
				ok = value["entries"][str(entry)]
				return True
			except KeyError:
				Logger.error("MapLoading", "The map : " + str(map) + " in zone: " + str(zone) + " has no entry point " + str(entry))
				return False
