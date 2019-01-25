from PIL import Image

def createMap(width, height, gap):
	im = Image.open("game/resources/textures/error.png")
	new_im = Image.new('RGBA', (width*gap, height*gap))
	for i in range(0, width):
		for a in range(0, height):
			new_im.paste(im, (i * gap,a * gap))
	# Show the map if you want
	# new_im.show()
	return new_im