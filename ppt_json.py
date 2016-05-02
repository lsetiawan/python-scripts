# /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time, calendar
import os
import rasterio as rio
import numpy as np
import gdal

def create_json(legends, colormap, colormap_long_pixels, 
    values, model_date, key, colormap_short_pixels, bbox, 
    creation_timestamp, image_url, colorbar_url, var):
    mainkey = dict()
    if legends != "":
        mainkey["legends"] = legends
    if colormap != "":
        mainkey["colormap"] = colormap
    if colormap_long_pixels != "":
        mainkey["colormap_long_pixels"] = colormap_long_pixels
    if values!= "":
        mainkey["values"] = values
    if model_date != "":
        mainkey["model_date"] = model_date
    if key != "":
        mainkey["key"] = key
    if colormap_short_pixels != "":
        mainkey["colormap_short_pixels"] = colormap_short_pixels
    if bbox != "":
        mainkey["bbox"] = bbox
    if creation_timestamp != "":
        mainkey["creation_timestamp"] = creation_timestamp
    if image_url != "":
        mainkey["image_url"] = image_url
    if colorbar_url != "":
        mainkey["colorbar_url"] = colorbar_url
    if var != "":
        mainkey["var"] = var

    return mainkey

def create_vars(variable, files, ppt_mins,ppt_max,tmean_mins,tmean_max,month, path):
    # PRISM data
    baseurl = "http://data.nanoos.org/files/cz/mapoverlays/"
    ppt_tick1 = ["0", "40", "80", "120", "160", "500"]
    ppt_units1 = "Precipitation (mm/month)"
    ppt_tick2 = ["0.0", "1.6", "3.1", "4.7", "6.3", "19.7"]
    ppt_units2 = "Precipitation (inches/month)"
    
    tmean_tick1 = ["-20", "-5", "5", "15", "25", "40"]
    tmean_units1 = "Air Temperature (°C)"
    tmean_tick2 = ["-4", "23", "41", "59", "77", "104"]
    tmean_units2 = "Air Temperature (°F)"

    tick_marks1 = []
    units1 = []
    colormap = ""
    units2 = []
    tick_marks2 = []
    colorbar_url = ""
    datamin = dict()
    datamax = dict()

    # values
    if variable == "Precipitation":
        tick_marks1 = ppt_tick1
        units1 = ppt_units1
        colorbar_url = os.path.join(baseurl,"ppt_colorbar.png")
        colormap = "ppt_colorbar"
        datamin = ppt_mins[files.replace(".png",".tif")]
        datamax = ppt_max[files.replace(".png",".tif")]
    if variable == "Mean Air Temperature":
        tick_marks1 = tmean_tick1
        units1 = tmean_units1
        colorbar_url = os.path.join(baseurl,"tmean_colorbar.png")
        colormap = "tmean_colorbar"
        datamin = tmean_mins[files.replace(".png",".tif")]
        datamax = tmean_max[files.replace(".png",".tif")]

    date = "2016-03-25T00:00:00Z"
    month = month
    bounds = [-125.021,-66.479,24.062,49.938]
    image_url = os.path.join(baseurl,files)
    variable = variable
    same_version = True

    if variable == "Precipitation" or variable == "Mean Air Temperature":
        same_version = False
        if variable == "Precipitation":
            tick_marks2 = ppt_tick2
            units2 = ppt_units2
        else:
            tick_marks2 = tmean_tick2
            units2 = tmean_units2
    
    if same_version == True:
        tick_marks2 = tick_marks1
        units2 = units1


    # main keys
    legends = {
         "v1": {
            "units":"{}".format(units1),
            "colormap_tick_labels":{
               "0.0":"{}".format(tick_marks1[0]),
               "0.1":"",
               "0.2":"{}".format(tick_marks1[1]),
               "0.3":"",
               "0.4":"{}".format(tick_marks1[2]),
               "0.5":"",
               "0.6":"{}".format(tick_marks1[3]),
               "0.7":"",
               "0.8":"{}".format(tick_marks1[4]),
               "0.9":"",
               "1.0":"{}".format(tick_marks1[5])
            }
         },
         "v2":{
            "units":"{}".format(units2),
            "colormap_tick_labels":{
               "0.0":"{}".format(tick_marks2[0]),
               "0.1":"",
               "0.2":"{}".format(tick_marks2[1]),
               "0.3":"",
               "0.4":"{}".format(tick_marks2[2]),
               "0.5":"",
               "0.6":"{}".format(tick_marks2[3]),
               "0.7":"",
               "0.8":"{}".format(tick_marks2[4]),
               "0.9":"",
               "1.0":"{}".format(tick_marks2[5])
            }    
        },
         "default":"v1"
      }
    colormap = colormap
    colormap_long_pixels = 256
    colormap_short_pixels = 16
    colorbar_url = colorbar_url
    values = {
         "min":datamin,
         "max":datamax
      }
    model_date = date
    key = month
    bbox = bounds
    creation_timestamp = calendar.timegm(time.gmtime())
    image_url = image_url
    var = variable

    return legends, colormap, colormap_long_pixels, values, model_date, key, colormap_short_pixels, bbox, creation_timestamp, image_url, colorbar_url, var

def getminmax(prop):
    ppt_mins = dict()
    ppt_max = dict()
    tmean_mins = dict()
    tmean_max = dict()

    if prop == "ppt":
        os.chdir('/Users/lsetiawan/Desktop/shared_ubuntu/APL/PRISM/ppt_climatology')
        for files in os.listdir("."):
            if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
                src = gdal.Open(files)
                raw_data = src.GetRasterBand(1)
                ppt_mins[files] = raw_data.GetMinimum()
                ppt_max[files] = raw_data.GetMaximum()
        return ppt_mins, ppt_max
    if prop == "tmean":
        os.chdir('/Users/lsetiawan/Desktop/shared_ubuntu/APL/PRISM/tmean_climatology')
        for files in os.listdir("."):
            if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
                src = gdal.Open(files)
                raw_data = src.GetRasterBand(1)
                tmean_mins[files] = raw_data.GetMinimum()
                tmean_max[files] = raw_data.GetMaximum()
        return tmean_mins, tmean_max

def main():
    path = raw_input("Where are your PNG's located: ")
    # /Users/lsetiawan/Desktop/shared_ubuntu/APL/PRISM/PRISM_png
    fp = open('ppt_climatology.json', 'w')
    ft = open('tmean_climatology.json', 'w')
    ppt_climatology = []
    tmean_climatology = []
    month = ""
    ppt_mins, ppt_max = getminmax("ppt")
    tmean_mins, tmean_max = getminmax("tmean")
    for files in os.listdir(path):
        if "ppt" in files and ".DS_Store" not in files:
            print files
            if "01" in files:
                month = "January"
            elif "02" in files:
                month = "February"
            elif "03" in files:
                month = "March"
            elif "04" in files:
                month = "April"
            elif "05" in files:
                month = "May"
            elif "06" in files:
                month = "June"
            elif "07" in files:
                month = "July"
            elif "08" in files:
                month = "August"
            elif "09" in files:
                month = "September"
            elif "10" in files:
                month = "October"
            elif "11" in files:
                month = "November"
            elif "12" in files:
                month = "December"
            legends, colormap, colormap_long_pixels, \
            values, model_date, key, colormap_short_pixels, \
            bbox, creation_timestamp, image_url, colorbar_url, \
            var = create_vars("Precipitation", files, ppt_mins,
                              ppt_max, tmean_mins, tmean_max, month, path)


            ppt_climatology.append(create_json(legends, colormap,
                                           colormap_long_pixels, values,
                                           model_date, key, colormap_short_pixels, bbox,
                                           creation_timestamp, image_url, colorbar_url, var))

        if "tmean" in files and ".DS_Store" not in files:
            print files
            if "01" in files:
                month = "January"
            elif "02" in files:
                month = "February"
            elif "03" in files:
                month = "March"
            elif "04" in files:
                month = "April"
            elif "05" in files:
                month = "May"
            elif "06" in files:
                month = "June"
            elif "07" in files:
                month = "July"
            elif "08" in files:
                month = "August"
            elif "09" in files:
                month = "September"
            elif "10" in files:
                month = "October"
            elif "11" in files:
                month = "November"
            elif "12" in files:
                month = "December"
            legends, colormap, colormap_long_pixels, \
            values, model_date, key, colormap_short_pixels, \
            bbox, creation_timestamp, image_url, colorbar_url, \
            var = create_vars("Mean Air Temperature", files, ppt_mins,
                              ppt_max, tmean_mins, tmean_max, month, path)

            tmean_climatology.append(create_json(legends, colormap,
                                   colormap_long_pixels, values,
                                   model_date, key, colormap_short_pixels, bbox,
                                   creation_timestamp, image_url, colorbar_url, var))
    fp.write(json.dumps(ppt_climatology, sort_keys=False, indent=4, separators=(',', ': ')))
    ft.write(json.dumps(tmean_climatology, sort_keys=False,indent=4, separators=(',', ': ')))
    print(json.dumps(ppt_climatology, sort_keys=False,indent=4, separators=(',', ': ')))
    print(json.dumps(tmean_climatology, sort_keys=False,indent=4, separators=(',', ': ')))
    fp.close()
    ft.close()

if __name__ == '__main__':
    main()



