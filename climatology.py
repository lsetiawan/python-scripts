#!/usr/bin/env python
import os,subprocess,shutil,string
import gdal
import numpy as np
gdal.UseExceptions()

def sort_to_folder(path,months,path1):
	print path
	tif = ".tif"
	for i in range(0,len(months)):
		print "Working on " + months[i][1]
		for files in os.listdir(path):
			if tif in files and months[i][0] in files and ".aux.xml" not in files:
				mvpath = os.path.join(path1,months[i][2])
				print files
				shutil.move(files,os.path.join(mvpath,files))
			else:
				pass
			
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

def rasterCalc(path,months,climatology,whichProp,userInput):
	print path
	if not os.path.exists(climatology):
		os.makedirs(climatology)
	
	data = []
	arrays = []
	
	for i in range(0,len(months)):
		os.chdir(os.path.join(path,months[i][2]))
		print os.getcwd()

		for files in os.listdir('.'):
			if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
				data.append(gdal.Open(files))
		dataTotal = len(data)
		print "There are {} files".format(dataTotal)
		
		for j in range(0,dataTotal):
			arrays.append(np.array(data[j].ReadAsArray()))
		
		meanArray = np.mean(arrays,axis=0)
		
		#Get data about original files
		[cols,rows] = arrays[0].shape
		trans = data[0].GetGeoTransform()
		proj = data[0].GetProjection()
		nodataval = data[0].GetRasterBand(1).GetNoDataValue()
		print [cols,rows]
		print trans
		print proj
		print nodataval
		
		# Convert Array into GeoTiff
		outfile = os.path.join(climatology,"{0}_{1}.tif".format(whichProp,months[i][2]))
		outdriver = gdal.GetDriverByName("GTiff")
		outdata = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)
		outdata.GetRasterBand(1).WriteArray(meanArray)
		if nodataval == None and userInput == "MOD13A3":
			outdata.GetRasterBand(1).SetNoDataValue(-3000)
		elif nodataval == None and userInput == "PRISM":
			outdata.GetRasterBand(1).SetNoDataValue(-9999)
		else:
			outdata.GetRasterBand(1).SetNoDataValue(nodataval)
		outdata.SetGeoTransform(trans)
		outdata.SetProjection(proj)
		
		data = []
		arrays = []
		
	data = None
	outdata = None
	
	if userInput == "MOD13A3":
		finalClip(climatology)

def finalClip(climatology):
	os.chdir(climatology)
	directory = "EVI_Final"
	if not os.path.exists(directory):
		os.makedirs(directory)
	for files in os.listdir('.'):
		if "EVI_Final" not in files:
			subprocess.call(['gdal_translate', '-projwin', '-127.829', '49.9184', 
			'-59.0521', '5.17714', '-of', 'GTiff', files, os.path.join(directory,files)])
		
	


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
		desired_path = "MOD13A3_TIF_epsg4326"
		whichProp = "EVI"
		path1 = os.path.join(os.getcwd(),whichProp)
		climatology = os.path.join(os.getcwd(),"{0}{1}".format(whichProp,"_climatology"))
		make_folder(os.path.join(os.getcwd(),desired_path))
		sort_to_folder(os.getcwd(),months,path1)
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
