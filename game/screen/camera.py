# Manages the projection and view (position of cam) matrices

import pyrr


class Camera:
	NEAR = 0.01
	FAR = 1000

	def __init__(self, fov, pos):
		self.camPos = pos
		from game.main import config as Config
		self.projection = pyrr.matrix44.create_perspective_projection_matrix(fov, Config.ratio, Camera.NEAR, Camera.FAR)
		self.view = pyrr.Matrix44.identity()
		self.updateView()

	def getView(self):
		return self.view

	def addPos(self, add):
		self.camPos[0] += add[0]
		self.camPos[1] += add[1]
		self.camPos[2] += add[2]
		self.updateView()

	def updateView(self):
		self.view[3][0] = self.camPos[0]
		self.view[3][1] = self.camPos[1]
		self.view[3][2] = self.camPos[2]

	def getProjection(self):
		return self.projection
