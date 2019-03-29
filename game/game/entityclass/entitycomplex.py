from game.game.entityclass import entitydrawable
from game.util.logger import Logger
import math


class EntityComplex(entitydrawable.EntityDrawable):
	def __init__(self, args):
		super().__init__(args)
		self.maxSpeed = 1

		self.life = 1
		self.damage = 1
		self.invincibilityCounter = 0
		self.weight = 1
		self.knockback = 0.2

		self.stuned = False
		self.stunTime = 10
		self.stunCounter = 0

		# In frame
		self.invincibilityTime = 1
		self.takeDamage = True
		self.wantDirection = [0, 0]
		self.oldWantDirection = [0, 0]

	def left(self, input):
		if input > 1 and not self.stuned:
			self.wantDirection[0] -= 1

	def up(self, input):
		if input > 1 and not self.stuned:
			self.wantDirection[1] += 1

	def right(self, input):
		if input > 1 and not self.stuned:
			self.wantDirection[0] += 1

	def down(self, input):
		if input > 1 and not self.stuned:
			self.wantDirection[1] -= 1

	def update(self):
		super().update()
		if self.stuned:
			if self.stunCounter >= self.stunTime:
				self.stuned = False
				self.stunCounter = 0
			else:
				self.stunCounter += 1

		if not self.takeDamage:
			if self.invincibilityCounter >= self.invincibilityTime:
				self.takeDamage = True
				self.invincibilityCounter = 0
			else:
				self.invincibilityCounter += 1

	def display(self):
		super().display()

	def dispose(self):
		super().dispose()
		self.wantDirection = [0, 0]
		self.oldWantDirection = self.oldWantDirection = [0, 0]

	def setLife(self, newLife, death=True):
		self.life = newLife
		if self.life <= 0 and death:
			self.removeEm()

	def collision(self, ent):
		if (ent.attributes["playerSword"] == 1 and self.attributes["playerSword"] == 2) or \
				(ent.attributes["playerBow"] == 1 and self.attributes["playerBow"] == 2):
			ent.triggerBox(self)

	def applyKnockback(self, knockback, pos):
		distance = [self.pos[0] - pos[0], self.pos[1] - pos[1]]
		hyp = math.sqrt(distance[0] * distance[0] + distance[1] * distance[1])
		angle = math.acos(distance[0] / hyp)
		if self.takeDamage:
			self.speed[0] += (knockback / self.weight) * math.cos(angle)
			if distance[1] >= 0:
				self.speed[1] = (knockback / self.weight) * math.sin(angle)
			else:
				self.speed[1] = (knockback / self.weight) * math.sin(-angle)

	def setStun(self, state):
		if state and self.takeDamage:
			self.stuned = True

	def applyDamage(self, damage, death=True):
		if self.takeDamage:
			Logger.info("ENTITY COMPLEX", self.type + " take " + str(damage) + " damage(s)")
			self.setLife(self.life - damage, death)
			self.takeDamage = False
