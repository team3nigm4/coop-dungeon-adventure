# Import test map
from game.game.map.mapdisplay import MapDisplay

def loadMap(zone, name, entry):
	import json
	path = "game/resources/map/" + zone + "/" + name + ".json"

	try:
		getValues = json.load(open(path))

		returnValues = []
		returnValues.append([getValues["map"]["zone"], getValues["map"]["id"],
							int(getValues["entries"]["default"]), int(getValues["map"]["events"])])

		# Load graphic
		MapDisplay.mapValues = getValues["layers"]

		returnValues.append(getValues["collision"][0])
		returnValues.append(getValues["entries"][str(entry)])

		returnValues.append(getValues["entities"][0])

		return returnValues
	except json.decoder.JSONDecodeError:
		print("Can't load the map", path)
		exit()
