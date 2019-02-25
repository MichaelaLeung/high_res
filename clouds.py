import numpy as np
import smart
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
from astropy.io import fits 
import matplotlib
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False

def clouds(res, cirrus, strato):
    lamin = 0.5
    lamax = 2.0
    
    sim = smart.interface.Smart(tag = "prox")
    sim.smartin.alb_file = "composite1_txt.txt"
    infile = "profile_Earth_proxb_.pt_filtered"
    sim.set_planet_proxima_b()

    HERE = os.path.dirname(os.path.abspath(__file__))
    place = os.path.join(HERE, "clouds")

    try:
        os.mkdir(place)
    except OSError:
        pass

        
    sim.set_run_in_place(place) 
    sim.set_executables_automatically()

    sim.load_atmosphere_from_pt(infile, addn2 = False)


    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 


    sim.gen_lblscripts()
    sim.run_lblabc()

    if cirrus == 1:
        sim.aerosols = smart.interface.Aerosols(cirrus=True, stratocum=False)
        sim.tag = "_cirrus"

    elif strato == 1:
        sim.aerosols = smart.interface.Aerosols(cirrus=False, stratocum=True)
        sim.tag = "_strato"

    else:
        pass

    import platform
    
    if platform.system() == 'Darwin':
        # On a Mac: usetex ok
        mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
        mpl.rcParams['font.size'] = 25.0
        mpl.rc('text', usetex=True)
    elif platform.node().startswith("n"):
        # On hyak: usetex not ok, must change backend to 'agg'
        mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
        mpl.rcParams['font.size'] = 25.0
        mpl.rc('text', usetex=False)
        plt.switch_backend('agg')

    sim.write_smart(write_file = True)
    sim.run_smart()

    sim.open_outputs()
    wl = sim.output.rad.lam
    flux = sim.output.rad.pflux
    sflux = sim.output.rad.sflux

    adj_flux = flux/sflux

    return(wl, adj_flux)

def longplot():
    HERE = os.path.dirname(os.path.abspath(__file__))
    place = os.path.join(HERE, "clouds")

    try:
        os.mkdir(place)
    except OSError:
        pass
    
    lamin = 0.5
    lamax = 2.0 
    
    res = 0.01
    
    sim = smart.interface.Smart(tag = "prox")
    infile = "profile_Earth_proxb_.pt_filtered"
    label = "Self Consistent PCb (Earth like)"
    sim.smartin.alb_file = "composite1_txt.txt"
    sim.set_planet_proxima_b()
    sim.set_run_in_place(place) 
    sim.set_executables_automatically()

    sim.load_atmosphere_from_pt(infile, addn2 = False)

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

    adj_flux = flux/sflux
    
    return(wl, adj_flux)


def plotting():
    cirrus_wl, cirrus_flux = clouds(0.01, 1, 0)
    strato_wl, strato_flux = clouds(0.01, 0, 1)
    wl, flux = longplot()
    length_wl = min(len(cirrus_wl), len(strato_wl), len(wl))-1
    avg_wl = (cirrus_wl[:length_wl] + strato_wl[:length_wl] + wl[:length_wl])/3
    avg_flux = (cirrus_flux[:length_wl] + strato_flux[:length_wl] +flux[:length_wl])/3
    fig, ax = plt.subplots(figsize = (30, 10))
    ax.plot(avg_wl, avg_flux, label = "avg")
    ax.set_ylabel("Reflectance")
    ax.set_xlabel("Wavelength ($\mu$ m)")
    fig.savefig("avg_clougs.png", bbox_inches = 'tight')
    
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="clouds",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "48:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        plotting()
    else:
        # Presumably, on a regular computer: ready to run
        plotting()        








