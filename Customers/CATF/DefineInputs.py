# You must define an inputs object
from Inputs.Input import Inputs
inputs = Inputs()


inputs.basic.timeToReplace = 10
inputs.basic.downTime = 10
inputs.basic.reactorType = 2
inputs.basic.N_mod = 1
inputs.basic.AM = 1
inputs.basic.constructionTime=3


inputs.blanket.firstWall = 1
inputs.blanket.blanketType = 0
inputs.blanket.primaryCoolant = 0
inputs.blanket.secondaryCoolant = 7
inputs.blanket.neutronMultiplier = 3
inputs.blanket.structure = 1