from game.game.entitymodel import door

class LockedDoor(door.Door):
    def __init__(self, args):
        args.append(False)
        super().__init__(args)
        self.attributes["key"] = 2
        self.deactivate()

    def collision(self, ent):
        if ent.attributes["key"] == 1:
            ent.triggerBox(ent)
            self.activate()
            self.em.remove(ent.id)

        super().collision(ent)

    def activate(self):
        self.isActive = True
        self.mam.setTileSize(self.pos, self.halfColSize, 0)
        self.setDrawCol(True)

    def deactivate(self):
        self.isActive = False
        self.setColBox(self.colSize, False)
        self.mam.setTileSize(self.pos, self.halfColSize, 1)
        self.setColBox(self.colSize, True)
        self.setDrawCol(False)

