#!/usr/bin/env python

# Import the necessary libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import shapely.geometry as sgeom
import pyproj

def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap

def getPNG(name, data, epsg):
    plt.figure(figsize=(20,10), frameon=False, dpi=300)
    box = sgeom.box(minx=-180, maxx=179, miny=-85,
                    maxy=85)
    x0, y0, x1, y1 = box.bounds
    # Set output projection
    ax = plt.axes(projection=ccrs.PlateCarree())
    '''if epsg == 4326:
        ax = plt.axes(projection=ccrs.PlateCarree())
    else:
        ax = plt.axes(projection=ccrs.epsg(epsg))'''
    #ax.set_global()
    ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())
    ### Create a list of RGB tuples
    colors = [(8, 0, 5), (255, 0, 242), (91, 0, 234), (0, 255, 245), (0, 255, 124),
              (244, 250, 97), (255, 122, 53), (255, 0, 25), (111, 8, 18)] # This example uses the 8-bit RGB
    ### Create an array or list of positions from 0 to 1.
    position = [0,0.19,0.19,0.38,0.50,0.62,0.75,0.9,1]
    ### Call the function make_cmap which returns your colormap
    my_cmap = make_cmap(colors, position=position, bit=True)
    # Define the coordinate system that the grid lons and grid lats are on
    coord = ccrs.PlateCarree() # aka Lat,Long
    # Plots the data
    data.plot(ax=ax,transform=coord, add_colorbar=False, vmin=0,vmax=5, add_labels=False, cmap=my_cmap)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    # Put Coastline on figure
    #ax.coastlines()
    if not os.path.exists("arag_climatology"):
        os.mkdir("arag_climatology")
    plt.savefig(os.path.join("arag_climatology",'{0}_EPSG{1}.png'.format(name,epsg)),bbox_inches='tight',dpi=300,
                transparent=True, format='png', pad_inches=0.0)
    #plt.show()

def get_dataset(pth, ds_name):
    work_file = os.path.join(pth, '{}'.format(ds_name))
    print "Working on {}".format(work_file)
    ds = xr.open_dataset(work_file)
    arag86_99 = []
    arag00_13 = []
    arag72_13 = []

    pressure_list = np.array(ds.Pressure).tolist()
    p = []
    for l in pressure_list:
        p.append(int(l))
    names1 = []
    names2 = []
    names3 = []
    pre = "arag"

    fw1 = open("min_max_86_99.txt", 'w')
    fw2 = open("min_max_00_13.txt", 'w')
    #fw3 = open("min_max_72_13.txt", 'w')
    # Time 1
    for i in range(0,19):
        # Get multiple depth 1986-1999 dataset
        arag86_99.append(ds.OmegaAinsitu[0, i, :, :])
        time = "8699"
        names1.append("{0}_{1}dbar_{2}".format(pre, p[i], time))
        if i == 18:
            fw1.write("{0}dbar,{1},{2},{3}".format(p[i], time, ds.OmegaAinsitu[0, i, :, :].min().values,
                                                        ds.OmegaAinsitu[0, i, :, :].max().values))
        else:
            fw1.write("{0}dbar,{1},{2},{3};".format(p[i], time, ds.OmegaAinsitu[0, i, :, :].min().values,
                                                    ds.OmegaAinsitu[0, i, :, :].max().values))
    # Time 2
    for j in range(0,19):
        # Get multiple depth 2000-2013 dataset
        arag00_13.append(ds.OmegaAinsitu[1, j, :, :])
        time = "0013"
        names2.append("{0}_{1}dbar_{2}".format(pre, p[j], time))
        if j == 18:
            fw2.write("{0}dbar,{1},{2},{3}".format(p[j], time, ds.OmegaAinsitu[1, j, :, :].min().values,
                                                        ds.OmegaAinsitu[1, j, :, :].max().values))
        else:
            fw2.write("{0}dbar,{1},{2},{3};".format(p[j], time, ds.OmegaAinsitu[1, j, :, :].min().values,
                                                     ds.OmegaAinsitu[1, j, :, :].max().values))
    # Depth 19 - 33
    '''for k in range(19,33):
        # Get multiple depth 1972-2013 dataset
        arag72_13.append(ds.OmegaAinsitu[0, k, :, :])
        arag72_13_max.append(ds.OmegaAinsitu[0, k, :, :].max())
        arag72_13_min.append(ds.OmegaAinsitu[0, k, :, :].min())
        time = "7213"
        names3.append("{0}_{1}dbar_{2}".format(pre, p[k], time))
        if k == 32:
            fw3.write("{0}dbar_{1},{2},{3}".format(p[k], time, ds.OmegaAinsitu[0, k, :, :].min().values,
                                                     ds.OmegaAinsitu[0, k, :, :].max().values))
        fw3.write("{0}dbar_{1},{2},{3};".format(p[k], time, ds.OmegaAinsitu[0, k, :, :].min().values,
                                                     ds.OmegaAinsitu[0, k, :, :].max().values))'''

    fw1.close()
    fw2.close()
    #fw3.close()

    names = [names1,names2,names3]

    return arag86_99,arag72_13,arag00_13,names

def prnt_lib_ver():
    '''
        Function used to print the current versions of xarray, cartopy, and numpy
    '''
    print "xarray version: " + xr.__version__
    print "cartopy version: " + cartopy.__version__
    print "numpy version: " + np.__version__

def main():
    prnt_lib_ver()

    pth = "/Users/lsetiawan/Desktop/shared_ubuntu/APL/GOA-ON/Aragonite/GLODAPv2_Mapped_Climatologies"
    ds_name = "GLODAPv2.OmegaAinsitu.nc"
    #pth =  raw_input("Where are your GLODAPv2_Mapped_Climatologies? [enter path] ")
    #ds_name = raw_input("Which dataset would you like to work on? [enter name of netCDF. eg. GLODAPv2.OmegaAinsitu.nc] ")
    arag86_99, arag72_13, arag00_13, names = get_dataset(pth,ds_name)
    # Processing
    for i in range(0, len(names)):
        for j in range(0, len(names[i])):
            if "8699" in names[i][j]:
                print "{0} {1} {2} {3}".format(i, j, names[i][j], arag86_99[j])
                if j == 0 or j == 9:
                    print names[i][j]
                    print arag86_99[j]
                    getPNG(names[i][j], arag86_99[j], 4326)
            if "0013" in names[i][j]:
                print "{0} {1} {2} {3}".format(i, j, names[i][j],arag00_13[j])
                if j == 0 or j == 9:
                    print names[i][j]
                    print arag86_99[j]
                    getPNG(names[i][j], arag00_13[j], 4326)
            if "7213" in names[i][j]:
                print "{0} {1} {2} {3}".format(i, j+19, names[i][j],arag72_13[j])
                getPNG(names[i][j], arag72_13[j], 4326)



if __name__ == '__main__':
    main()