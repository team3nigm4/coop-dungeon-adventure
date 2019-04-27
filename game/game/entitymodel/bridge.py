# Class pressure plate

from game.game.entityclass import entitycollision
from game.game.map.maprender import MapRender

import math

class Bridge(entitycollision.EntityCollision):
	# True horizontal, False vertical
	ARGS_DIRECTION = 3
	ARGS_COUNTER = 4
	ARGS_SIZE = 5
	ARGS_EVENT = 6

	def __init__(self, args):
		super().__init__(args)

		self.direction = args[Bridge.ARGS_DIRECTION]
		self.size = args[Bridge.ARGS_SIZE]
		if self.size > 0:
			self.size -= 1
			self.append = 1
		else:
			self.size += 1
			self.append = -1

		self.size = int(math.fabs(self.size))

		self.event = args[Bridge.ARGS_EVENT]
		self.countLen = args[Bridge.ARGS_COUNTER]

		# 0 is the counter, 1 is the case linked, 2 the value to change
		self.counters = []
		self.state = False

		if self.direction:
			if self.append < 0:
				self.colSize = [self.size + 1, 1]
				self.valueRender = [self.pos[0] + 1 - self.colSize[0] / 2, self.pos[1] + 0.5]
			else:
				self.colSize = [self.size + 1, 1]
				self.valueRender = [self.pos[0] + self.colSize[0] / 2, self.pos[1] + 0.5]
		else:
			if self.append < 0:
				self.colSize = [1, self.size + 1]
				self.valueRender = [self.pos[0] + 0.5, self.pos[1] + 1 - self.colSize[1] / 2]
			else:
				self.colSize = [1, self.size + 1]
				self.valueRender = [self.pos[0] + 0.5, self.pos[1] + self.colSize[1] / 2]

		self.colRenderer.setAttributes(self.colSize, [0, 0.7725, 0.258, 0.5])
		self.colRenderer.updateModel(self.valueRender)

		self.ev.addActive(self.event, self.entityId)

	def update(self):
		toRemove = []
		for i in range(len(self.counters)):
			if self.counters[i][0] >= self.countLen:

				# Apply change
				toRemove.append(i)
				if self.direction:
					rotation = 2
					position = int(self.counters[i][1]), int(self.pos[1])

					if self.counters[i][1] == self.pos[0]:
						texture = "begin-bridge"
					elif self.counters[i][1] == self.pos[0] + self.size * self.append:
						texture = "begin-bridge"
						rotation += 2
						rotation %= 4
					else:
						texture = "bridge"

					self.mam.setTileSize([self.counters[i][1]+0.5, self.pos[1]+0.5], [0.498, 0.498], self.counters[i][2])

					# Next case
					if not math.fabs(math.fabs(self.pos[0]) - math.fabs(self.counters[i][1])) == self.size:
						self.counters.append([0, self.counters[i][1] + self.append, self.counters[i][2]])
				else:
					rotation = 1
					position = int(self.pos[0]), int(self.counters[i][1])

					if self.counters[i][1] == self.pos[1]:
						texture = "begin-bridge"
					elif self.counters[i][1] == self.pos[1] + self.size * self.append:
						texture = "begin-bridge"
						rotation += 2
						rotation %= 4
					else:
						texture = "bridge"

					self.mam.setTileSize([self.pos[0] + 0.5, self.counters[i][1] + 0.5], [0.498, 0.498], self.counters[i][2])

					# Next case
					if not math.fabs(math.fabs(self.pos[1]) - math.fabs(self.counters[i][1])) == self.size:
						self.counters.append([0, self.counters[i][1] + self.append, self.counters[i][2]])

				if self.counters[i][2] == 0:
					if self.append > 0:
						rotation += 2
						rotation %= 4

					MapRender.addTile(0, position[0], position[1], texture, rotation)
				else:
					MapRender.deleteTile(0, position[0], position[1])

			else:
				self.counters[i][0] += 1

		# Remove finish case
		if not len(toRemove) == 0:
			for i in toRemove:
				del self.counters[i]

	def display(self):
		pass

	def activate(self):
		if self.direction:
			self.counters.append([0, self.pos[0], 0])
		else:
			self.counters.append([0, self.pos[1], 0])

		self.state = True
		self.colRenderer.updateModel(self.valueRender)

	def deactivate(self):
		if self.direction:
			self.counters.append([0, self.pos[0], 2])
		else:
			self.counters.append([0, self.pos[1], 2])

		self.state = False
		self.colRenderer.updateModel(self.valueRender)
