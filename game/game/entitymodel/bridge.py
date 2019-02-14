# Class pressure plate

from game.game.entityclass import entitydrawable
from game.game.map.mapmanager import MapManager as mam

import math

class Bridge(entitydrawable.EntityDrawable):
	# True horizontal, False vertical
	ARGS_DIRECTION = 2
	ARGS_COUNTER = 3
	ARGS_SIZE = 4
	ARGS_EVENT = 5

	def __init__(self, args):
		super().__init__(args)

		self.entityRenderer.setImagePath([1, 1], "entities/pontV.png", [0, 0])

		self.direction = args[Bridge.ARGS_DIRECTION]
		self.size = args[Bridge.ARGS_SIZE]
		if self.size > 0:
			self.append = 1
		else:
			self.append = -1

		self.size = int(math.fabs(self.size))

		self.event = args[Bridge.ARGS_EVENT]
		self.countLen = args[Bridge.ARGS_COUNTER]

		# 0 is the counter, 1 is the case linked, 2 the value to change
		self.counters = []
		self.state = False

	def update(self):
		toRemove = []
		for i in range(len(self.counters)):
			if self.counters[i][0] >= self.countLen:
				# Apply change
				toRemove.append(i)
				if self.direction:
					mam.changeInterMap([self.counters[i][1], self.pos[1]], self.counters[i][2])

					# Next case
					if not math.fabs(math.fabs(self.pos[0]) - math.fabs(self.counters[i][1])) == self.size:
						self.counters.append([0, self.counters[i][1] + self.append, self.counters[i][2]])
				else:
					mam.changeInterMap([self.pos[0], self.counters[i][1]], self.counters[i][2])
					# Next case
					if not math.fabs(math.fabs(self.pos[1]) - math.fabs(self.counters[i][1])) == self.size:
						self.counters.append([0, self.counters[i][1] + self.append, self.counters[i][2]])

			else:
				self.counters[i][0] += 1

		# Remove finish case
		if not len(toRemove) == 0:
			for i in toRemove:
				del self.counters[i]

	def display(self):
		if self.state:
			super().display()

	def activate(self):
		if self.direction:
			self.counters.append([0, self.pos[0], 0])
		else:
			self.counters.append([0, self.pos[1], 0])

		self.state = True

	def deactivate(self):
		if self.direction:
			self.counters.append([0, self.pos[0], 2])
		else:
			self.counters.append([0, self.pos[1], 2])

		self.state = False

	def setId(self, id):
		super().setId(id)
		from game.game.map.eventmanager import EventManager
		EventManager.addActive(self.event, self.id)