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

    class Blanket:
        def __init__(self):
            self.firstWall:int = None
            self.blanketType:int = None
            self.primaryCoolant:int = None
            self.secondaryCoolant:int = None
            self.neutronMultiplier:int = None
            self.structure:int = None