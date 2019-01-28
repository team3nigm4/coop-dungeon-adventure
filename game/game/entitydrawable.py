# Entity class to display something

import pyrr

from game.game import entity
from game.render.shader.shadermanager import ShaderManager as sm
from game.render.shape import shape
from game.render.texture import texture


class EntityDrawable(entity.Entity):
	ARGS_SIZE = 2
	ARGS_PATH = 3
	ARGS_GAP = 4

	def __init__(self, args):
		super().__init__(args)
		self.size = args[EntityDrawable.ARGS_SIZE]

		self.tex = texture.Texture(args[EntityDrawable.ARGS_PATH])
		self.tex.load()

		size = self.size
		quad = [0 - args[EntityDrawable.ARGS_GAP][0], 0 - args[EntityDrawable.ARGS_GAP][1], 0.0, 0.0, 0.0,
				size[0] - args[EntityDrawable.ARGS_GAP][0], 0 - args[EntityDrawable.ARGS_GAP][1], 0.0, 1.0, 0.0,
				size[0] - args[EntityDrawable.ARGS_GAP][0], size[1] - args[EntityDrawable.ARGS_GAP][1], 0.0, 1.0,
				1.0,
				0 - args[EntityDrawable.ARGS_GAP][0], size[1] - args[EntityDrawable.ARGS_GAP][1], 0.0, 0.0, 1.0]

		indices = [0, 1, 2,
				   2, 3, 0]

		self.shape = shape.Shape(0)
		self.shape.setEbo(indices)
		self.shape.setVertices(quad, [3, 2])

		self.modelMtx = pyrr.Matrix44.identity()

	def display(self):

		sm.updateLink(sm.TEXTURE, "model", self.modelMtx)
		self.tex.bind()
		self.shape.display()

	def setPos(self, position):
		super().setPos(position)
		self.updateModel()

	def updateModel(self):
		self.modelMtx[3][0] = self.pos[0]
		self.modelMtx[3][1] = self.pos[1]

	def unload(self):
		self.tex.unload()
