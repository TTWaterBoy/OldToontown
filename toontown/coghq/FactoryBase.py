# File: F (Python 2.4)

import FactorySpecs
from otp.level import LevelSpec
from toontown.toonbase import ToontownGlobals

class FactoryBase:
    
    def __init__(self):
        pass

    
    def setFactoryId(self, factoryId):
        self.factoryId = factoryId
        self.factoryType = ToontownGlobals.factoryId2factoryType[factoryId]
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(factoryId)

    
    def getCogTrack(self):
        return self.cogTrack

    
    def getFactoryType(self):
        return self.factoryType

    if __dev__:
        
        def getEntityTypeReg(self):
            import FactoryEntityTypes as FactoryEntityTypes
            EntityTypeRegistry = EntityTypeRegistry
            import otp.level
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg

    

