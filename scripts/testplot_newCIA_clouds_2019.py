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
    sim.load_atmosphere_from_pt(infile, addn2 = False)
    
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/HITRAN2019.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim.lblin.par_index = 7


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
    adj_flux = (flux/sflux)
    return(wl, adj_flux)

def clouds(lamin, lamax, cloud_type):
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
    sim.load_atmosphere_from_pt(infile, addn2 = False)
    
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/HITRAN2019.par'
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim.lblin.par_index = 7


    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 


    sim.gen_lblscripts()
    sim.run_lblabc()

    
    # Create a cirrus cloud mie scattering aerosol mode
    mie_cirrus = smart.interface.MieMode(mie_file = os.path.join(smart.interface.CLDMIEDIR, "baum_cirrus_de100.mie"),
                                         mie_skip = 1,
                                         mie_lines =
                                         '1,4,5,3',
                                         iang_smart = 2)

    # Create an optical depth profile
    tau_cirrus = smart.interface.CloudTau(vert_file = os.path.join(smart.interface.CLDMIEDIR, "cld_tau.dat"),
                                          vert_ref_wno = 15400.0,
                                          vert_skip = 4,
                                          vert_coord = 1,
                                          vert_xscale = 1.0e5,
                                          vert_yscale = 2.0)

    # Create an Aerosol object with our cirrus mie scattering and optical depths
    cirrus = smart.interface.Aerosols(miemodes=[mie_cirrus],
                                      mietau=[tau_cirrus])

    sim_cirrus.aerosols = cirrus

    # Create a stratocumulus cloud mie scattering aerosol mode
    mie_strato = smart.interface.MieMode(mie_file = os.path.join(smart.interface.CLDMIEDIR, "strato_cum.mie"),
                                         mie_skip = 19,
                                         mie_lines = '1,7,8,11',
                                         iang_smart = 1,
                                         mom_skip = 17)

    # Create an optical depth profile
    tau_strato = smart.interface.CloudTau(vert_file = os.path.join(smart.interface.CLDMIEDIR, "cld_tau.dat"),
                                          vert_ref_wno = 15400.0,
                                          vert_skip = 28,
                                          vert_coord = 1,
                                          vert_xscale = 1.0e5,
                                          vert_yscale = 1.0)

    # Create an Aerosol object with our stratocumulus mie scattering and optical depths
    strato = smart.interface.Aerosols(miemodes=[mie_strato],
                                      mietau=[tau_strato])

    sim_strato.aerosols = strato


    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl = sim.output.rad.lam
    flux = sim.output.rad.pflux
    sflux = sim.output.rad.sflux

    adj_flux = flux/sflux

    return(wl, adj_flux)


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
    sim.load_atmosphere_from_pt(infile, addn2 = False, scaleP = 1.0)
   
    o2 = sim.atmosphere.gases[1]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'

    sim.set_run_in_place(place) 
    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/HITRAN2019.par'
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim.lblin.par_index = 7


    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin

    sim.smartin.iraylei = [4]
    sim.smartin.vraylei = [1]

    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl2 = sim.output.rad.lam
    flux2 = sim.output.rad.pflux
    sflux2 = sim.output.rad.sflux

    adj_flux2 = flux2/sflux2
    return(wl2, adj_flux2)

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

    sim2.lblin.par_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/HITRAN2019.par' #/gscratch/vsm/alinc/fixed_input/
    sim2.lblin.hitran_tag = 'hitran2016'
    sim2.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim2.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'
    sim2.lblin.par_index = 7

    sim.smartin.iraylei = [4]
    sim.smartin.vraylei = [1]

    sim2.smartin.sza = 57
    sim2.load_atmosphere_from_pt(infile2, addn2 = False, scaleP = 1.0)

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
    wl2 = sim2.output.rad.lam
    flux2 = sim2.output.rad.pflux
    sflux2 = sim2.output.rad.sflux

    adj_flux2 = flux2/sflux2
    return(wl2, adj_flux2)

def plotting(lamin, lamax, atmos, title):
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 25.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig_name = int(100*(float(lamin) + float(lamax))/2)
    wl, flux = earth_like_hyak(lamin, lamax)
    wl2, flux2 = clouds(lamin, lamax, 0)
    wl3, flux3 = clouds(lamin, lamax, 1)
    avg_flux = (0.5*flux+0.25*flux2+0.25*flux3)
    if atmos == 0: # zero = ocean loss
        wl4, flux4 = ocean_loss_hyak(lamin, lamax)
        fig, ax = plt.subplots(figsize = (10,10))
        ax.plot(wl, avg_flux, label = "1 bar Earth-Like")
        ax.plot(wl4, flux4, label = "10 bar Ocean Loss")
        ax.set_title(title)
        ax.set_ylabel("Reflectance")
        ax.set_xlabel("Wavelength ($\mu$m)")
        if lamin == 0.61:
            ax.legend()
        fig.savefig("/gscratch/vsm/mwjl/projects/high_res/plots/" + str(fig_name) +  "new_CIA_clouds.png", bbox_inches = "tight")
    else:
        wl4, flux4 = ocean_outgassing_hyak(lamin, lamax)
        fig, ax = plt.subplots(figsize = (10,10))
        ax.plot(wl, avg_flux, label = "1 bar Earth-Like")
        ax.plot(wl4, flux4, label = "10 bar Ocean Outgassing")
        ax.set_title(title)
        ax.set_ylabel("Reflectance")
        ax.set_xlabel("Wavelength ($\mu$m)")
        if lamin == 0.61:
            ax.legend()
        fig.savefig("/gscratch/vsm/mwjl/projects/high_res/plots/" + str(fig_name) +  "new_CIA_ocean_clouds.png", bbox_inches = "tight")

   
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="nor_cld",
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
