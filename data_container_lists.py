# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:09:39 2023

@author: iolab
"""
import reading_files_to_get_settings_for_TEST as read_fl_for_test

def get_master_volatgeLevels_and_pwrLvls_lists(test_sequences):
    master_voltages_levels = []
    master_power_levels = []
    for power_level_setups in test_sequences:
        temp_voltages_supply = []
        v_right_val, v_center_val, v_left_val, power_level_list = read_fl_for_test.get_conditions_from_DUT_Setups_files(power_level_setups)
        checking_list = (v_right_val, v_center_val, v_left_val)
        temp_voltages_supply.append(checking_list)
        
        if checking_list not in master_voltages_levels:
            master_voltages_levels.append(checking_list)
        
        for each_power_level in power_level_list:
            if each_power_level not in master_power_levels:
                master_power_levels.append(each_power_level)

    
    master_power_levels = sorted(master_power_levels, key=lambda number:float(number))
    return master_voltages_levels, master_power_levels


# test_sequences = ['harmonics_RVT', 'harmonics_test - Copy', 'harmonics_test']
# voltages_levels, power_levels = get_master_volatgeLevels_and_pwrLvls_lists(test_sequences)
# print(voltages_levels, power_levels)

# for each_voltage_set in voltages_levels:
#     print(each_voltage_set[2])