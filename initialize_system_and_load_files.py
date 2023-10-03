# -*- coding: utf-8 -*-
"""
THe following script contains the calibration sequence

This sequence will be hybrid 
"""
import instrument_control_commands as inst_commands

# =============================================================================
# Initializing all instruments
# Addresses will come from the INI FILE
# Notice that each object is being encapsulated inside a Error-Exception Handling block
# The reason we do this is to check that the instrument has a succeful connection
# Should any of the conditions return 0, then an error has occur and one of the
# insturments may not be properly set up or connected.
# =============================================================================
def initializing_instruments_0_reply(pin_addr, pout_addr, sigGenAddr, freq, specAddr, dc_src_addr, v_left_addr, v_center_addr, v_right_addr):
    power_in_B_val=power_out_B_val=sigGen=specAnalyzer=dc_src_val=""
    try:
        pwrMtr_in = inst_commands.PM_initialization(pin_addr)
    except ValueError:
        print("Unable to initialized the Power Meter (ladybug) at INPUT POWER")
        power_in_B_val = 0
    
    try:
        pwrMtr_out = inst_commands.PM_initialization(pout_addr)
    except ValueError:
        print("Unable to initialized the Power Meter (ladybug) at OUTPUT POWER")
        power_out_B_val = 0
    
    try:
        sigGen = inst_commands.SigGen_RF_OFF(sigGenAddr)
    except ValueError:
        print("Unable to communicate with the Signal Generator at the given Address")
        sigGen = 0
    
    try:
        specAnalyzer = inst_commands.SigAnalyzer_init(specAddr, freq)
    except ValueError:
        print("Unable to communicate with the Spectrum Analyzer at the given Address")
        specAnalyzer = 0
    
    try:
        dc_source = inst_commands.HP4142_initialize(dc_src_addr, v_left_addr, v_center_addr, v_right_addr)
    except ValueError:
        print("Unable to communicate with the DC Power Source Meter at the given Address")
        dc_src_val = 0
        
    if power_in_B_val == 0 or power_out_B_val == 0 or sigGen == 0 or specAnalyzer == 0 or dc_src_val == 0:
        return None, None, None, None, None
    else:
        return pwrMtr_in, pwrMtr_out, dc_source