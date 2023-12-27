class Inputs:
    def __init__(self):
        self.basic = self.Basic()
        self.blanket = self.Blanket()

    class Basic:
        def __init__(self):
            self.timeToReplace:float = None #years
            self.downTime:float = None # years
            self.reactorType:int = None #2 is IFE, 1 is MFE, 3 is MIF
            self.N_mod:int = None # number of modules
            self.AM:int = None # dunno
            self.constructionTime:float #years

        def toDict(self):
            return {
                'timeToReplace': self.timeToReplace,
                'downTime': self.downTime,
                'reactorType': self.reactorType,
                'N_mod': self.N_mod,
                'AM': self.AM,
                'constructionTime': self.constructionTime
            }

    class Blanket:
        def __init__(self):
            self.firstWall:int = None
            self.blanketType:int = None
            self.primaryCoolant:int = None
            self.secondaryCoolant:int = None
            self.neutronMultiplier:int = None
            self.structure:int = None

        def toDict(self):
            return {
                'firstWall': self.firstWall,
                'blanketType': self.blanketType,
                'primaryCoolant': self.primaryCoolant,
                'secondaryCoolant': self.secondaryCoolant,
                'neutronMultiplier': self.neutronMultiplier,
                'structure': self.structure
            }


    def toDict(self):
        inputsDict = {
            'basic': self.basic.toDict(),
            'blanket': self.blanket.toDict()
        }
        return inputsDict