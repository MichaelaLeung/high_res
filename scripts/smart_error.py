#!/usr/bin/python

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
import math 

def ocean_loss(lamin, lamax):
    
    res = 1/(10*lamin)

    place = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim = smart.interface.Smart(tag = "highd")
    sim.set_run_in_place(place)
    sim.smartin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.lblin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    infile = "/gscratch/vsm/mwjl/projects/high_res/inputs/10bar_O2_dry.pt_filtered.pt"
    label = "Simulated Earth-like planet orbiting Proxima Centauri"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/desert_highd.alb"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt(infile, addn2 = False)
    
    o2 = sim.atmosphere.gases[1]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'

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
    adj_flux = math.pi * (flux/sflux)
    return(wl, adj_flux)

def ocean_loss_noO4(lamin, lamax):
    res = 1/(10*lamin)
    place = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    sim2 = smart.interface.Smart(tag = "highd_noO4")
    sim2.set_run_in_place(place)
    
    infile = "/gscratch/vsm/mwjl/projects/high_res/inputs/10bar_O2_dry.pt_filtered.pt"
    label = "Simulated post ocean-loss planet orbiting Proxima Centauri"
    sim2.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/desert_highd.alb"

    sim2.smartin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim2.lblin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim2.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    sim2.set_planet_proxima_b()
    sim2.load_atmosphere_from_pt(infile, addn2 = False, scaleP = 1.0)
   
    o2 = sim2.atmosphere.gases[1]
    o2.cia_file = None
    sim2.set_executables_automatically()

    sim2.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim2.lblin.hitran_tag = 'hitran2016'
    sim2.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim2.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'

    sim2.smartin.sza = 57

    sim2.smartin.FWHM = res
    sim2.smartin.sample_res = res

    sim2.smartin.minwn = 1e4/lamax
    sim2.smartin.maxwn = 1e4/lamin 

    sim2.lblin.minwn = 1e4/lamax
    sim2.lblin.maxwn = 1e4/lamin 

    sim2.gen_lblscripts()
    sim2.run_lblabc()
    sim2.write_smart(write_file = True)
    sim2.run_smart()

    sim2.open_outputs()
    wl2 = sim2.output.rad.lam
    flux2 = sim2.output.rad.pflux
    sflux2 = sim2.output.rad.sflux

    adj_flux2 = math.pi * (flux2/sflux2)
    return(wl2, adj_flux2)

def plotting(lamin, lamax, atmos, title):
    import platform
    if platform.system() == 'Jarvis':
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
    fig_name = int(100*(float(lamin) + float(lamax))/2)
    if atmos == 0: # zero = ocean loss
        wl, flux = earth_like(lamin, lamax)
        wl2, flux2 = ocean_loss_noO4(lamin, lamax)
        fig, ax = plt.subplots(figsize = (10,10))
        ax.plot(wl, flux, label = "10 bar Ocean Loss")
        ax.plot(wl2, flux2, label = "10 bar Ocean Loss, no O2-O2")
        ax.set_title(title)
        ax.set_ylabel("Reflectance")
        ax.set_xlabel("Wavelength ($\mu$ m)")
        ax.legend()
        fig.savefig("/gscratch/vsm/mwjl/projects/high_res/plots/" + str(fig_name) +  "_noO4_new_CIA.png", bbox_inches = "tight")
   
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="smartest",
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
        plotting(0.61,0.65,0,"Oxygen Gamma band ")
        plotting(0.67,0.71,0,"Oxygen B band (0.69) ")
        plotting(0.74,0.78,0,"Oxygen A band (0.76) ")
        plotting(1.25,1.29,0,"1.27 Ocean Loss")
    else:
        plotting(0.61,0.645,1,"Gamma band (0.63) Ocean Outgassing")
