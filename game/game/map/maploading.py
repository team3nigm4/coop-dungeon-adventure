# Import test map
import json
import os
from sys import exit


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
			print("Can't load the map", path)
			exit()

	@staticmethod
	def isMap(zone, map, entry):
		path = "game/resources/map/" + zone + "/" + map + ".json"
		state = os.path.isfile(path)
		if not state:
			print("(MapLoading): the map :", map, " in zone:", zone, "doesn't exists")
			return False
		else:
			value = json.load(open(path))
			try:
				ok = value["entries"][str(entry)]
				return True
			except KeyError:
				print("(MapLoading): the map :", map, " in zone:", zone, "has not entry point:", entry)
				return False
