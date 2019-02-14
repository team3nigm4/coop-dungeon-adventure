# Manages the projection and view (position of cam) matrices

import pyrr
from game.game.entityclass.entitymanager import EntityManager as em

class Camera:
	NEAR = 0.01
	FAR = 1000

	width = 9
	height = 6

	def __init__(self, fov, pos):
		self.pos = pos
		from game.main.config import Config
		self.projection = pyrr.matrix44.create_perspective_projection_matrix(fov, Config.ratio, Camera.NEAR, Camera.FAR)
		self.view = pyrr.Matrix44.identity()
		self.updateView()

		# Track
		self.track = [False, False]
		self.entityId = 0
		self.posMax = [0, 0]
		self.setMaximum([18, 12])

	def getView(self):
		return self.view

	def setMaximum(self, maximum):
		self.posMax[0] = -(maximum[0] - Camera.width)
		self.posMax[1] = -(maximum[1] - Camera.height)

	def addPos(self, add):
		self.pos[0] += add[0]
		self.pos[1] += add[1]
		self.pos[2] += add[2]
		self.updateView()

	def setPos(self, newPos):
		self.pos = newPos
		self.updateView()

	def trackEntity(self, entityId):
		self.entityId = entityId
		
	def goToEntity(self):
		if self.track[0]:
			if -em.entities[self.entityId].pos[0] > - Camera.width:
				self.setPos([-Camera.width, self.pos[1], self.pos[2]])
			elif -em.entities[self.entityId].pos[0] < self.posMax[0]:
				self.setPos([self.posMax[0], self.pos[1], self.pos[2]])
			else:	
				self.setPos([round(-em.entities[self.entityId].pos[0] * 32) / 32, self.pos[1], self.pos[2]])
		if self.track[1]:
			if -em.entities[self.entityId].pos[1] > - Camera.height:
				self.setPos([self.pos[0], -Camera.height, self.pos[2]])
			elif -em.entities[self.entityId].pos[1] < self.posMax[1]:
				self.setPos([self.pos[0], self.posMax[1], self.pos[2]])
			else:
				self.setPos([self.pos[0], round(-em.entities[self.entityId].pos[1] * 32) / 32, self.pos[2]])


	def updateView(self):
		self.view[3][0] = self.pos[0]
		self.view[3][1] = self.pos[1]
		self.view[3][2] = self.pos[2]

	def getProjection(self):
		return self.projection
