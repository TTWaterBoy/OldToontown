# File: D (Python 2.4)

from toontown.safezone import DistributedTreasure

class DistributedTagTreasure(DistributedTreasure.DistributedTreasure):
    
    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/icecream'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'
        self.accept('minigameOffstage', self.handleMinigameOffstage)

    
    def handleEnterSphere(self, collEntry):
        if not base.localAvatar.isIt:
            self.d_requestGrab()
        

    
    def handleMinigameOffstage(self):
        self.nodePath.reparentTo(hidden)


