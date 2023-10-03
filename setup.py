# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 14:24:49 2022

@author: juarez
"""
import sys, os
from cx_Freeze import setup, Executable


company_name = "Qualcomm"
product_name = "On_Wafer Harmonics Measurement System"
#Create Calibration Folder
current_directory = os.getcwd()
folder_name_to_create = "CALIBRATION_FILES"
create_folder_path = os.path.join(current_directory,folder_name_to_create)
try:
    os.makedirs(create_folder_path)
except:
    pass

options = {"build_exe":{"includes": 'atexit'}}

#Windows Base Application
base = None
if sys.platform == 'win32':
    base = "Win32GUI"

exe = Executable(script = r"harmonics_system_UI_4.py",
                 # base = base,
                 base = None,
                 icon = "icon_for_harmonics.ico",
                 )

setup(name="HARMONICS SYSTEM",
      version='2.0.0',
      description="On-Wafer Harmonics Measurement System",
      executables = [exe],
     )