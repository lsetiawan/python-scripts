#!/usr/bin/env python
import os,subprocess,shutil,string
import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, RESAMPLING
from rasterio import crs
import numpy as np
gdal.UseExceptions()

# Sort tif files to designated months
def sort_to_folder(path,months):
	print path
	tif = ".tif"
	for i in range(0,len(months)):
		print "Working on " + months[i][1]
		for files in os.listdir(path):
			if tif in files and months[i][0] in files and ".aux.xml" not in files:
				mvpath = os.path.join(path,months[i][2])
				print files
				shutil.move(files,os.path.join(mvpath,files))
			else:
				pass

# Make folders for each month of the year		
def make_folder(path):
	os.chdir(path)
	for month in range(1,13):
		if month < 10:
			directory = "0"+ str(month)
			if not os.path.exists(directory):
				print "Creating Directory: 0" + str(month)
				os.makedirs(directory)
		if month >= 10:
			directory = str(month)
			if not os.path.exists(directory):
				print "Creating Directory: " + str(month)
				os.makedirs(directory)

# Calculate climatology
def rasterCalc(path,months,climatology,whichProp,userInput):
	print path
	if not os.path.exists(climatology):
		os.makedirs(climatology)
	
	for i in range(0,len(months)):
		os.chdir(os.path.join(path,months[i][2]))
		print os.getcwd()
		data = []
		arrays = []
		for files in os.listdir('.'):
			if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
				data.append(rio.open(files))
		dataTotal = len(data)
		print "There are {} files".format(dataTotal)
		
		for j in range(0,dataTotal):
			raw_data = data[j].read(1)
			arrays.append(np.where(raw_data == -3000, np.nan, raw_data))

		meanArray = np.nanmean(arrays,axis=0)
		final_array = np.where(meanArray == np.nan, -3000, raw_data)
		#Get data about original files
		cols = data[0].width
		rows = data[0].height
		trans = data[0].affine
		proj = data[0].crs
		profile = data[0].profile
		print [cols,rows]
		print trans
		print proj
		print profile
		outfile = os.path.join(climatology,"{0}_{1}.tif".format(whichProp,months[i][2]))

		dst_crs = crs.from_string("EPSG:4326")

		with rio.drivers():
			profile.update({
	            'crs': dst_crs,
	            'transform': trans,
	            'affine': trans,
	            'width': cols,
	            'height': rows
	        })

			# Convert Array into GeoTiff
			with rio.open(outfile, 'w', **profile) as dst:
				dst_array = np.empty((rows, cols), dtype='int16')
				reproject(
	                    # Source parameters
	                    source=final_array,
	                    src_crs=proj,
	                    src_transform=trans,
	                    # Destination paramaters
	                    destination=dst_array,
	                    dst_transform=trans,
	                    dst_crs=dst_crs,
	                    resampling=RESAMPLING.nearest
	                    )

				dst.write(dst_array, 1)
				print "success"
		
	


## Function for PRISM
def goFolder(path,path1,months):
	for year in range(1895,2017):
		folder1 = "tif"
		folder2 = "epsg4326"
		folder = os.path.join(folder1,folder2)
		
		os.chdir(os.path.join(path,os.path.join(str(year),folder)))
		print year
		print os.getcwd()
		
		sort_to_folder(os.getcwd(),months,path1)
		os.chdir(path1)
		print os.getcwd()

def main():
	userInput = raw_input("What data would you like to work on? [MOD13A3 or PRISM]: ")
	months = [["01_01", "January", "01"], 
			  ["02_01", "February", "02"],
			  ["03_01", "March", "03"],
			  ["04_01", "April", "04"],
			  ["05_01", "May", "05"],
			  ["06_01", "June", "06"],
			  ["07_01", "July", "07"],
			  ["08_01", "August", "08"],
			  ["09_01", "September", "09"],
			  ["10_01", "October", "10"],
			  ["11_01", "November", "11"],
			  ["12_01", "December", "12"]]
	if userInput == "MOD13A3":
		desired_path = "MOD13A3.006"
		whichProp = "EVI"
		climatology = os.path.join(os.getcwd(),"{0}{1}".format(whichProp,"_climatology"))
		make_folder(os.path.join(os.getcwd(),desired_path))
		sort_to_folder(os.getcwd(),months)
		rasterCalc(os.getcwd(),months,climatology,whichProp,userInput)
	if userInput == "PRISM":
		os.chdir(os.path.join(os.getcwd(),"PRISM"))
		whichProp = raw_input("Which property would you like? [ppt or tmean]: ")
		path1 = os.path.join(os.getcwd(),whichProp)
		climatology = os.path.join(os.getcwd(),"{0}{1}".format(whichProp,"_climatology"))
		make_folder(os.path.join(path1))
		goFolder(os.getcwd(),path1,months)
		rasterCalc(os.getcwd(),months,climatology,whichProp,userInput)
	
if __name__ == '__main__' :
	main()
