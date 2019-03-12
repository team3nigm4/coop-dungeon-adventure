from game.game.entityclass import entitydrawable
from game.util.logger import Logger

class EntityComplex(entitydrawable.EntityDrawable):
    def __init__(self, args):
        super().__init__(args)
        self.maxSpeed = 1

        self.life = 1
        self.damage = 1

        # In frame
        self.invincibilityTime = 1
        self.takeDamage = True
        self.invincibilityCounter = 0
        self.wantDirection = [0, 0]

    def left(self, input):
        if input > 1:
            self.wantDirection[0] -= 1

    def up(self, input):
        if input > 1:
            self.wantDirection[1] += 1

    def right(self, input):
        if input > 1:
            self.wantDirection[0] += 1

    def down(self, input):
        if input > 1:
            self.wantDirection[1] -= 1

    def update(self):
        super().update()
        if not self.takeDamage:
            if self.invincibilityCounter >= self.invincibilityTime:
                self.takeDamage = True
                self.invincibilityCounter = 0
            else:
                self.invincibilityCounter +=1

    def display(self):
        self.wantDirection = [0, 0]
        super().display()

    def setLife(self, newLife, death=True):
        self.life = newLife
        if self.life <= 0 and death:
            self.em.remove(self.id)

    def collision(self, ent):
        if (ent.attributes["playerSword"] == 1 and self.attributes["playerSword"] == 2) or \
                (ent.attributes["playerBow"] == 1 and self.attributes["playerBow"] == 2):
            ent.triggerBox(self)

    def applyDamage(self, damage, death=True):
        if self.takeDamage:
            Logger.info("ENTITY COMPLEX", self.type + " take " + str(damage) + " damage(s)")
            self.setLife(self.life - damage, death)
            self.takeDamage = False
