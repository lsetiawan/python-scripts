#!/usr/bin/env python
''' Import the Necessary Libraries '''
import os
import pymodis.downmodis as pmod
import numpy as np
import gdal
import subprocess
from datetime import date, timedelta


def makeFolder(basepath, foldername):
    ''' 
    Function used to create the MOD13A3.006 Folders and for each dates 

    '''
    maindir = "MOD13A3.006"
    if not os.path.exists(maindir):
        print "Creating {}".format("MOD13A3.006")
        os.makedirs(maindir)
    os.chdir(os.path.join(os.getcwd(), maindir))
    for folder in foldername:
        if not os.path.exists(folder):
            print "Creating {}".format(folder)
            os.makedirs(folder)


def performDownload(tilelist, dates, i, work_path):
    '''
    Downloads MODIS tiles from USGS ftp server and save them to the appropriate
    date folder 
    
    '''
    print ""
    print "Working on {0} to {1}".format(dates[i], dates[i + 1])
    print "Files are saved in {}".format(work_path)
    destination = work_path
    # make downloader
    dm = pmod.downModis(destinationFolder=destination,
                        path="MOLT", product="MOD13A3.006", tiles="{}".format(tilelist),
                        today="{}".format(dates[i]), enddate="{}".format(dates[i + 1]))
    dm.connect()
    print "Connection Attempts: " + str(dm.nconnection)
    # Download all the files in that day
    print "Please Wait....................."
    dm.downloadsAllDay()


def makeFileName(x, ext="tif"):
    """
    Generate a new file name by appending a suffix and changing the extension of an input file name 
    :param x: string, input file name
    :param suffix: string, suffix to be placed just before file extension (e.g., 'NDVI')
    :param ext: string, extension. Don't put the period before the extension
    """
    base = os.path.splitext(os.path.basename(x))[0]
    return base + '.' + ext


def processHDF(folder, work_path):
    '''
    Perfom processing for the .hdf MODIS Tiles. Reads the data, grab only the desired subdataset,
    in this case the EVI. Next, GDAL library is used to create numpy array and save the array as 
    GeoTiff in the appropriate folder.
    
    '''
    if ".tif" not in folder:
        print "Now converting hdf for {}".format(folder)
        os.chdir(work_path)
        print os.getcwd()
        for hdf in os.listdir('.'):
            if ".hdf" in hdf and ".txt" not in hdf and ".log" not in hdf and ".xml" not in hdf:
                print "Working on {0}".format(hdf)
                sds = gdal.Open(hdf, gdal.GA_ReadOnly).GetSubDatasets()
                # Read data in arrays
                # EVI              
                vi_src = gdal.Open(sds[1][0])
                vi_np = vi_src.ReadAsArray()

                # QA
                QA_src = gdal.Open(sds[10][0])
                QA_np = QA_src.ReadAsArray()

                # Let's take a quick look at the dimension of that first array
                cols, rows = vi_np.shape
                # Perform value replacement and drop QA layer
                vi_np[np.logical_and(QA_np != 0, QA_np != 1)] = -3000
                # De-allocate QA array
                QA_np = None
                # Get Geotransforms and projection of original dataset
                geoT = vi_src.GetGeoTransform()
                proj = vi_src.GetProjection()

                # Create new dataset to write array to
                outfile_name = os.path.join(os.getcwd(), makeFileName(hdf, 'tif'))
                driver = gdal.GetDriverByName('GTiff')
                # Create empty dataset using array dimentions
                dataset = driver.Create(outfile_name, cols, rows, 1, gdal.GDT_Int16)
                dataset.SetGeoTransform(geoT)
                dataset.SetProjection(proj)
                dataset.GetRasterBand(1).SetNoDataValue(-3000)
                dataset.GetRasterBand(1).WriteArray(vi_np)
                # Close datasets and unallocate arrays
                dataset = None
                vi_np = None
                QA_np = None
                vi_src = None
                QA_src = None


def reprojectTile(path, end_date, i):
    '''
    Reprojection is performed after .hdf is converted to .tif. The tiles are reprojected to 
    EPSG:4326 by using gdalwarp.
    
    '''
    if not os.path.exists(os.path.join(path, "EPSG436")):
        os.makedirs(os.path.join(path, 'EPSG4326'))
        print "Creating folder: EPSG4326"

    img = []
    for tif in os.listdir(path):
        if ".tif" in tif and ".aux.xml" not in tif and end_date[i + 1].strftime("%j") in tif:
            img.append(tif)
        if ".hdf" in tif:
            print "Removing {}".format(tif)
            os.remove(tif)
    newpath = os.path.join(path, "EPSG4326")
    for i in range(0, len(img)):
        print "Reprojecting {}".format(img[i])
        subprocess.call(["gdalwarp", "-t_srs", "EPSG:4326", "-dstnodata",
                         "-3000", "{0}".format(img[i]), "{0}".format(os.path.join(newpath, "{0}".format(img[i])))])
    return newpath


def mosaicTile(newpath, folder, path, basepath):
    '''
    Using gdalmerge.py the EPSG:4326 GeoTiffs are mosaiced together to create a complete map of 
    the specified date.
    
    '''
    for j in os.listdir(path):
        if ".tif" in j:
            print "Removing {}".format(j)
            os.remove(j)
    os.chdir(newpath)
    gdalMerge = ['gdal_merge.py', '-ul_lr', '-127.829404882663', '49.9999999955068',
                 '-59.0520773226612', '5.17713995546022', '-n', '-3000', '-a_nodata', '-3000', '-o',
                 '{0}.tif'.format(os.path.join(basepath, folder))]
    print "Merging {}".format(folder)
    for image in os.listdir('.'):
        if ".tif" in image and ".aux.xml" not in image and ".DS_Store" not in image:
            gdalMerge.append(os.path.join(newpath, image))
    subprocess.call(gdalMerge)


def createTiles():
    ''' 
    Function to create list of tiles to download.
    In this case, MODIS tiles around lower 48 and central america are downloaded
    Tiles are based on sinusoidal projection by NASA
    
    '''

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


def createDates(startyear, endyear):
    '''
    Function to create list of dates in the format for pyModis to ingest

    '''
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


def getDeltas(dates):
    '''
    Create list of days between the monthly date 

    '''
    comma_date = []
    end_date = []
    for d in range(0, len(dates)):
        comma_date.append(dates[d].replace("-", ","))
    for cd in range(0, len(comma_date)):
        if cd != len(comma_date) - 1:
            a_split = map(int, comma_date[cd].split(','))
            a = date(a_split[0], a_split[1], a_split[2])
            end_date.append(a)

    return end_date


def main():
    '''
    This program will produce GeoTiff files of the MODIS files specified in date range.
    Currently it is limited to MOD13A3.006
    :return:
    '''
    startyear = input("Enter start year: ")
    endyear = input("Enter end year: ")

    foldernames, dates = createDates(startyear, endyear)
    tilelist = ','.join(createTiles())
    basepath = os.getcwd()
    end_date = getDeltas(dates)
    print end_date
    makeFolder(basepath, foldernames)
    mod_path = os.getcwd()
    print mod_path
    for i in range(0, len(dates)):
        if i != len(dates) - 1:
            work_path = os.path.join(mod_path, foldernames[i + 1])
            performDownload(tilelist, dates, i, work_path)
            processHDF(foldernames[i + 1], work_path)
            new_path = reprojectTile(work_path, end_date, i)
            mosaicTile(new_path, foldernames[i + 1], work_path, mod_path)


if __name__ == '__main__':
    main()
