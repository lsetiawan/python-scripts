#!/usr/bin/env python
import os
import subprocess
import rasterio as rio
#import pymodis.downmodis as pmod


# Function to download MODIS tiles from USGS ftp server
def performDownload(tilelist, foldername, dates):
    maindir = "MOD13A3.006"
    if not os.path.exists(maindir):
        print "Creating {}".format("MOD13A3.006")
        os.makedirs(maindir)
    os.chdir(os.path.join(os.getcwd(),maindir))
    for folder in foldername:
        if not os.path.exists(folder):
            print "Creating {}".format(folder)
            os.makedirs(folder)
    for i in range(0,len(dates)):
        if i != len(dates) - 1:
            print "Working on {0} to {1}".format(dates[i], dates[i + 1])
            print "Files are saved in {}".format(os.path.join(os.getcwd(), dates[i]))
            print ""
            subprocess.call(["modis_download.py", "-r", "-p", "MOD13A3.006", "-t", "{}".format(tilelist), "-f",
                             "{}".format(dates[i]), "-e", "{}".format(dates[i+1]), "{}".format(os.path.join(os.getcwd(), dates[i]))])
            """pmod.downModis(os.path.join(os.getcwd(), dates[i]), tiles = tilelist,
                       product="MOD13A3.006", today=dates[i], enddate=dates[i+1])"""

# Function to create list of tiles to download.
# In this case, MODIS tiles around lower 48 and central america are downloaded
# Tiles are based on sinusoidal projection by NASA
def createTiles():
    h = []
    v = []
    tile = []

    for k in range(7, 15):
        h.append(k)
    for l in range(4, 10):
        v.append(l)
    for i in range(0, len(h) - 1):
        for j in range(0, len(v) - 1):
            if h[i] < 10 and v[i] >= 10:
                tile.append("h0" + str(h[i]) + "v" + str(v[j]))
            elif v[j] < 10 and h[i] >= 10:
                tile.append("h" + str(h[i]) + "v0" + str(v[j]))
            elif h[i] < 10 and v[j] < 10:
                tile.append("h0" + str(h[i]) + "v0" + str(v[j]))
            else:
                tile.append("h" + str(h[i]) + "v" + str(v[j]))
    return tile


# Function to create list of dates in the format for pyModis to ingest
def createDates(startyear, endyear):
    folderlist = []
    datelist = []
    for year in range(startyear, (endyear + 1)):
        for month in range(01, 13):
            if month < 10:
                folderlist.append(str(year) + "_0" + str(month) + "_0" + str(1))
                datelist.append(str(year) + "-0" + str(month) + "-0" + str(1))
            if month >= 10:
                folderlist.append(str(year) + "_" + str(month) + "_0" + str(1))
                datelist.append(str(year) + "-" + str(month) + "-0" + str(1))
    return folderlist, datelist


def main():
    startyear = input("Enter start year: ")
    endyear = input("Enter end year: ")
    foldernames, dates = createDates(startyear, endyear)
    tilelist = ' '.join(createTiles())
    print tilelist
    print foldernames
    print dates
    performDownload(tilelist,foldernames,dates)

if __name__ == '__main__':
    main()
