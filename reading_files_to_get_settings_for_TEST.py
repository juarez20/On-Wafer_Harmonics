# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:15:18 2023

@author: iolab
"""
import os
import csv

# =============================================================================
# The following function will take a name of a file as an argument.
# this file will be assigned by user at the User Interface level. 
# These are the conditions that the test will run.
# =============================================================================
def get_conditions_from_DUT_Setups_files(get_conditions_test_file):
    get_the_current_path = os.getcwd()
    dut_setups_folder = "TEST_SEQUENCES"
    construct_folder = os.path.join(get_the_current_path, dut_setups_folder)
    get_the_file = os.path.join(construct_folder, get_conditions_test_file + str(".txt"))

    v_right = v_center = v_left = ""
    power_levels_sequence = []
    
    if os.path.isfile(get_the_file):
        with open(get_the_file) as get_file:
            get_conditions_from_file = csv.reader(get_file)
            
            for each_value_read in get_conditions_from_file:
                if each_value_read[0] == 'v_right':
                    v_right = each_value_read[1]
                if each_value_read[0] == 'v_center':
                    v_center = each_value_read[1]
                if each_value_read[0] == 'v_left':
                    v_left = each_value_read[1]
                    
                if "P" in each_value_read[0] or "p" in each_value_read[0]:
                    fix_value =  each_value_read[1]
                    if "\t" in str(fix_value):
                        fix_value = fix_value.replace("\t", '')
                        power_levels_sequence.append(fix_value)
                    else:
                        power_levels_sequence.append(fix_value)
                
        return v_right, v_center, v_left, power_levels_sequence
    else:
        return None


# =============================================================================
# The following function will help us to get the list of files 
# available in the folder "TEST_SEQUENCES"
# In this folder will reside all the text files containing the 
# conditions to test. The power levels and voltages.
# notice that there are no arguments but the function
# does return a list of names of each file present as long as 
# it is in text file format.
# =============================================================================
def get_all_the_name_of_the_files_for_the_SETUPs():
    get_the_current_path = os.getcwd()
    dut_setups_folder = "TEST_SEQUENCES"
    dut_setups_folder = os.path.join(get_the_current_path, dut_setups_folder)
    list_of_files_SETUPS = []
    
    for each_file in os.listdir(dut_setups_folder):
        if ".txt" in each_file:
            each_file = os.path.splitext(each_file)
            list_of_files_SETUPS.append(each_file[0])
       
    if len(list_of_files_SETUPS) > 0:
        return list_of_files_SETUPS
    else:
        return None