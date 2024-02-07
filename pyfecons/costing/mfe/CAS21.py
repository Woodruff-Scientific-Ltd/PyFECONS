from pyfecons.inputs import Inputs
from pyfecons.data import Data

def GenerateData(inputs: Inputs, data:Data, figures:dict):

    basic = inputs.basic
    IN = data.power_table
    OUT = data.cas21
    #Cost Category 21: Buildings

    #Buildings come out to be 470$/kW gross, so if we are looking at a gross power of 1GW, we have:


    #21.01.00,,Site improvements and facs,,20.7,,,,,2019,1.19,

    OUT.C210100 = 24.6/1e3 * IN.p_et

    #21.02.00,,Fusion Heat Island Building,Concrete & Steel,131.6,48.3,48.3,60,140000,2009,1.42,

    OUT.C210200 = 186.8/1e3 * IN.p_et

    #21.03.00,,Turbine building,Steel ,45.3,48.3,48.3,30,70000,2019,1.19,

    OUT.C210300 = 54.0/1e3 * IN.p_et

    #21.04.00,,Heat exchanger building,Concrete & Steel,31.7,48.3,48.3,15,35000,2019,1.19,

    OUT.C210400 = 37.8/1e3 * IN.p_et

    #21.05.00,,Power supply & energy storage,Concrete & Steel,9.1,9.7,9.7,6.0,560,2019,1.19,

    OUT.C210500 = 10.8/1e3 * IN.p_et
    #21.06.00,,Reactor auxiliaries,Concrete & Steel,4.5,4.8,4.8,3.0,70,2019,1.19,

    OUT.C210600 = 5.4/1e3 * IN.p_et

    #21.07.00,,Hot cell,Concrete & Steel,65.8,24.2,24.2,60,35000,2013,1.42,

    OUT.C210700 = 93.4/1e3 * IN.p_et

    #21.08.00,,Reactor services,Steel frame,13.2,4.8,4.8,10,233,2013,1.42,

    OUT.C210800 = 18.7/1e3 * IN.p_et

    #21.09.00,,Service water,Steel frame,0.2,1.3,4.0,4.0,21,2019,1.19,

    OUT.C210900 = 0.3/1e3 * IN.p_et

    #21.10.00,,Fuel storage,Steel frame,0.9,5.0,15.0,2.5,188,2019,1.19,

    OUT.C211000 = 1.1/1e3 * IN.p_et

    #21.11.00,,Control room,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,

    OUT.C211100 = 0.9/1e3 * IN.p_et

    #21.12.00,,Onsite AC power,Steel frame,0.7,3.6,10.8,1.8,70,2019,1.19,

    OUT.C211200 = 0.8/1e3 * IN.p_et

    #21.13.00,,Administration,Steel frame,3.7,20.0,60.0,10,12000,2019,1.19,

    OUT.C211300 = 4.4/1e3 * IN.p_et

    #21.14.00,,Site services,Steel frame,1.3,7.3,22.0,3.7,593,2019,1.19,

    OUT.C211400 = 1.6/1e3 * IN.p_et

    #21.15.00,,Cryogenics,Steel frame,2.0,11.0,33.0,5.5,2003,2019,1.19,

    OUT.C211500 = 2.4/1e3 * IN.p_et

    #21.16.00,,Security,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,

    OUT.C211600 = 0.9/1e3 * IN.p_et

    #21.17.00,,Ventilation stack,Steel cylinder & concrete foundation,22.7,,,120,,2019,1.19,

    OUT.C211700 = 27.0/1e3 * IN.p_et

    OUT.C210000 = OUT.C210100 + OUT.C210200 + OUT.C210300 + OUT.C210400 + OUT.C210500 + OUT.C210600 + OUT.C210700 \
        + OUT.C210800 + OUT.C210900 + OUT.C211000 + OUT.C211100 + OUT.C211200 + OUT.C211300 + OUT.C211400 + OUT.C211500 + OUT.C211600 + OUT.C211700

    OUT.C211800 = 0.1*OUT.C210000 #10% contingency

    OUT.C210000 = OUT.C210000 + OUT.C211800