#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time, calendar, datetime
import os

def create_json(forecast_date, model_date, image_url, forecast_end_date, creation_timestamp, forecast_start_date,
                legends,values):

    # Some variables
    colormap = "liqing"
    colorbar_url = "http://data.nanoos.org/files/goaon/mapoverlays/arag_colorbar.png"
    colormap_long_pixels = 256
    colormap_short_pixels = 16
    var = "aragonite"
    bbox = [-181, 179, -85, 85]

    # Create main JSON keys
    mainkey = dict()
    if legends != "":
        mainkey["legends"] = legends
    if forecast_date != "":
        mainkey["forecast_date"] = forecast_date
    if colormap != "":
        mainkey["colormap"] = colormap
    if colorbar_url != "":
        mainkey["colorbar_url"] = colorbar_url
    if model_date != "":
        mainkey["model_date"] = model_date
    if colormap_long_pixels != "":
        mainkey["colormap_long_pixels"] = colormap_long_pixels
    # FOR MULTIPLE DEPTH
    #if images != "":
    #    mainkey["images"] = images
    if values != "":
        mainkey["values"] = values
    if image_url != "":
        mainkey["image_url"] = image_url
    if colormap_short_pixels != "":
        mainkey["colormap_short_pixels"] = colormap_short_pixels
    if bbox != "":
        mainkey["bbox"] = bbox
    if var != "":
        mainkey["var"] = var
    if forecast_end_date != "":
        mainkey["forecast_end_date"] = forecast_end_date
    if creation_timestamp != "":
        mainkey["creation_timestamp"] = creation_timestamp
    if forecast_start_date != "":
        mainkey["forecast_start_date"] = forecast_start_date
    return mainkey

def imagesURL(p, pth):
    images1 = []
    images2 = []
    images3 = []

    baseurl = "http://data.nanoos.org/files/goaon/mapoverlays/"
    for png in os.listdir(pth):
        for d in p:
            if ".DS_Store" not in png:
                spt = png.split("_")
                if "{}dbar".format(d) in spt and "8699" in spt:
                    url = os.path.join(baseurl,png)
                    key = "{}dbar".format(d)
                    img = {
                        'url': '{}'.format(url),
                        'key': '{}'.format(key)
                    }
                    images1.append(img)

                if "{}dbar".format(d) in spt and "0013" in spt:
                    url = os.path.join(baseurl, png)
                    key = "{}dbar".format(d)
                    img = {
                        'url': '{}'.format(url),
                        'key': '{}'.format(key)
                    }
                    images2.append(img)

                if "{}dbar".format(d) in spt and "7213" in spt:
                    url = os.path.join(baseurl, png)
                    key = "{}dbar".format(d)
                    img = {
                        'url': '{}'.format(url),
                        'key': '{}'.format(key)
                    }
                    images3.append(img)
    images = images1, images2, images3
    return images

def dates(year):
    ts = time.time()
    # Create vars for forecast stuff
    forecast_date = ""
    forecast_start_date = ""
    forecast_end_date = ""

    creation_timestamp = calendar.timegm(time.gmtime())
    model_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
    if year == "8699":
        forecast_date = "1986-01-01T00:00:00Z"
        forecast_start_date = "1986-01-01T00:00:00Z"
        forecast_end_date = "1999-01-01T00:00:00Z"
    if year == "0013":
        forecast_date = "2000-01-01T00:00:00Z"
        forecast_start_date = "2000-01-01T00:00:00Z"
        forecast_end_date = "2013-01-01T00:00:00Z"
    if year == "7213":
        forecast_date = "1972-01-01T00:00:00Z"
        forecast_start_date = "1972-01-01T00:00:00Z"
        forecast_end_date = "2013-01-01T00:00:00Z"

    return forecast_date,forecast_start_date,forecast_end_date,creation_timestamp,model_date

def legends():
    # Setting units and tickmarks
    units1 = "Aragonite Saturation State"
    units2 = units1
    tick_marks1 = [0,1,2,3,4,5]
    tick_marks2 = tick_marks1

    # main keys
    legend = {
        "v1": {
            "units": units1,
            "colormap_tick_labels": {
                "0.0": "{}".format(tick_marks1[0]),
                "0.1": "",
                "0.2": "{}".format(tick_marks1[1]),
                "0.3": "",
                "0.4": "{}".format(tick_marks1[2]),
                "0.5": "",
                "0.6": "{}".format(tick_marks1[3]),
                "0.7": "",
                "0.8": "{}".format(tick_marks1[4]),
                "0.9": "",
                "1.0": "{}".format(tick_marks1[5])
            }
        },
        "v2": {
            "units": units2,
            "colormap_tick_labels": {
                "0.0": "{}".format(tick_marks2[0]),
                "0.1": "",
                "0.2": "{}".format(tick_marks2[1]),
                "0.3": "",
                "0.4": "{}".format(tick_marks2[2]),
                "0.5": "",
                "0.6": "{}".format(tick_marks2[3]),
                "0.7": "",
                "0.8": "{}".format(tick_marks2[4]),
                "0.9": "",
                "1.0": "{}".format(tick_marks2[5])
            }
        },
        "default": "v1"
    }

    return legend

def main():
    pth = "/Users/lsetiawan/PycharmProjects/Global_Climatology/arag_climatology"
    p = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300,
         1400, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500]
    #arag_climatology = []

    # FOR DEPTH 0 and 200 ###########################
    arag_climatology1 = []
    arag_climatology2 = []
    fr1 = open('min_max_86_99.txt', 'r')
    fr2 = open('min_max_00_13.txt', 'r')
    s1 = fr1.read()
    s2 = fr2.read()
    fr1.close()
    fr2.close()

    array1 = s1.split(";")
    array2 = s2.split(";")

    split1 = []
    for ii in range(0, len(array1)):
        split1.append(array1[ii].split(","))
    split2 = []
    for jj in range(0, len(array2)):
        split2.append(array2[jj].split(","))

    year = ["8699", "0013", "7213"]
    baseurl = "http://data.nanoos.org/files/goaon/mapoverlays/"
    for png in os.listdir(pth):
        if ".DS_Store" not in png:
            spt = png.split("_")
            if "{}dbar".format(0) in spt:
                for y in range(0,len(year)):
                    for n in range(0, len(split1)):
                        if year[y] in spt and "0dbar" in split1[n] and year[y] in split1[n]:
                            legend = legends()
                            image_url = os.path.join(baseurl, png)
                            values = {
                                "min": "{}".format(split1[n][2]),
                                "max": "{}".format(split1[n][3])
                            }
                            forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(year[y])
                            arag_climatology1.append(create_json(forecast_date, model_date, image_url, forecast_end_date,
                                                                creation_timestamp, forecast_start_date, legend, values))
                        if year[y] in spt and "0dbar" in split2[n] and year[y] in split2[n]:
                            legend = legends()
                            image_url = os.path.join(baseurl, png)
                            values = {
                                "min": "{}".format(split2[n][2]),
                                "max": "{}".format(split2[n][3])
                            }
                            forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(year[y])
                            arag_climatology1.append(create_json(forecast_date, model_date, image_url, forecast_end_date,
                                                                 creation_timestamp, forecast_start_date, legend, values))
            if "{}dbar".format(200) in spt:
                for y in range(0, len(year)):
                    for n in range(0, len(split1)):
                        if year[y] in spt and "200dbar" in split1[n] and year[y] in split1[n]:
                            legend = legends()
                            image_url = os.path.join(baseurl, png)
                            values = {
                                "min": "{}".format(split1[n][2]),
                                "max": "{}".format(split1[n][3])
                            }
                            forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(
                                year[y])
                            arag_climatology2.append(create_json(forecast_date, model_date, image_url,
                                                                 forecast_end_date, creation_timestamp,
                                                                 forecast_start_date, legend,values))
                        if year[y] in spt and "200dbar" in split2[n] and year[y] in split2[n]:
                            legend = legends()
                            image_url = os.path.join(baseurl, png)
                            values = {
                                "min": "{}".format(split2[n][2]),
                                "max": "{}".format(split2[n][3])
                            }
                            forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(
                                year[y])
                            arag_climatology2.append(create_json(forecast_date, model_date, image_url,
                                                                 forecast_end_date, creation_timestamp,
                                                                 forecast_start_date, legend, values))
    ########################################################################################################
    ##### FOR MULTIPLE DEPTH ##################################################################################
    images = imagesURL(p,pth)
    '''for i in range(0,len(images)):
        legend = legends()
        year = ["8699","0013","7213"]
        forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(year[i])
        arag_climatology.append(create_json(forecast_date, model_date, images[i], forecast_end_date,
                                            creation_timestamp,forecast_start_date,legend))'''
    #######################################################################################################

    f0 = open("arag_0dbar.json", 'w')
    f200 = open("arag_200dbar.json", 'w')
    #print json.dumps(arag_climatology1, sort_keys=False, indent=4, separators=(',', ': '))
    f0.write(json.dumps(arag_climatology1, sort_keys=False, indent=4, separators=(',', ': ')))
    #print json.dumps(arag_climatology2, sort_keys=False, indent=4, separators=(',', ': '))
    f200.write(json.dumps(arag_climatology2, sort_keys=False, indent=4, separators=(',', ': ')))

    f0.close()
    f200.close()


if __name__ == '__main__':
    main()