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

def earth_like(lamin, lamax):
    res = 1/(10*lamin)
    sim = smart.interface.Smart(tag = "prox")
    sim.set_run_in_place()

    infile7 = "/Users/mwl/python/profile_Earth_proxb_.pt_filtered"
    label = "/Users/mwl/python/Simulated Earth-like planet orbiting Proxima Centauri"
    sim.smartin.alb_file = "/Users/mwl/python/composite1_txt.txt"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt(infile7, addn2 = True)
    
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/Users/mwl/python/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()

    sim.set_executables_automatically()
    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 

    sim.radstar = 0.1542

    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl = sim.output.trnst.lam
    t_depth = sim.output.trnst.tdepth
    return(wl, t_depth)

def ocean_loss(lamin, lamax):
    res = 1/(10*lamin)

    sim = smart.interface.Smart(tag = "highd")
    sim.set_run_in_place()
    
    infile = "/Users/mwl/python/10bar_O2_dry.pt_filtered.pt"
    label = "/Users/mwl/python/Simulated post ocean-loss planet orbiting Proxima Centauri"
    sim.smartin.alb_file = "/Users/mwl/python/desert_highd.alb"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt(infile, addn2 = True, scaleP = 1.0)
   
    o2 = sim.atmosphere.gases[1]
    o2.cia_file = '/Users/mwl/python/o4_calc.cia'

    sim.set_run_in_place() 
    sim.set_executables_automatically()

    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin

    sim.radstar = 0.1542

    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl = sim.output.trnst.lam
    t_depth = sim.output.trnst.tdepth
    return(wl, t_depth)

def ocean_outgassing(lamin, lamax):
    res = 1/(10*lamin)

    sim2 = smart.interface.Smart(tag = "highw")
    sim2.set_run_in_place()
    infile2 = "/Users/mwl/python/10bar_O2_wet.pt_filtered.pt"
    label = "Ocean Outgassing"
    sim2.smartin.alb_file = "/Users/mwl/python/earth_noveg_highw.alb"
    sim2.set_planet_proxima_b()
    sim2.set_star_proxima()

    sim2.set_run_in_place() 
    sim2.set_executables_automatically()

    sim2.smartin.sza = 57
    sim2.load_atmosphere_from_pt(infile2, addn2 = True, scaleP = 1.0)

    sim2.smartin.FWHM = res
    sim2.smartin.sample_res = res

    sim2.radstar = 0.1542

    sim2.smartin.minwn = 1e4/lamax
    sim2.smartin.maxwn = 1e4/lamin 

    sim2.lblin.minwn = 1e4/lamax
    sim2.lblin.maxwn = 1e4/lamin 


    o2 = sim2.atmosphere.gases[2]
    o2.cia_file = '/Users/mwl/python/o4_calc.cia'

    sim2.gen_lblscripts()
    sim2.run_lblabc()
    sim2.write_smart(write_file = True)
    sim2.run_smart()

    sim2.open_outputs()
    wl = sim2.output.trnst.lam
    t_depth = sim2.output.trnst.tdepth
    return(wl, t_depth)

def earth_like_hyak(lamin, lamax):
    
    res = 1/(10*lamin)

    place = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim = smart.interface.Smart(tag = "prox")
    sim.set_run_in_place(place)
    
    sim.smartin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.lblin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    infile = "/gscratch/vsm/mwjl/projects/high_res/inputs/profile_Earth_proxb_.pt_filtered"
    label = "Simulated Earth-like planet orbiting Proxima Centauri"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/composite1_txt.txt"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt(infile, addn2 = True)
    
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim.lblin.par_index = 7

    sim.radstar = 0.1542

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
    wl = sim.output.trnst.lam
    abs_rad = sim.output.trnst.absrad
    t_depth = sim.output.trnst.tdepth
    t_depth = np.asarray(t_depth)
    t_depth = t_depth * 10**6
    return(wl, t_depth, abs_rad)

def ocean_loss_hyak(lamin, lamax):
    res = 1/(10*lamin)
    place = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    sim = smart.interface.Smart(tag = "highd")
    sim.set_run_in_place(place)
    sim.smartin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.lblin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    
    infile = "/gscratch/vsm/mwjl/projects/high_res/inputs/10bar_O2_dry.pt_filtered.pt"
    label = "Simulated post ocean-loss planet orbiting Proxima Centauri"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/desert_highd.alb"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt(infile, addn2 = True, scaleP = 1.0)
   
    o2 = sim.atmosphere.gases[1]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'

    sim.set_run_in_place(place) 
    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim.lblin.par_index = 7
    
    sim.radstar = 0.1542


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
    wl = sim.output.trnst.lam
    abs_rad = sim.output.trnst.absrad
    t_depth = sim.output.trnst.tdepth
    t_depth = np.asarray(t_depth)
    t_depth = t_depth * 10**6
    return(wl, t_depth, abs_rad)

def ocean_outgassing_hyak(lamin, lamax):
    res = 1/(10*lamin)
    place = '/gscratch/vsm/mwjl/projects/high_res/smart_output'

    sim2 = smart.interface.Smart(tag = "highw")
    sim2.set_run_in_place(place)
    sim2.smartin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim2.lblin.out_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    sim2.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/high_res/smart_output'
    infile2 = "/gscratch/vsm/mwjl/projects/high_res/inputs/10bar_O2_wet.pt_filtered.pt"
    label = "Ocean Outgassing"
    sim2.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/earth_noveg_highw.alb"
    sim2.set_planet_proxima_b()
    sim2.set_star_proxima()

    sim2.set_run_in_place() 
    sim2.set_executables_automatically()

    sim2.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim2.lblin.hitran_tag = 'hitran2016'
    sim2.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim2.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim2.lblin.par_index = 7
    sim2.radstar = 0.1542


    sim2.smartin.sza = 57
    sim2.load_atmosphere_from_pt(infile2, addn2 = True, scaleP = 1.0)

    sim2.smartin.FWHM = res
    sim2.smartin.sample_res = res

    sim2.smartin.minwn = 1e4/lamax
    sim2.smartin.maxwn = 1e4/lamin 

    sim2.lblin.minwn = 1e4/lamax
    sim2.lblin.maxwn = 1e4/lamin 


    o2 = sim2.atmosphere.gases[2]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'

    sim2.gen_lblscripts()
    sim2.run_lblabc()
    sim2.write_smart(write_file = True)
    sim2.run_smart()

    sim2.open_outputs()
    wl = sim2.output.trnst.lam
    t_depth = sim2.output.trnst.tdepth
    t_depth = np.asarray(t_depth)
    t_depth = t_depth *10**6
    abs_rad = sim2.output.trnst.absrad    
    return(wl, t_depth, abs_rad)

def plotting(lamin, lamax, atmos, title):
    import platform
    if platform.system() == 'Darwin':
        # On a Mac: usetex ok
        matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
        matplotlib.rcParams['font.size'] = 25.0
        matplotlib.rc('text', usetex=False)
        plt.switch_backend('agg')

        fig_name = int(100*(float(lamin) + float(lamax))/2)
        if atmos == 0: # zero = ocean loss
            wl, flux = earth_like(lamin, lamax)
            wl2, flux2 = ocean_loss(lamin, lamax)
            fig, ax = plt.subplots(figsize = (10,10))
            ax.plot(wl, flux, label = "1 bar Earth-Like")
            ax.plot(wl2, flux2, label = "10 bar Ocean Loss")
            ax.set_title(title)
            ax.set_ylabel("Transit depth (ppm)")
            ax.set_xlabel("Wavelength ($\mu$ m)")
            ax.legend()
            fig.savefig(str(fig_name) +  "new_CIA.png", bbox_inches = "tight")
        else:
            wl, flux = earth_like(lamin, lamax)
            wl2, flux2 = ocean_outgassing(lamin, lamax)
            fig, ax = plt.subplots(figsize = (10,10))
            ax.plot(wl, flux, label = "1 bar Earth-Like")
            ax.plot(wl2, flux2, label = "10 bar Ocean Outgassing")
            ax.set_title(title)
            ax.set_ylabel("Effective Absorbing Radius")
            ax.set_xlabel("Wavelength ($\mu$ m)")
            ax.legend()
            fig.savefig(str(fig_name) +  "new_CIA_ocean.png", bbox_inches = "tight")
            
    elif platform.node().startswith("n"):
        # On hyak: usetex not ok, must change backend to 'agg'
        matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
        matplotlib.rcParams['font.size'] = 25.0
        matplotlib.rc('text', usetex=False)
        plt.switch_backend('agg')
        fig_name = int(100*(float(lamin) + float(lamax))/2)
        if atmos == 0: # zero = ocean loss
            wl, t_depth,app_rad = earth_like_hyak(lamin, lamax)
            wl2, t_depth2, app_rad2 = ocean_loss_hyak(lamin, lamax)
            fig, ax = plt.subplots(figsize = (10,10))
            ax.plot(wl, app_rad, label = "1 bar Earth-Like")
            ax.plot(wl2, app_rad2, label = "10 bar Ocean Loss")
            ax2 = ax.twinx()
            ax2.plot(wl, t_depth)
            ax2.plot(wl2, t_depth2)
            ax.set_title(title)
            ax.set_xlabel("Wavelength")
            ax.set_ylabel("Apparent Radius (km)")
            ax2.set_ylabel("Transit Depth (ppm)")
            ax.legend()
            fig.savefig("/gscratch/vsm/mwjl/projects/high_res/plots/" + str(fig_name) +  "_trn_new_CIA.png", bbox_inches = "tight")
        else:
            wl, t_depth,app_rad = earth_like_hyak(lamin, lamax)
            wl2, t_depth2,app_rad2 = ocean_outgassing_hyak(lamin, lamax)
            fig, ax = plt.subplots(figsize = (10,10))
            ax.plot(wl, app_rad, label = "1 bar Earth-Like")
            ax.plot(wl2, app_rad2, label = "10 bar Ocean Outgassing")
            ax2 = ax.twinx()
            ax2.plot(wl, t_depth)
            ax2.plot(wl2, t_depth2)
            ax.set_title(title)
            ax.set_ylabel("Apparent Radius (km)")
       	    ax2.set_ylabel("Transit Depth (ppm)")
            ax.set_xlabel("Wavelength ($\mu$ m)")
            ax.legend()
            fig.savefig("/gscratch/vsm/mwjl/projects/high_res/plots/" + str(fig_name) +  "_trn_new_CIA_ocean.png", bbox_inches = "tight")

   
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="nor_plt",
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
        plotting(0.61,0.645,0,"Gamma band (0.63) Ocean Loss")
        plotting(0.67,0.71,0,"Oxygen B band (0.69) Ocean Loss")
        plotting(0.74,0.78,0,"Oxygen A band (0.76) Ocean Loss")
        plotting(1.25,1.29,0,"1.27 Ocean Loss")
        plotting(0.61,0.645,1,"Gamma band (0.63) Ocean Outgassing")
        plotting(0.67,0.71,1,"Oxygen B band (0.69) Ocean Outgassing")
        plotting(0.74,0.78,1,"Oxygen A band (0.76) Ocean Outgassing")
        plotting(1.25,1.29,1,"1.27 Ocean Outgassing")
    else:
        plotting(0.61,0.645,1,"Gamma band (0.63) Ocean Outgassing")
