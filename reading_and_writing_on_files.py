# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:07:05 2023

@author: iolab
"""
import configparser
import csv
import openpyxl

# =============================================================================
# The following function overwrites values on the INI file
# it will get an INI file and update the value for the ouputpath 
# landed on the tru during the partial calibration 
# =============================================================================
def update_INI_file_with_THRU_loss(get_file_path, new_outpath_loss_val):
    config = configparser.ConfigParser()
    config.sections()   
    config.read(get_file_path)
    config.sections()
    if config['Test Conditions']['updated_pout_landed_on_thru']:
        config.set('Test Conditions', 'updated_pout_landed_on_thru', str(new_outpath_loss_val))
        with open(get_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        pass


# =============================================================================
# The following function will get the INI file and output 
# the power input offset, the amplitude offset, the seconds
# and third harmoincs.
# =============================================================================
def get_INI_settings_conditions_from_file(get_file_path):
    config = configparser.ConfigParser()
    config.read(get_file_path)
    config.sections()
    pin_offset = config['Test Conditions']['power_input_offset']
    amplitude_offset = config['Test Conditions']['amplitude_offset']
    sec_harmonics_value = config['Test Conditions']['second_harmonics_val']
    thr_harmonics_value = config['Test Conditions']['third_harmonics_val']
    return pin_offset, amplitude_offset, sec_harmonics_value, thr_harmonics_value


# =============================================================================
# The following function will help us to get all the conditions from the INI file
# =============================================================================
def reading_the_entire_INI_file(get_file_path):
    config = configparser.ConfigParser()
    config.read(get_file_path)
    config.sections()
    pin_lb_addr = config['Hardware']['pin_power_meter']
    pout_lb_addr = config['Hardware']['pout_power_meter']
    sigGen_addr = config['Hardware']['siggen']
    sigAna_addr = config['Hardware']['siganalyzer']
    src_meter_addr = config['Hardware']['src_power_meter']
    prober_addr = config['Hardware']['velox_prober']
    pin_offset = config['Test Conditions']['power_input_offset']
    amplitude_offset = config['Test Conditions']['amplitude_offset']
    pout_offset = config['Test Conditions']['updated_pout_landed_on_thru']
    sec_harm_offset = config['Test Conditions']['second_harmonics_val']
    trd_harm_offset = config['Test Conditions']['third_harmonics_val']
    left_smu_addr = config['smu source']['v_left']
    center_smu_addr = config['smu source']['v_center']
    right_smu_addr = config['smu source']['v_right']
    return pin_lb_addr, pout_lb_addr, sigGen_addr, sigAna_addr, src_meter_addr, prober_addr, pin_offset, amplitude_offset, pout_offset, sec_harm_offset, trd_harm_offset, left_smu_addr, center_smu_addr, right_smu_addr
    

# =============================================================================
# The following function helps to read and extract content from 
# a STV file coming from the prober system
# =============================================================================
def create_subdie_mapping_container(read_stv_file_with_csv_command_lines):
    the_x_was_found = first_line_only = False
    subdies_data_container = []
    counter = 0
    #This block is executed when the STV file is orginal 
    #Other wise
    if ".stv" in read_stv_file_with_csv_command_lines:
        try:
            with open(read_stv_file_with_csv_command_lines) as file_to_read:
                read_file = csv.reader(file_to_read)
                
                for each_line in read_file:
                    
                    if each_line[0] == "X" or each_line[0] == 'x':
                        the_x_was_found = True
                        
                    if the_x_was_found == True:
                        if first_line_only == False:
                            each_line.insert(0, "index")
                            # subdies_data_container.append(each_line)
                            first_line_only = True
                        else:
                            each_line.insert(0, counter)
                            subdies_data_container.append(each_line)
                            counter+=1
                        
                if len(subdies_data_container) > 0:
                    print("SUBDIE MAP CONTAINER READY....")
                    return subdies_data_container
        
        except:
            pass
        #This block is executed when the file is being made by the program
        with open(read_stv_file_with_csv_command_lines) as file_to_read:
            read_file = csv.reader(file_to_read)
            for each_line in read_file:
                subdies_data_container.append(each_line)
            
            if len(subdies_data_container)> 0:
                print("SUBDIE MAP CONTAINER READY....")
                return subdies_data_container
    
    if ".txt" in read_stv_file_with_csv_command_lines:
        try:
            with open(read_stv_file_with_csv_command_lines) as file_to_read:
                read_file = csv.reader(file_to_read)
                
                for each_line in read_file:
                    each_line.insert(0, counter)
                    subdies_data_container.append(each_line)
                    counter+=1
                
                return subdies_data_container
        except:
            pass
                    
                  
# checking_file = r"C:\Harmonics_2p0\build\exe.win-amd64-3.11\SUBSITE_MAP_FILES\umc1707_rfmoscapmimcap_subdie.txt"
# # checking_file = r"C:/Harmonics_2p0/build/exe.win-amd64-3.11/SUBSITE_MAP_FILES/5_george_probing_labels.stv"
# data = create_subdie_mapping_container(checking_file)
# print(data)



# =============================================================================
# The following function will help to parse and extract the COLUMN and ROW
# values from a file.
# These two values are stored into a list pair, then append to a master holder list. 
# =============================================================================
def create_die_probing_master_list_row_column_format(die_probing_file):
    read_file = openpyxl.load_workbook(die_probing_file)
    worksheet_to_work = read_file.worksheets[0]
    
    die_probing_col_row_format = []
    for each_row_in_file in worksheet_to_work:
        if each_row_in_file[0].value == "col":
            pass
        else:
            die_temp_holding_vals = []
            col_val = each_row_in_file[0].value
            row_val = each_row_in_file[1].value
            die_temp_holding_vals.append(col_val)
            die_temp_holding_vals.append(row_val)
            
            die_probing_col_row_format.append(die_temp_holding_vals)
    return die_probing_col_row_format