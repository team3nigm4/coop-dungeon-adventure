import numpy

class Matrix4f:
	def __init__(self, identity=False):
		self.matrix = [[0, 0, 0, 0],
					   [0, 0, 0, 0],
					   [0, 0, 0, 0],
					   [0, 0, 0, 0]]

		self.matrix = numpy.array(self.matrix, dtype=numpy.float32)

		if identity:
			self.setIdentity()

	def setIdentity(self):
		self.matrix[0][0] = 1
		self.matrix[0][1] = 0
		self.matrix[0][2] = 0
		self.matrix[0][3] = 0
		self.matrix[1][0] = 0
		self.matrix[1][1] = 1
		self.matrix[1][2] = 0
		self.matrix[1][3] = 0
		self.matrix[2][0] = 0
		self.matrix[2][1] = 0
		self.matrix[2][2] = 1
		self.matrix[2][3] = 0
		self.matrix[3][0] = 0
		self.matrix[3][1] = 0
		self.matrix[3][2] = 0
		self.matrix[3][3] = 1

	def refresh(self):
		self.matrix = numpy.array(self.matrix, dtype=numpy.float32)
