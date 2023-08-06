# HREELS data handling and simulation

Set of data analysis routines for surface vibrational spectroscopy based on a Delta05 spectrometer. Simple data reading and plotting routines are provided, but also advanced routines for in depth analysis.

A fast data browser as graphical user interface is included as **ViewHREELS.py**. It can also take command line arguments.

Additional a python interface to a Fortran-based calculation of full HREEL spectra is provided in **class lambin** (in **calcHREELS.py**). Note that this part requires a local compilation (via f2py3) from the Fortran90 files. Only for the Linux-based python version 3.6, there are complied files provided. For details see below.

Most of the routines are within the **class HREELS** (HREELS.py). A simple command line program is "showHREELS.py", which reads one data file and plots the spectrum with a second amplified trace.

    Usage:  >python showHREELS.py filename [factor wavenumber]

        E.g.: python showHREELS.py H9H03 100 53 

More general usage:

Read dataset by calling the HREELS class:
    **data1 = HREELS('filename', datapath='datapath')**        # Here you can omit the extension '.gph'
                                                    # The second argument is optional
                                                    
    This will assign/calculate the following properties:
    
    data1.filename
    data1.datapath
    data1.startTime
    data1.stopTime
    data1.totalTime
    data1.timePerChannel
    data1.numberOfSegments
    data1.energy    # Electron kinetic energy
    data1.filament  # Filament current in Ampere
    data1.segments  # list of segment info
    data1.data      # [(-100.1021616, 259.5), (-98.5374352, 264.5), ...]
    data1.xdata
    data1.ydata
    data1.maxIntensity  # Count rate of elastic peak
    data1.resolution    # width of elastic peak

The following methods are defined within the class:

    info()      :   Print information about the spectrum
    plot()      :   Draws the spectrum. Optional arguments are:
                    (xmin=None, xmax=None, factor=1, label='x', normalized=False, color="b-",marker=True)

    plotInfoAmp()   Draws spectrum together with amplified trace.
    pickPeak()  :   Select peak by mouse cursor. The call of figure() is required before.
    selectData():   Returns the data between wavenumbers x1 and x2
    findIndex(lossenergy): Returns the data array index for a given energy loss
    setMarker(x, y, ymin=0, size=None): Sets vertical marker with text label 
    plotWaterFall(...):
        

# calcHREELS

These routines are based on the publication "Computation of the surface electron-energy-loss spectrum in specular geometry for an arbitrary plane-stratified medium" by P. Lambin, J.-P. Vigneron, and A. A. Lucas, in the Journal "Computer Physics Communications 60, 351-64(1990)".



