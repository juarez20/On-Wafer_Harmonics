# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:18:18 2023

@author: iolab
"""
import pyvisa as visa
import time, os
import calibration_functions_and_readbacks as cal_func
import datetime
import instrument_control_commands as inst_control
import reading_and_writing_on_files as rd_wr_files

rm = visa.ResourceManager()

# =============================================================================
# The following function will help to probing dies on a wafer map
# INDEX SUPPLIED MODE
# In this mode, the reference will be the entire loaded wafer map at the moment. 
# The user then will supply an excel file containing the index values.
# Those index values will be used to determine which location to test the die. 
# It is up to the user which index they want to start or how many dies are to be tested.
# 
# =============================================================================
def probing_dies_through_indexes_provided_by_user(probe_addr, die_probing_index_file, get_subdies_index_and_label, smuAddr, v_left_addr, v_center_addr, v_right_addr, voltages_level_list, sigGenAddr, Amp, freq, power_level_list, addr_pin, addr_pout, SigAnaAddr, second_harmonics, third_harmonics, user_file_name, userPath, Lot, Wafer, pin_offset_val, pout_offset_val, reading_current_bias):
    prober_test = rm.open_resource(probe_addr)
    prober_info = prober_test.query("*IDN?")
    print(prober_info)
    
    
    print(reading_current_bias)
    input("Checking that all the conditions are met before  we jump into getting all the system")
    inst_control.SigAnalyzer_init(SigAnaAddr, freq)
    
    #This will be data container holder for the index. 
    # get_the_index_die_values = cal_func.get_power_levels_for_system_verification(die_probing_index_file)
    get_the_col_row_coord = rd_wr_files.create_die_probing_master_list_row_column_format(die_probing_index_file)
        
    freq = int(freq)
    Amp = float(Amp)
    second_harmonics = float(second_harmonics)
    third_harmonics = float(third_harmonics)
    
    start_time = stop_time = ""
    
    #creating the file we need to use.
    user_file_name = user_file_name + "_" + str(freq)
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    fullPath = os.path.join(userPath, user_file_name)
    ip_shv = open(fullPath + "_" + timestamp + ".csv", 'w+')
    ip_shv.write("Lot, Wafer, Die, Subdie, Freq, Target Power Level, Pwr Input, Pwr Output, Insertion Loss, V_left, V_center, V_right, I_Left, I_center, I_right, 2H, 3H\n")
    
    # print(get_the_index_die_values)    
    if  len(get_the_col_row_coord) > 0:
        print("Probing Dies")
        
        for each_index in get_the_col_row_coord:
            #now each index will contain two sets col and row
            col = each_index[0]
            row = each_index[1]

            start_time = time.time()
            
            prober_test.write(":move:prob:absolute:die " +str(col) +" "+str(row))
            # prober_test.write(":mov:prob:abs:index %d" %(each_index))
            time.sleep(20)
            #now we need to check that the correct index has been gone to
            # get_current_index = prober_test.query(":mov:prob:abs:index?")
            # get_current_index = int(get_current_index)
            
            print("\n========================================")
            print(f"Current Probing Die : {each_index}")
            
            
            # get_current_index = True
            # # if each_index == get_current_index:
            # if get_current_index == True:
            #     # print("Test can commence and it is ready for execution")
                
            for each_die_index_label in get_subdies_index_and_label:
                each_die_index_label = each_die_index_label.split(", ")
                print(each_die_index_label)
                subside_index = each_die_index_label[0]
                subside_label = each_die_index_label[3]
                
                #now we need to go to the laBEL
                prober_test.write(":mov:probeplan:abs:subsite:label %s" %(subside_label))
                time.sleep(15)
                # get_the_current_subdie_index = prober_test.query(":mov:prob:abs:subs?")
                # get_the_current_subdie_index = int(get_the_current_subdie_index)
                
                print(f"\nCurrent Subsite Label: {subside_label}")
                first_time = False
                for each_voltage_set_level in voltages_level_list:
                    print(each_voltage_set_level)
                    v_left_val = each_voltage_set_level[0] 
                    v_center_val = each_voltage_set_level[1]
                    v_right_val = each_voltage_set_level[2]
                    
                    if reading_current_bias == True:
                        inst_control.HP4142_setting_voltages(smuAddr, v_left_addr, v_center_addr, v_right_addr, v_left_val, v_center_val, v_right_val)
                        time.sleep(15)
                    
                    # if get_the_current_subdie_index == int(subside_index):
                        # print("we can perform the test")
                        # print(power_level_list)
                    for each_power_level in power_level_list:
                        if float(each_power_level) <= 35: #The power to be injected is limited 35 dBm
                            print(f"Current Power Testing : {each_power_level} dBm")
                            # print(f" Power Level : {Amp}")
                            
                            # # print("we can perform the test")
                            Ampl = Amp + float(each_power_level)
                            print(f"Amplitude : {Ampl} dBm without Servo")
                            
                            #Servoing POWER....
                            # ampl_offset, pin_reading, pout_reading = cal_func.power_sequence_servo(sigGenAddr, Ampl, freq, addr_pin, each_power_level, addr_pout)
                            # print(f"Servoed Amplitude : {ampl_offset} dBm")
                            #now reading the voltages and currents
                            # i_left_reading = i_center_reading = i_right_reading =  0
                            i_left_reading = i_center_reading = i_right_reading = None
                            if reading_current_bias == True:
                                i_left_reading, i_center_reading, i_right_reading = inst_control.HP4142_getting_IgIb(smuAddr, v_left_addr, v_center_addr, v_right_addr)
                                time.sleep(0.5)
                            
                            
                            
                            time.sleep(0.3)
                            if first_time == False:
                                inst_control.SigGen(sigGenAddr, Ampl, freq)
                                first_time = True
                            else:
                                inst_control.SigGen_pwr_only(sigGenAddr, Ampl, freq)
                            
                            time.sleep(0.3)
                            #now let us measure the 
                            #the value from the signal/generator
                            sec_harm_freq = freq * 2
                            trd_harm_freq = freq * 3
                            time.sleep(0.5)
                            sec_harm = inst_control.SigAnalyzer_read(SigAnaAddr, sec_harm_freq)
                            time.sleep(0.5)
                            rd_harm = inst_control.SigAnalyzer_read(SigAnaAddr, trd_harm_freq)
                            print(f"Second Harmonics reading: {sec_harm}")
                            print(f"Third Harmonics reading: {rd_harm}")
                            time.sleep(0.2)
                            
                            get_power_read_up =  inst_control.measure_PM(addr_pin, freq)
                            time.sleep(0.1)
                            get_power_read_from_pout = inst_control.measure_PM(addr_pout, freq)
                            time.sleep(0.1)
                            
                           
                            # print("OFFSETS LADY BUG")
                            # print(pin_offset_val)
                            # print(pout_offset_val)
                            pin_reading = get_power_read_up - float(pin_offset_val)
                            pout_reading = get_power_read_from_pout - float(pout_offset_val)
                            print(f"Input Power: {pin_reading} dBm")
                            print(f"Output Power: {pout_reading} dBm")
                            
                            try:
                                sec_harm = float(sec_harm)
                                sec_harm-=second_harmonics
                                sec_harm = round(sec_harm,3)
                            except:
                                sec_harm = str(sec_harm)
                            
                            try:
                                rd_harm = float(rd_harm)
                                rd_harm-= third_harmonics
                                rd_harm = round(rd_harm, 3)
                            except:
                                rd_harm = str(rd_harm)
                                
                            
                            try:
                                insertion_power_loss = float(pin_reading) - float(pout_reading)
                                insertion_power_loss = round(insertion_power_loss,2)
                            except:
                                insertion_power_loss = None
                            
                          
                            each_index_composite = "C" + str(col) +"R" + str(row)
                            
                            print(Lot, Wafer, each_index, subside_label, freq, each_power_level, pin_reading, pout_reading, insertion_power_loss, v_left_val, v_center_val, v_right_val, i_left_reading, i_center_reading, i_right_reading, sec_harm, rd_harm,"\n")
                            ip_shv.write(str(Lot) +","+ str(Wafer) +","+ str(each_index_composite) +","+ str(subside_label) +","+ str(freq) +","+ str(each_power_level) +","+ str(pin_reading) +","+ str(pout_reading) +","+ str(insertion_power_loss) +","+ str(v_left_val) +","+ str(v_center_val) +","+ str(v_right_val) +","+ str(i_left_reading) +","+ str(i_center_reading) +","+ str(i_right_reading) +","+ str(sec_harm) +","+ str(rd_harm) +"\n")
                            time.sleep(0.1)
                            ip_shv.flush()
                            time.sleep(0.1)
                            os.fsync(ip_shv)
                            time.sleep(0.05)
                            # try:
                            #     if rd_harm > -5.5:
                            #         break
                            # except:
                            #     pass
                            
                        else:
                            pass
                  
            
                # Calculating Test Completion Time.
                stop_time = time.time()
                now = datetime.datetime.today()
                taken_time = stop_time - start_time
                print(f"\ndie took about {round(taken_time,2)} seconds to run")
                current_index_in_index_list = get_the_col_row_coord.index(each_index)+1
                remaining_probing_indexes = len(get_the_col_row_coord) - current_index_in_index_list
                remaining_seconds = taken_time * remaining_probing_indexes
                print(f"Remaining Probing Dies {remaining_probing_indexes}")
                print(f"Remaining Time : {round(remaining_seconds,2)}  seconds")
                
                estimated_time_of_completion = now + datetime.timedelta(seconds=remaining_seconds)
                print(f"Estimated Completion Time : {estimated_time_of_completion}")
            
    else:
        pass
    
    inst_control.SigGen_RF_OFF(sigGenAddr)
    inst_control.clean_SigAnalyzer(SigAnaAddr)
    inst_control.HP4142_sets_OFF(smuAddr, v_left_addr, v_center_addr, v_right_addr)
    print("\nTest Sequence Successfully Executed")
    return 0