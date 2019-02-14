# Class sliding block

from game.game.entitymodel import slidingblock


class ActivationBlock(slidingblock.SlidingBlock):

	def __init__(self, args):
		super().__init__(args)
		self.entityRenderer.setImagePath([1, 1], "entities/activation-block.png", [0.5, 0.5])
		self.attributes["energy"] = 1
