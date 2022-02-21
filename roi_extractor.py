import os
import sys
import syglass as sy
from syglass import pyglass
import numpy as np
import tifffile
import subprocess
import tkinter as tk

returnString = ""

def extract_roi(project, projectPath, roi_index): 
	head, tail = os.path.split(projectPath)

	os.chdir(os.path.dirname(projectPath))
	roi_block = project.get_roi_data(int(roi_index))
	roi_mask = project.get_mask(int(roi_index))
	print(roi_mask.data.dtype)
	if roi_block.data.shape == (0, 0, 0, 1):
		print("No ROI detected for that number, please double check the ROI number!")
	else:
		tifffile.imsave(projectPath[:-4] + "_ROI_" + str(roi_index) + "_rawData.tiff", roi_block.data)
		tifffile.imsave(projectPath[:-4] + "_ROI_" + str(roi_index) +"._integerLabels.tiff", roi_mask.data)
		subprocess.run(['explorer', head])

def get_roi_number():
	root=tk.Tk()
	mystring = tk.StringVar()
	def getvalue():
		global returnString 
		returnString = mystring.get()
		root.destroy()
	tk.Label(root, text="ROI #").grid(row=0)  #label
	tk.Entry(root, textvariable = mystring).grid(row=0, column=1) #entry textbox
	tk.WSignUp = tk.Button(root, text="Extract", command=getvalue).grid(row=3, column=0) #button
	root.mainloop()

def main(args):
	print("ROI Extractor, by Michael Morehead")
	print("Attempts to extract a specific ROI volume from a syGlass project")
	print("and write it to a series of TIFF files")
	print("---------------------------------------")
	print("Usage: Highlight a project and use the Script Launcher in syGlass.")
	print("---------------------------------------")
	
	projectList = args["selected_projects"]

	doExtract = True
	if len(projectList) < 1:
		print("Highlight a project before running to select a project!")
		doExtract = False
	
	if len(projectList) > 1:
		print("This script only supports 1 project at a time, please select only one project before running.")
		doExtract = False
	
	if doExtract:
		project = projectList[0]
		projectPath = project.get_path_to_syg_file().string()
		get_roi_number()
		global returnString
		print("Extracting ROI " + str(returnString) + " from: " + projectPath)
		extract_roi(project, projectPath, returnString)