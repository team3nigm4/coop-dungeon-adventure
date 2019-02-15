from game.game.gameplay import item
from game.game.entitymodel import triggerbox

class ItemKey(item.Item):
    def __init__(self, player):
        super().__init__(player, "Key")

    def useItem(self):
        if self.player.direction == 0:
            entity = triggerbox.TriggerBox(self.player, ["TriggerBox", [self.player.pos[0] - self.player.halfColSize[0] - 0.15,
                                                            self.player.pos[1]], 0.01])
            size = [0.3, 0.01]
        elif self.player.direction == 1:
            entity = triggerbox.TriggerBox(self.player, ["TriggerBox", [self.player.pos[0],
                                                          self.player.pos[1]  + self.player.halfColSize[1] + 0.15], 0.01])
            size = [0.01, 0.3]
        elif self.player.direction == 2:
            entity = triggerbox.TriggerBox(self.player, ["TriggerBox",
                                                         [self.player.pos[0] + self.player.halfColSize[0] + 0.15,
                                                          self.player.pos[1]], 0.01])
            size = [0.3, 0.01]
        else :
            entity = triggerbox.TriggerBox(self.player, ["TriggerBox",
                                                         [self.player.pos[0],
                                                          self.player.pos[1] - self.player.halfColSize[0] - 0.15], 0.01])
            size = [0.01, 0.03]

        entity.setColBox(size, True)
        entity.attributes["key"] = 1
        self.player.em.add(entity)


    def used(self):
        self.player.item = item.Item(self.player, "null")