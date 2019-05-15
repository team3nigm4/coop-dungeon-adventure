# Parent class of each item

class Item:
	def __init__(self, player, name):
		# A item got a name and is hold by a player
		self.player = player
		self.name = name

	def getName(self):
		return self.name

	# These methods must be here

	def update(self):
		pass

	# Function called when the player want to call the primary function of the item
	def useItem(self):
		pass

	# Function called when the player want to call the secondary function of the item
	def useItem2(self):
		pass

	# Function called when the item is use and for what or who
	def triggerBox(self, ent):
		pass
