from game.game.entityclass import entitydrawable
from game.game.map.mapmanager import MapManager as mam
from game.inputs.inputmanager import InputManager as im


class SlidingBlock(entitydrawable.EntityDrawable):
	SPEED = 0.20

	def __init__(self, args):
		super().__init__(args)
		self.setColBox([0.998, 0.998], True)
		self.entityRenderer.setImagePath([1, 1], "entities/sliding-block.png", [0.5, 0.5])

		self.attributes["collision"] = 2
		self.attributes["heavy"] = 1
		self.attributes["interaction"] = 2

	def update(self):
		if self.inMov[0]:
			newPos = [mam.checkCollisionX(self.pos, self.speed[0], self.halfColSize), self.pos[1]]
			if newPos == self.pos:
				self.inMov[0] = False
				self.speed[0] = 0
			else:
				self.setPos(newPos)
		elif self.inMov[1]:
			newPos = [self.pos[0], mam.checkCollisionY(self.pos, self.speed[1], self.halfColSize)]
			if newPos == self.pos:
				self.inMov[1] = False
				self.speed[1] = 0
			else:
				self.setPos(newPos)

	def active(self, ent):

		if ent.attributes["collision"] != 2 or ent.inMov[0] == True or ent.inMov[1] == True:
			# Move in x
			if (ent.inMov[0] and not ent.inMov[1]):
				tempDir = 0
				if ent.speed[0] > 0:
					ent.setPos([self.pos[0] - self.halfColSize[0] - ent.halfColSize[0] - 0.001, ent.pos[1]])
					tempDir = 1
				elif ent.speed[0] < 0:
					ent.setPos([self.pos[0] + self.halfColSize[0] + ent.halfColSize[0] + 0.001, ent.pos[1]])
					tempDir = -1

				if ent.type == "SlidingBlock":
					ent.inMov[0] = 0

				# interaction attribute
				if ent.type == "Player":
					if im.inputPressed(im.INTERACT):
						self.inMov[0] = True
						self.speed[0] = SlidingBlock.SPEED * tempDir


			# Move in y
			elif (ent.inMov[1] and not ent.inMov[0]):
				tempDir = 0
				if ent.speed[1] < 0:
					ent.setPos([ent.pos[0], self.pos[1] + self.halfColSize[1] + ent.halfColSize[1] + 0.001])
					tempDir = -1
				elif ent.speed[1] > 0:
					ent.setPos([ent.pos[0], self.pos[1] - self.halfColSize[1] - ent.halfColSize[1] - 0.001])
					tempDir = 1

				if ent.type == "SlidingBlock":
					ent.inMov[1] = 0

				# interaction attribute
				if ent.type == "Player":
					if im.inputPressed(im.INTERACT):
						self.inMov[1] = True
						self.speed[1] = SlidingBlock.SPEED * tempDir

			# Move in x and y
			elif ent.inMov[0] and ent.inMov[1]:
				oldPos = [ent.pos[0] - ent.speed[0], ent.pos[1] - ent.speed[1]]

				# what ent's position to replace

				if ent.inMov[0] == True:
					# left
					if oldPos[0] + ent.halfColSize[0] < self.pos[0] - self.halfColSize[0]:
						ent.setPos([self.pos[0] - self.halfColSize[0] - ent.halfColSize[0] - 0.001, ent.pos[1]])
					# right
					elif oldPos[0] - ent.halfColSize[0] > self.pos[0] + self.halfColSize[0]:
						ent.setPos([self.pos[0] + self.halfColSize[0] + ent.halfColSize[0] + 0.001, ent.pos[1]])

				if ent.inMov[1] == True:
					# up
					if oldPos[1] - ent.halfColSize[1] > self.pos[1] + self.halfColSize[1]:
						ent.setPos([ent.pos[0], self.pos[1] + self.halfColSize[1] + ent.halfColSize[1] + 0.001])
					# down
					elif oldPos[1] + ent.halfColSize[1] < self.pos[1] - self.halfColSize[1]:
						ent.setPos([ent.pos[0], self.pos[1] - self.halfColSize[1] - ent.halfColSize[1] - 0.001])
