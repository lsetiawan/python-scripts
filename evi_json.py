# /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time, calendar, datetime
import os
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

def create_vars(variable, files, evi_mins,evi_max,month, path):
    # PRISM data
    baseurl = "http://data.nanoos.org/files/cz/mapoverlays/"
    evi_tick1 = ["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"]
    evi_units1 = "Enhanced Vegetation Index"


    tick_marks1 = []
    units1 = []
    colormap = ""
    colorbar_url = ""
    datamin = dict()
    datamax = dict()

    # values
    if variable == "EVI":
        tick_marks1 = evi_tick1
        units1 = evi_units1
        colorbar_url = os.path.join(baseurl,"evi_colorbar.png")
        colormap = "evi_colorbar"
        datamin = evi_mins[files.replace(".png",".tif")]
        datamax = evi_max[files.replace(".png",".tif")]

    month = month
    bounds = [-125.021,-66.479,24.062,49.938]
    image_url = os.path.join(baseurl,files)
    variable = variable

    if variable == "EVI":
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
    ts = time.time()
    model_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
    key = month
    bbox = bounds
    creation_timestamp = calendar.timegm(time.gmtime())
    image_url = image_url
    var = variable

    return legends, colormap, colormap_long_pixels, values, model_date, key, colormap_short_pixels, bbox, creation_timestamp, image_url, colorbar_url, var

def getminmax(prop):
    evi_mins = dict()
    evi_max = dict()

    if prop == "evi":
        os.chdir('/Users/lsetiawan/Desktop/shared_ubuntu/MODIS/EVI_climatology')
        for files in os.listdir("."):
            if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
                src = gdal.Open(files)
                raw_data = src.GetRasterBand(1)
                evi_mins[files] = raw_data.GetMinimum()
                evi_max[files] = raw_data.GetMaximum()
        return evi_mins, evi_max

def main():
    #path = raw_input("Where are your PNG's located: ")
    path = "/Users/lsetiawan/PycharmProjects/Global_Climatology/EVI_png"
    fev = open('evi_climatology.json', 'w')
    evi_climatology = []

    month = ""
    evi_mins, evi_max = getminmax("evi")
    for files in os.listdir(path):
        if "EVI" in files and ".DS_Store" not in files and ".aux.xml" not in files:
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
            var = create_vars("EVI", files, evi_mins,
                              evi_max, month, path)


            evi_climatology.append(create_json(legends, colormap,
                                           colormap_long_pixels, values,
                                           model_date, key, colormap_short_pixels, bbox,
                                           creation_timestamp, image_url, colorbar_url, var))

    fev.write(json.dumps(evi_climatology, sort_keys=False, indent=4, separators=(',', ': ')))
    print(json.dumps(evi_climatology, sort_keys=False,indent=4, separators=(',', ': ')))
    fev.close()

if __name__ == '__main__':
    main()