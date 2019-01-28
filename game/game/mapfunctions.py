# Import test map

from PIL import Image

# 0 = Vide
# 1 = Sol
# 2 = Sol2
# 3 = Obstacle
# 4 = Plaque de pression
# 5 = Boule


map = [[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
		[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],

	   [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 3],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 3],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		[3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3],
		[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]]

collision = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			 [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
			 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			 [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
			 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
			 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

tiles = ['ground.png', 'ground2.png', 'obstacle.png', 'plaque de pression.png', 'bloc glissant.png']


def createMap():
	returnValues = []
	returnValues.append([len(map[0][0]), len(map[0])])
	returnValues.append([1.5, 4])

	width = len(map[0][0])
	height = len(map[0])

	returnValues.append(collision)

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

	# Show the map if you want
	returnValues.append(images)
	return returnValues
