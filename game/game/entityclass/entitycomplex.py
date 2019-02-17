from game.game.entityclass import entitydrawable

class EntityComplex(entitydrawable.EntityDrawable):
    def __init__(self, args):
        super().__init__(args)
        self.life = 6
        self.damage = 1
        self.maxSpeed = 1

    def setLife(self, newLife):
        if newLife <= 0:
            self.em.remove(self.id)

        self.life = newLife
