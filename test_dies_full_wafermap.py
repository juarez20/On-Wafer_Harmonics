# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:07:10 2023

@author: iolab
"""
import pyvisa as visa
import time, os
import instrument_control_commands as inst_control
import calibration_functions_and_readbacks as cal_func
import datetime

rm = visa.ResourceManager()

# =============================================================================
# This function will help to probe all dies available in a wafer loaded region map
# FULL WAFER PROBE MODE
# In this mode, the entire wafer map loaded is being tested
# the program wil go to the first available die. 
# From that die, it will iterate through the entire wafer map. 
# Because the "last die" search does not work as expected, instead, it goes to the last die of the column where it starts. 
# A way to make sure that all the dies are tested, a "tested_devices" holder is being created. 
# This will help us to know when  a die is being tested again. 
# If more than 2 dies are being retested, the program will terminate.
# =============================================================================
def probing_dies_through_entire_wafer_loaded_map(probe_addr, get_subdies_index_and_label, smuAddr, v_left_addr, v_center_addr, v_right_addr, v_left_val, v_center_val, v_right_val, sigGenAddr, Amp, freq, power_level_list, addr_pin, addr_pout, SigAnaAddr, second_harmonics, third_harmonics, user_file_name, userPath, Lot, Wafer, pin_offset_val, pout_offset_val):
    prober_test = rm.open_resource(probe_addr)
    print(prober_test)
    x = prober_test.query("*IDN?")
    print(x)
    # set_on_first_die = prober_test.write(":mov:prob:firs:die")
    # # go_to_the_last_die_on_MAP = test.write(":mov:prob:last:die") this one does not work as expected.... it gets the last die of that column
    # # get_last_position_die = prober_test.query(:"move:prob:abs:die?)
    # get_the_index_position_of_current_die = prober_test.write(":mov:prob:abs:index?") #this one gets the index of the current device... 
    freq = int(freq)
    Amp = float(Amp)
    second_harmonics = float(second_harmonics)
    third_harmonics = float(third_harmonics)
    
    # done_once = False
    prober_test.write(":mov:prob:last:die")
    time.sleep(12)
    get_the_last_die_index = prober_test.query(":mov:prob:abs:index?")
    get_the_last_die_index = int(get_the_last_die_index)
    print("This is the last dies in the sequence.")
    print(get_the_last_die_index)
    
    #creating the file we need to use.
    user_file_name = user_file_name + "_" + str(freq)
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    fullPath = os.path.join(userPath, user_file_name)
    print(fullPath)
    print(timestamp)
    # ip_shv = open(fullPath + "_" + timestamp + ".csv", 'w+')
    # ip_shv.write("Lot, Wafer, Die, Device, Setup, Freq, Pin, Vg, Vb, Pin_act, Pout, IL, Ig, Ib, 2H, 3H\n")
    
    #We set up the table headers....
    
    prober_test.write(":mov:prob:firs:die")
    time.sleep(12)
    get_the_index_position_of_current_die = prober_test.query(":mov:prob:abs:index?")
    get_the_index_position_of_current_die = int(get_the_index_position_of_current_die)
    
    while True:
        # if done_once == False:
        #     # set_on_first_die
        #     prober_test.write(":mov:prob:firs:die")
        #     time.sleep(9)
        #     get_the_index_position_of_current_die = prober_test.query(":mov:prob:abs:index?")
        #     get_the_index_position_of_current_die = int(get_the_index_position_of_current_die)
        #     #after_the_test_is_performance
        #     done_once = True
    
        # next_die_in_wafer
        #We make the measurememn
        print("\n==================================================================")
        print(f"We are probing die at index {get_the_index_position_of_current_die}")
        for each_die_index_label in get_subdies_index_and_label:
            subside_index = each_die_index_label[0]
            subside_label = each_die_index_label[3]
            
            #now we need to go to the laBEL
            prober_test.write(":mov:probeplan:abs:subsite:label %s" %(subside_label))
            time.sleep(3)
            get_the_current_subdie_index = prober_test.query(":mov:prob:abs:subs?")
            get_the_current_subdie_index = int(get_the_current_subdie_index)
            
            print(f"Current Subdie labelled as {subside_label} at index {get_the_current_subdie_index} ")
            
            if get_the_current_subdie_index == int(subside_index):
                for each_power_level in power_level_list:
                    Ampl = Amp + float(each_power_level)
                    print(f"Curret Power Test {each_power_level}")
                    
                    
                    #it is time to set up conditions.
                    #enable SMUs
                    # inst_control.HP4142_setting_voltages(smuAddr, v_left_addr, v_center_addr, v_right_addr, v_left_val, v_center_val, v_right_val)
                    # time.sleep(1)
                    #perform servo to make sure correct power level is injected
                    #inject the correct power
                    # ampl_offset, pin_reading, pout_reading = cal_func.power_sequence_servo(sigGenAddr, Ampl, freq, addr_pin, each_power_level, addr_pout)
                    #now reading the voltages and currents
                    # v_left_reading, v_center_reading, v_right_reading = inst_control.HP4142_getting_IgIb(smuAddr, v_left_addr, v_center_addr, v_right_addr)
                    #now let us measure the 
                    #the value from the signal/generator
                    sec_harm_freq = freq * 2
                    trd_harm_freq = freq * 3
                    sec_harm = inst_control.SigAnalyzer_read(SigAnaAddr, sec_harm_freq)
                    try:
                        sec_harm = float(sec_harm)
                        sec_harm-=second_harmonics
                        sec_harm = round(sec_harm,3)
                    except:
                        sec_harm = str(sec_harm)
                        
                    rd_harm = inst_control.SigAnalyzer_read(SigAnaAddr, trd_harm_freq)
                    try:
                        rd_harm = float(rd_harm)
                        rd_harm-= third_harmonics
                        rd_harm = round(rd_harm, 3)
                    except:
                        rd_harm = str(rd_harm)
                        
                    print(f"Second Harmonics reading: {sec_harm}")
                    print(f"Third Harmonics reading: {rd_harm}")
                    
                    # insertion_power_loss = float(pin_reading) - float(pout_reading)
                    # print(Lot, Wafer, each_die_index_label, subside_label, freq, pin_reading, each_power_level, v_left_val, v_center_val, v_right_val, pout_reading, insertion_power_loss, v_left_reading, v_center_reading, v_right_reading, sec_harm, rd_harm)
        
        
    
        #we check here if the current die is the same as the last die avilable in the wafer.
        if get_the_index_position_of_current_die == get_the_last_die_index:
            print("Entire WAFER has been probed")
            break
        else:
        #if the prevous statments is false, then we go to the next die in the sequence..
            prober_test.write(":mov:prob:next:die")
            time.sleep(7)
            get_the_index_position_of_current_die = prober_test.query(":mov:prob:abs:index?")
            get_the_index_position_of_current_die = int(get_the_index_position_of_current_die)
                 
                
        #     else:
        #         print(f"Subsite with label {subside_label} was not found at index location {subside_index}")
        #         print("We are going to skip this subsite label")
        
        # #We need the probing subsites_selection_based_on_labels and 
        
        # if get_the_last_die_index == get_the_index_position_of_current_die:
        #     print("The whole wafer has been tested....")
        #     break
    
        
# probe_addr = "GPIB0::28::INSTR"
# get_subdies_index_and_label = [[0, '0', '0', '[Die Origin]'], [1, '0', '0', 'MOM_FA_01'], [2, '0', '-280', 'MOM_FA_02']]
# probing_dies_through_entire_wafer_loaded_map(probe_addr, get_subdies_index_and_label)