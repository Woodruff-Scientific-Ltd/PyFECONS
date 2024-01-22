
class Material:
    def __init__(self, rho=None, c=None,  c_raw=None, m=None, sigma=None):
        self.rho = rho
        self.c = c
        self.c_raw = c_raw
        self.m = m
        self.sigma = sigma

class Materials:
    def __init__(self):
        self.FS = Material(rho=7470, c_raw=10, m=3, sigma=450)
        self.Pb = Material(rho=9400, c_raw=2.4, m=1.5)
        self.Li4SiO4 = Material(rho=2390, c_raw=1, m=2)
        self.Flibe = Material(rho=1900, c=40)
        self.W = Material(rho=19300, c_raw=100, m=3)
        self.Li = Material(rho=534, c_raw=70, m=1.5)
        self.BFS = Material(rho=7800, c_raw=30, m=2)
        self.SiC = Material(rho=3200, c_raw=14.49, m=3)
        self.Inconel = Material(rho=8440, c_raw=46, m=3)
        self.Cu = Material(rho=7300, c_raw=10.2, m=3)
        self.Polyimide = Material(rho=1430, c_raw=100, m=3)
        self.YBCO = Material(rho=6200, c=55)
        self.Concrete = Material(rho=2300, c_raw=13/25, m=2)
        self.SS316 = Material(rho=7860, c_raw=2, m=2, sigma=900)
        self.Nb3Sn = Material(c=5)
        self.Incoloy = Material(rho=8170, c_raw=4, m=2)
        self.GdBCO = Material()  # Density and cost not provided
        self.He = Material()  # Density and cost not provided
        self.NbTi = Material()  # Density and cost not provided

        self.PbLi: Material  # Values to be calculated
        pblir = 10
        pbli_rho = (self.Pb.rho * pblir + self.Li.rho) / (pblir + 1)
        pbli_c = (self.Pb.c_raw * self.Pb.m * pblir + self.Li.c_raw * self.Li.m) / (pblir + 1)
        self.PbLi = Material(rho=pbli_rho, c=pbli_c)
