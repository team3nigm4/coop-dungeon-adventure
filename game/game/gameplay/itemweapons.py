from game.game.gameplay import item
from game.game.entitymodel import triggerbox

class ItemKey(item.Item):
    def __init__(self, player):
        super().__init__(player, "Weapon")

    def useItem(self):
        entity = triggerbox.TriggerBox(self.player, ["TriggerBox", [self.player.pos[0] + self.player.halfColSize[0] + 0.15, self.player.pos[1]], 0.01])
        entity.attributes["damage"] = 1
        entity.setColBox([0.3, 0.01], True)
        self.player.em.add(entity)