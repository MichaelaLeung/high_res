import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from astropy.io import fits
import smart
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False
import random

def longplot(atmos, res, lamin, lamax, cirrus, strato):
    
    sim = smart.interface.Smart(tag = atmos)
    if atmos == "earth":
        infile = "earth_avg.pt"
        sim.smartin.alb_file = "composite1_txt.txt"
        sim.load_atmosphere_from_pt(infile, addn2 = False)
        co2 = sim.atmosphere.gases[1]
        co2.cia_file = 'co2_calc.cia'
        o2 = sim.atmosphere.gases[6]
        o2.cia_file = 'o4_calc.cia'
        n2 = sim.atmosphere.gases[7]
        n2.cia_file = 'n4_calc.cia'
    elif atmos == "prox":
        infile = "profile_Earth_proxb_.pt_filtered"
        label = "Simulated Earth-like planet orbiting Proxima Centauri"
        sim.smartin.alb_file = "composite1_txt.txt"
        sim.set_planet_proxima_b()
        sim.load_atmosphere_from_pt(infile, addn2 = False)
        co2 = sim.atmosphere.gases[2]
        co2.cia_file = 'co2_calc.cia'
        o2 = sim.atmosphere.gases[3]
        o2.cia_file = 'o4_calc.cia'
    elif atmos == "highd":
        infile = "10bar_O2_dry.pt_filtered.pt"
        label = "Simulated post ocean-loss planet orbiting Proxima Centauri"
        sim.smartin.alb_file = "desert_highd.alb"
        sim.set_planet_proxima_b()
        sim.load_atmosphere_from_pt(infile, addn2 = False, scaleP = 1.0)
        co2 = sim.atmosphere.gases[0]
        co2.cia_file = 'co2_calc.cia'
        o2 = sim.atmosphere.gases[1]
        o2.cia_file = 'o4_calc.cia'
        n2 = sim.atmosphere.gases[6]
        n2.cia_file = 'n4_calc.cia'
    elif atmos == "highw":
        infile = "10bar_O2_wet.pt_filtered.pt"
        label = "Simulated 10 bar oxygen ocean planet orbiting Proxima Centauri"
        sim.smartin.alb_file = "earth_noveg_highw.alb"
        sim.set_planet_proxima_b()
        sim.load_atmosphere_from_pt(infile, addn2 = False, scaleP = 1.0)
        co2 = sim.atmosphere.gases[1]
        co2.cia_file = 'co2_calc.cia'
        o2 = sim.atmosphere.gases[2]
        o2.cia_file = 'o4_calc.cia'
        n2 = sim.atmosphere.gases[8]
        n2.cia_file = 'n4_calc.cia'
    elif atmos == "arch_prox":
        infile = "clearsky_archean.pt"
        sim.set_planet_proxima_b()
    HERE = os.path.dirname(os.path.abspath(__file__))
    place = os.path.join(HERE, "longplot")

    try:
        os.mkdir(place)
    except OSError:
        pass

        
    sim.set_run_in_place(place) 
    sim.set_executables_automatically()

#    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016' #/gscratch/vsm/alinc/fixed_input/
 #   sim.lblin.hitran_tag = 'hitran2016'
#    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    #sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'

    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 


    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl = sim.output.rad.lam
    flux = sim.output.rad.pflux
    sflux = sim.output.rad.sflux

    adj_flux = flux/sflux * ((sim.smartin.radius / sim.smartin.r_AU) **2 )
    refl = flux/sflux
    flux = adj_flux
    
    if platform.system() == 'Darwin':
        # On a Mac: usetex ok
        matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
        matplotlib.rcParams['font.size'] = 25.0
        matplotlib.rc('text', usetex=True)
    elif platform.node().startswith("n"):
        # On hyak: usetex not ok, must change backend to 'agg'
        matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
        matplotlib.rcParams['font.size'] = 25.0
        matplotlib.rc('text', usetex=False)
        plt.switch_backend('agg')
        
    fig, ax = plt.subplots(figsize = (30, 10))
    ax3 = ax.twinx()
    ax3.plot(wl, refl)
    ax3.set_ylabel("Reflectance")
    ax.set_xlabel("Wavelength ($\mu$ m)")
    ax.set_title(label)
    ax.set_xlim(0.5,2)
    ax.axvspan(0.61, 0.65, alpha=0.5, color='0.85')
    ax.axvspan(0.67, 0.71, alpha=0.5, color='0.85')
    ax.axvspan(0.74, 0.78, alpha=0.5, color='0.85')
    ax.axvspan(1.25, 1.29, alpha=0.5, color='0.85')
    
    fig.savefig(str(atmos) + "_newCIA.png", bbox_inches = 'tight')




if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="co_test",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "10:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
 #       longplot("earth", 0.01, 0.5, 2, True, False)
 #       longplot("earth", 0.01, 0.5, 2, False, True)
        longplot("prox", 0.01, 0.6, 1, False, False)
 #       longplot("highd", 0.01, 0.5, 2, False, False)
 #       longplot("highw", 0.01, 0.5, 2, False, False)
 #       longplot("arch_prox", 0.01, 0.5, 2, False, False)
    else:
        # Presumably, on a regular computer: ready to run
        longplot("earth", 1, 0.5, 0.501, True, False)
        longplot("earth", 1, 0.5, 0.501, False, True)
        longplot("prox", 1, 0.5, 0.501, False, False)
        longplot("highd", 1, 0.5, 0.501, False, False)
        longplot("highw", 1, 0.5, 0.501, False, False)
        longplot("arch_prox", 1, 0.5, 0.501, False, False)








