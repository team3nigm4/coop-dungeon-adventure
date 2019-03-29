from game.game.entitymodel import door

class LockedDoor(door.Door):
    def __init__(self, args):
        args.append(False)
        super().__init__(args)
        self.attributes["key"] = 2
        self.testCol = False
        self.checkState()

    def collision(self, ent):
        if ent.attributes["key"] == 1:
            ent.triggerBox(ent)
            self.activate()
            ent.removeEm()

        super().collision(ent)

    def checkState(self):
        if self.testCol:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.testCol = True
        self.mam.setTileSize(self.pos, self.halfColSize, 0)
        self.setDrawCol(True)

    def deactivate(self):
        self.testCol = False
        self.mam.setTileSize(self.pos, self.halfColSize, 1)
        self.setDrawCol(False)
