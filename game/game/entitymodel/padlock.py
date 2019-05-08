from game.game.entityclass import entitycollision

class Padlock(entitycollision.EntityCollision):

    ARGS_COL_BOX_SIZE = 3
    ARGS_EVENT = 4

    def __init__(self, args):
        args.append(False)
        super().__init__(args)
        self.event = args[Padlock.ARGS_EVENT]
        self.checkState()

        self.setColBox(args[Padlock.ARGS_COL_BOX_SIZE])
        self.colReduc()

        self.setCollision(True)
        self.attributes["key"] = 2
        self.attributes["interaction"] = 2

        self.colRenderer.setAttributes(self.colSize, [1, 0.5, 0.5, 0.5])
        self.setDrawCol(True)

    def collision(self, ent):
        if ent.attributes["key"] == 1:
            ent.triggerBox(ent)
            ent.removeEm()
            self.ev.activate(self.event)
            self.removeEm()

        super().collision(ent)

    def checkState(self):
        self.ev.deactivate(self.event)
