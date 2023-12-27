#Basic inputs

timetoReplace=10 #years
downTime=1 #years
reactorType=2 #2 is IFE, 1 is MFE, 3 is MIF %input
N_mod=1 #input
AM=1 #input
constructionTime=3 #input

firstW = blanket["firstWall"][1]
blanketT = blanket["blanketType"][0]
primaryC = blanket["primaryCoolant"][0]
secondaryC = blanket["secondaryCoolant"][7]
neutronM = blanket["neutronMultiplier"][3]
structure1 = blanket["structure"][1]