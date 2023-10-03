# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:14:20 2023

@author: iolab
"""
import instrument_control_commands as instrument_control
import pyvisa as visa
import time
import openpyxl

rm = visa.ResourceManager()

# =============================================================================
# The following function will helps us to calibrating a path
# that complies with a 0dBm calibration approach
# =============================================================================
def calibrating_outputs_at_0dBm(sigGenAddr, Ampl, freq, addr_pin, addr_pout):
    N5173B = rm.open_resource(sigGenAddr)
    freq = int(freq)
    # get_power_lb_offset = -99
    while True:
        instrument_control.SigGen(sigGenAddr, Ampl, freq)
        time.sleep(1)
        read_power_from_lb = instrument_control.measure_PM(addr_pout, freq)
        print(round(Ampl,4),"\t",round(read_power_from_lb,5))
        if read_power_from_lb < -01.2:
            Ampl+= 0.9
        else:
            Ampl+= 0.01
        
        if read_power_from_lb >= 0.00:
            print("0 dBm Cal reached")
            get_power_lb_offset = instrument_control.measure_PM(addr_pin, freq)
            return get_power_lb_offset, Ampl, read_power_from_lb
        
            if get_power_lb_offset >= 1.0:
                print("Please make sure all cables are being properly connected")
                N5173B.write(':OUTPut:STATe %d' % (0))
                return None, None, None
        if Ampl >= 0.1:
            print("Look the power is not being read. \nShutting SigGen down")
            N5173B.write(':OUTPut:STATe %d' % (0))
            return None, None, None

# =============================================================================
# This function will calibrate/get the loss of a cable
# =============================================================================
def calibrating_cable_get_path_loss(sigGenAddr, Ampl, freq, addr_x):
    freq = int(freq)
    instrument_control.SigGen(sigGenAddr, Ampl, freq)
    time.sleep(1.2)
    get_cable_path_loss = instrument_control.measure_PM(addr_x, freq)
    return get_cable_path_loss


# =============================================================================
# The following function will help the system to obtained the targeted power
# it will compasate for all the possible losses occur duting calibration 
# It also helps with the non linearity nature of the system
# =============================================================================
def power_sequence_servo(sigGenAddr, Ampl, freq, addr_pin, target_power, addr_pout):
    target_power = float(target_power)
    instrument_control.SigGen(sigGenAddr, Ampl, freq)
    time.sleep(0.6)
    get_power_read_up = instrument_control.measure_PM(addr_pin, freq)
    if get_power_read_up == target_power or get_power_read_up > target_power-0.2 or get_power_read_up < target_power+0.2:
        get_power_read_from_pout = instrument_control.measure_PM(addr_pout, freq)
        return round(Ampl,3), round(get_power_read_up,3), round(get_power_read_from_pout,3)
    elif get_power_read_up < target_power:
        Ampl+=0.1
    elif get_power_read_up > target_power:
        Ampl-=0.1
        

# =============================================================================
# This function will get a file containig user power levels
# the file can be modified depending on user needs
# =============================================================================
def get_power_levels_for_system_verification(pwrlvl_file_path):
    read_file = openpyxl.load_workbook(pwrlvl_file_path)
    worksheet_to_work = read_file.worksheets[0]
    
    power_level_list = []
    for each_row_in_file in worksheet_to_work:
        pwr_level = each_row_in_file[0].value
        power_level_list.append(pwr_level)    
    return power_level_list


# =============================================================================
# This functions will help to get the corrected cable loss value from the output path
# once the probe tips land on a thru.
# =============================================================================
def send_signal_to_get_outputpath_loss_updated(sigGenAddr, Ampl, freq, pout_lb_ini):
    instrument_control.SigGen(sigGenAddr, Ampl, freq)
    time.sleep(1.2)
    get_power_read_up = instrument_control.measure_PM(pout_lb_ini, freq)
    return round(get_power_read_up,3)


# =============================================================================
# The following function is intended to normalize the frequency entry value
# supplied by user. 
# =============================================================================
def normalizing_freq_entry_value(freq):
    freq = str(freq)
    if "." in freq:
        head, sep, tail = freq.partition(".")
        if len(tail) == 1:
            freq = freq.replace(".", "")
            freq = freq + "00000"
        elif len(tail) == 2:
            freq = freq.replace(".", "")
            freq = freq + "0000"
    else:
        freq += "000000"
    return int(freq)