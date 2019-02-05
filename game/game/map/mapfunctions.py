# Import test map

from PIL import Image

tiles = ['ground.png', 'ground2.png', 'obstacle.png']


def loadMap(zone, name, entry):
	import json
	path = "game/resources/map/" + zone + "/" + name + ".json"

	getValues = []
	try:
		getValues = json.load(open(path))

		returnValues = []
		returnValues.append([getValues["map"]["zone"], getValues["map"]["id"],
							int(getValues["entries"]["default"]), int(getValues["map"]["events"])])

		# Load graphic
		map = []
		for i in range(0, len(getValues["layers"])):
			map.append(getValues["layers"][i])

		# Create images
		width = len(map[0][0])
		height = len(map[0])
		print(height)

		images = []
		gap = 32
		for z in range(0, len(map)):
			new_im = Image.new('RGBA', (width * gap, height * gap))
			for x in range(0, width):
				for y in range(0, height):
					if not map[z][y][x] == 0:
						im = Image.open("game/resources/textures/tiles/" + tiles[map[z][y][x] - 1])
						new_im.paste(im, (x * gap, y * gap))
			images.append(new_im)
		returnValues.append(images)

		returnValues.append(getValues["collision"])
		returnValues.append(getValues["entries"][str(entry)])


		returnValues.append(getValues["entities"])
		print(returnValues[4])

		return returnValues
	except json.decoder.JSONDecodeError:
		print("Can't load the map", path)
		exit()
