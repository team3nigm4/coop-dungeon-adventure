from game.game.entityclass import entitydrawable

class EntityComplex(entitydrawable.EntityDrawable):
    def __init__(self, args):
        super().__init__(args)
        self.maxSpeed = 1

        self.life = 6
        self.damage = 1

        # In frame
        self.invincibilityTime = 1
        self.takeDamage = True
        self.invincibilityCounter = 0

    def update(self):
        super().update()
        if not self.takeDamage:
            if self.invincibilityCounter >= self.invincibilityTime:
                self.takeDamage = True
                self.invincibilityCounter = 0
            else:
                self.invincibilityCounter +=1

    def setLife(self, newLife):
        if newLife <= 0:
            self.em.remove(self.id)

        self.life = newLife

    def applyDamage(self, damage):
        if self.takeDamage:
            print(self.type, "take", str(damage), "damages")
            self.setLife(self.life - damage)
            self.takeDamage = False
