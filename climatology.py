#!/usr/bin/env python
import os,subprocess,shutil,string

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

def rasterCalc(path,months,alphabet,climatology,whichProp,origin):
	print path
	print months
	print alphabet
	calcSUM = " "
	for i in range(0,len(months)):
		os.chdir(os.path.join(path,months[i][2]))
		print os.getcwd()
		if not os.path.exists(os.path.join(climatology,months[i][1])):
			os.makedirs(os.path.join(climatology,months[i][1]))
		#for j in range(0,len(os.listdir('.'))):
		#	print j
		Alpha = []
		addAlpha = []
		filelist = []
		addition = []
		filenum = []

		for files in os.listdir('.'):
			if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
				filenum.append(files)
		print "There are {} files".format(len(filenum))
		length = len(filenum)
		if length > 25:
			for j in range(0,len(filenum),26):
				for k in range(0,26):
					if j + k < len(filenum):
						newfile = "-{0} {1}".format(alphabet[k],filenum[j+k])
						filelist.append(newfile)
						Alpha.append("{}".format(alphabet[k]))
		
		for m in range(0,len(filelist),26):
			addition.append(filelist[m:26+m])
			addAlpha.append(Alpha[m:26+m])
		
		for l in range(0,len(addition)):
			strlist_file = ' '.join(addition[l])
			strlist_calc = '+'.join(addAlpha[l])
			calcSUM = "({0})".format(strlist_calc)	
			print calcSUM
			print strlist_file
			print calcSUM
			os.system("gdal_calc.py {0} {1} {2} {3} {4} {5} {6}".\
				format(strlist_file,"--outfile={0}{1}_{2}.tif".format(os.path.join(os.path.join(climatology,months[i][1]),"{}_".format(whichProp)),months[i][1],l),
					"--calc=\"{}\"".format(calcSUM),"--NoDataValue=-3.4028234663852886e+38",
					"--type=Float32","--overwrite","--NoDataValue=-9999"))

	rasterMean(climatology,months,alphabet,calcSUM,length,whichProp)

def rasterMean(path,months,alphabet,calcSUM,length,whichProp):
	os.chdir(path)
	fileArray = []
	alphaArray = []
	alphaAdd = []
	for i in range(0,len(months)):
		os.chdir(os.path.join(path,months[i][1]))
		for files in os.listdir('.'):
			if ".tif" in files and ".aux.xml" not in files and ".DS_Store" not in files:
				fileArray.append(files)
		for j in range(0,len(fileArray)):
			alphaArray.append("-{0} {1}".format(alphabet[j],fileArray[j]))
			alphaAdd.append("{}".format(alphabet[j]))
		for l in range(0,len(alphaArray)):
			strlist_file = ' '.join(alphaArray[l])
			strlist_calc = '+'.join(alphaAdd[l])
			calcSUM = "({0})/{1}".format(strlist_calc,length)	
			print calcSUM
			print strlist_file
			print calcSUM
			os.system("gdal_calc.py {0} {1} {2} {3} {4} {5} {6}".\
				format(strlist_file,"--outfile={0}{1}_{2}.tif".format(os.path.join(path,"{}_".format(whichProp)),months[i][1],l),
					"--calc=\"{}\"".format(calcSUM),"--NoDataValue=-3.4028234663852886e+38",
					"--type=Float32","--overwrite","--NoDataValue=-9999"))
			

	os.chdir(path)
	
	print fileArray

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
		alphabet = list(string.ascii_uppercase)
		desired_path = "MOD13A3_TIF_epsg4326"
		make_folder(os.path.join(os.getcwd(),desired_path))
		sort_to_folder(os.getcwd(),months)
		rasterCalc(os.getcwd(),months,alphabet)
	if userInput == "PRISM":
		alphabet = list(string.ascii_uppercase)
		origin = os.path.join(os.getcwd(),"PRISM")
		os.chdir(os.path.join(os.getcwd(),"PRISM"))
		whichProp = raw_input("Which property would you like? [ppt or tmean]: ")
		path1 = os.path.join(os.getcwd(),whichProp)
		climatology = os.path.join(os.getcwd(),"{0}{1}".format(whichProp,"_climatology"))
		make_folder(os.path.join(path1))
		goFolder(os.getcwd(),path1,months)
		#rasterCalc(os.getcwd(),months,alphabet,climatology,whichProp,origin)
	
if __name__ == '__main__' :
	main()
