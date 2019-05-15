# Class activation block, depend of sliding block, activator entity

from game.game.entitymodel import slidingblock


class ActivationBlock(slidingblock.SlidingBlock):

	def __init__(self, args):
		super().__init__(args)
		self.entityRenderer.setImage([1, 1], "activation-block", [0.5, 0.5])
		self.attributes["energy"] = 1
