from game.render.texture.texturemanager import TextureManager as tm

class Font:

	POS_X = 0
	POS_Y = 1
	SIZE_X = 2
	SIZE_Y = 3

	def __init__(self, info):
		self.fontTexture = tm.key(info["texture"])
		self.infoFile = info["info"]
		self.sizeX = 0
		self.sizeY = 0
		self.charBeg = 32
		self.charEnd = 33
		self.numberChars = 1
		self.chars = {}
		self.load(self.infoFile)

	def load(self, file):
		with open(("game/resources/textures/fonts/" + file), 'r') as buffer:
			data = buffer.read().replace('\n', " ")
			buffer.close()

		# Init loading
		cursor = 0
		a = 0

		# Search and loading scaleX -> sizeX
		while data[cursor:cursor+3] != "sca":
			cursor += 1

		cursor += 7

		while data[cursor + a :cursor + a + 1] != " ":
			a += 1

		self.sizeX = int(data[cursor: cursor + a])
		cursor += a
		a = 0

		# Search and loading scaleY -> sizeY
		while data[cursor:cursor+3] != "sca":
			cursor += 1

		cursor += 7

		while data[cursor + a :cursor + a + 1] != " ":
			a += 1

		self.sizeY = int(data[cursor: cursor + a])
		cursor += a
		a = 0

		# Search number of letter
		while data[cursor:cursor+5] != "count":
			cursor += 1

		cursor += 6

		while data[cursor + a :cursor + a + 1] != " ":
			a += 1

		self.numberChars = int(data[cursor: cursor + a])
		cursor += a
		a = 0

		# Search first char
		while data[cursor:cursor+4] != "char":
			cursor += 1

		for number in range(self.numberChars):
			# Search number of letter
			while data[cursor:cursor + 2] != "id":
				cursor += 1

			cursor += 3

			while data[cursor + a:cursor + a + 1] != " ":
				a += 1

			charId = int(data[cursor: cursor + a])
			self.charEnd = charId
			self.chars[charId] = [0, 0, 0, 0]
			cursor += a
			a = 0

			while data[cursor:cursor + 1] != "x":
				cursor += 1

			cursor += 2

			while data[cursor + a:cursor + a + 1] != " ":
				a += 1

			self.chars[charId][Font.POS_X] = int(data[cursor: cursor + a]) / self.sizeX
			cursor += a
			a = 0

			while data[cursor:cursor + 1] != "y":
				cursor += 1

			cursor += 2

			while data[cursor + a:cursor + a + 1] != " ":
				a += 1

			self.chars[charId][Font.POS_Y] = int(data[cursor: cursor + a]) / self.sizeY
			cursor += a
			a = 0

			while data[cursor:cursor + 2] != "wi":
				cursor += 1

			cursor += 6

			while data[cursor + a:cursor + a + 1] != " ":
				a += 1

			self.chars[charId][Font.SIZE_X] = int(data[cursor: cursor + a]) / self.sizeX
			cursor += a
			a = 0

			while data[cursor:cursor + 2] != "he":
				cursor += 1

			cursor += 7

			while data[cursor + a:cursor + a + 1] != " ":
				a += 1

			self.chars[charId][Font.SIZE_Y] = int(data[cursor: cursor + a]) / self.sizeY
			cursor += a
			a = 0

	def constructVbo(self, text, size, centering="center"):
		line = 1 + text.count("\n")
		chars = len(text) - line + 1

		vbo = [0] * (chars * 36)

		part = text.split("\n")
		partAdvancement = [0] * len(part)

		# Calculations and securities
		for index in range(0, len(part)):
			if not index == 0:
				partAdvancement[index] = partAdvancement[index-1]
				partAdvancement[index] += len(part[index-1])

			for i in part[index]:
				if not ord(i) in self.chars:
					part[index] = part[index].replace(i, " ")

		# Create the content of vbo
		for index in range(len(part)):
			sizes = []
			for letter in part[index]:
				sizes.append(size * self.chars[ord(letter)][Font.SIZE_X] / self.chars[ord(letter)][Font.SIZE_Y])

			if centering.count("left") >= 1 :
				halfSizeX = 0
			elif centering.count("right") >= 1:
				halfSizeX = sum(sizes)
			else:
				halfSizeX = sum(sizes) / 2

			if centering.count("up") >= 1 :
				halfSizeY = 0
			elif centering.count("down") >= 1 :
				halfSizeY = size * (3 / 2 * line - 0.5)
			else:
				halfSizeY = size * (3 / 2 * line - 0.5) / 2

			for letter in range(len(sizes)):
				# pos X
				vbo[(partAdvancement[index] + letter) * 36] = sum(sizes[0:letter]) - halfSizeX
				vbo[(partAdvancement[index] + letter) * 36 + 9] = sum(sizes[0:letter+1]) - halfSizeX
				vbo[(partAdvancement[index] + letter) * 36 + 18] = vbo[(partAdvancement[index] + letter) * 36 + 9]
				vbo[(partAdvancement[index] + letter) * 36 + 27] = vbo[(partAdvancement[index] + letter) * 36]

				# pos Y
				vbo[(partAdvancement[index] + letter) * 36 + 1] = -size * (index + 1) - size / 2 * (index) + halfSizeY
				vbo[(partAdvancement[index] + letter) * 36 + 10] = vbo[(partAdvancement[index] + letter) * 36 + 1]
				vbo[(partAdvancement[index] + letter) * 36 + 19] = -size * index - (size / 2 * index) + halfSizeY
				vbo[(partAdvancement[index] + letter) * 36 + 28] = vbo[(partAdvancement[index] + letter) * 36 + 19]

				# texture pos X
				vbo[(partAdvancement[index] + letter) * 36 + 3] = round(
					self.chars[ord(part[index][letter])][Font.POS_X], 7)
				vbo[(partAdvancement[index] + letter) * 36 + 12] = round(
					self.chars[ord(part[index][letter])][Font.POS_X] + (self.chars[ord(part[index][letter])][Font.SIZE_X]), 7)
				vbo[(partAdvancement[index] + letter) * 36 + 21] = vbo[(partAdvancement[index] + letter) * 36 + 12]
				vbo[(partAdvancement[index] + letter) * 36 + 30] = vbo[(partAdvancement[index] + letter) * 36 + 3]

				# texture pos Y
				vbo[(partAdvancement[index] + letter) * 36 + 4] = 1 - \
									(self.chars[ord(part[index][letter])][Font.POS_Y] + self.chars[ord(part[index][letter])][Font.SIZE_Y])
				vbo[(partAdvancement[index] + letter) * 36 + 13] = vbo[(partAdvancement[index] + letter) * 36 + 4]
				vbo[(partAdvancement[index] + letter) * 36 + 22] = 1 - self.chars[ord(part[index][letter])][Font.POS_Y]
				vbo[(partAdvancement[index] + letter) * 36 + 31] = vbo[(partAdvancement[index] + letter) * 36 + 22]

		return vbo

	def bind(self):
		tm.bind(self.fontTexture)
