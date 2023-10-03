# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:34:37 2023

@author: iolab
"""
import functions_and_definitions as definitions
import calibration_functions_and_readbacks as cal_func
import ctypes
import instrument_control_commands as ctrl_commands
import reading_and_writing_on_files as rw_on_files
import time
import configparser
import datetime
import os

# =============================================================================
# The following function will perform the calibration of the system
# there will be two modes:
# The first one will be the full calibration sequence, where the user needs to get
# the cable and path losses
# The second mode will be the partial calibration sequence where the user is required
# to supply an old INI file which contains all the cable losses previously obtained. 
# The purpose of the partial calibration would be to update the outpath cable loss 
# measuring troughout landing the chucks on a structure thru.
# =============================================================================
def harmonics_calibration_sequence(full_calibration, partial_calibration, pin_lb, pout_lb, sigGenAddr, Ampl, freq, pin_lb_ini, pout_lb_ini, userPath, userfileName, lot, wafer, die, device, setup, v_left, v_center, v_right, SigAnaAddr, full_path, power_level_file_location):
    print("HARMONICS SEQUENCE....")
    # =============================================================================
    # Initializing variables to use during the program execution
    # =============================================================================
    input_trace_cable_offset = amplitud_offset = pout_ladybug_calVal = None
    second_harmonics = third_harmonics = 0.0
    
    
    full_calibration = full_calibration
    partial_calibration = partial_calibration
    
    # ctrl_commands.clear_Offsets_PM(pin_lb_ini)
    # ctrl_commands.clear_Offsets_PM(pout_lb_ini)
    
    if full_calibration == True:
        print("\n===============================================================")
        print("FULL CALIBRATION HAS BEEN SELECTED")
        print("\nFM MODE IS NOW ENABLE")
        # =============================================================================
        # Part 1: Cabling Loss Calibration Measurement
        # In this part, the intention is to get all the paths being calibrated. 
        # We obtain all the losses in the cable chain. 
        # 
        # If the user wants to skikp this part when performing calibration, it can be done
        # =============================================================================
    
    
    
        # =============================================================================
        # PHASE A: Prepare PROBER and Instruments
        # In this step the user will be given serveral instructions to 
        # perform to make sure the PROBER is propely prepare for the 
        # calibration. All instrunctions should be follow carefully to 
        # avoid any damage to the prober and/or equipment. 
        # Step 1-4
        # =============================================================================
        reset_step = 0
        phase_to_run = "PHASE A"
        counting = 0
        while True:
            
            if reset_step >= 1:
                message_to_show_for_resetting_step = f"Because YOU cancel the step sequence. \nThe system has been reset.\nStart from the beggining of phase {phase_to_run}"
                ctypes.windll.user32.MessageBoxW(0, message_to_show_for_resetting_step, "ALERT!!!", 0)
                counting = 0
            
            counting=+1
            message_raise_prober_metal_handle = f"Step {counting} : \nLocate the metal handle and raise it to its fully up position. \nThis is being done to avoid accidenly contacting the wafer.\n\nRaise manipulative arm by turning the nob one full rotation in the "'UP'" direction"
            image_raise_handle = "raise_probe_metal_handle.jpg"
            image_raise_handle = definitions.locating_image_and_returning_its_path(image_raise_handle)
            prober_handle_reply = definitions.show_image_and_message(image_raise_handle, message_raise_prober_metal_handle)
            if prober_handle_reply == "Cancel":
                reset_step+=1
                continue
            
            if prober_handle_reply == None:
                raise SystemExit
            
            counting+=1
            message_raise_prober_microscope = "Step {counting}: \n Use the switch at the left side of the base of the microscope to raise it, to access the probes."
            image_microscope = "raise_microscope_head.jpg"
            image_microscope = definitions.locating_image_and_returning_its_path(image_microscope)
            raise_prober_reply = definitions.show_image_and_message(image_microscope, message_raise_prober_microscope)
            if raise_prober_reply == "Cancel":
                reset_step=+1
                continue
            if raise_prober_reply == None:
                raise SystemExit
            
            counting+=1
            message_unscrew_screws = f"Step {counting}: \nWith the microscope up, unscrew all 4 screws that hold down the top plate of the Tophat. \nAlso,  \nRemove the metal Tophat cover and place it aside while working on the Probes."
            image_metal_cover_plate = "raise_probe_microscope.jpg"
            image_metal_cover_plate = definitions.locating_image_and_returning_its_path(image_metal_cover_plate)
            remove_plate_reply = definitions.show_image_and_message(image_metal_cover_plate, message_unscrew_screws)
            if remove_plate_reply == "Cancel":
                reset_step+=1
                continue
            if remove_plate_reply == None:
                raise SystemExit
            
            counting+=1
            message_last_step = f"Step {counting}: \nNow you have completed the steps to prepare the prober side"
            image_last_setp_prober = None
            image_last_setp_prober = definitions.locating_image_and_returning_its_path(image_last_setp_prober)
            last_step_reply = definitions.show_image_and_message(image_last_setp_prober, message_last_step)
            if last_step_reply == "Cancel":
                reset_step+=1
                continue
            if last_step_reply == None:
                raise SystemExit
            break
        
            
        
        # =============================================================================
        # PHASE B: 0 dBm Calibration at Input path
        # The purpose of this first step is to calibrate 
        # the input side of the prober
        # 
        # We perform a servo to get zero. This is acomplished by
        # injecting power from the signal generator and monitor 
        # the output power using a power ladbug power sensor. 
        # Step 5 - 14
        # =============================================================================
        reset_step = 0
        phase_to_run = "PHASE B"
        
        
        while True:
            if reset_step >= 1:
                message_to_show_for_resetting_step = f"Because YOU cancel the step sequence. \nThe system has been reset.\nStarting from the beggining of phase {phase_to_run}"
                ctypes.windll.user32.MessageBoxW(0, message_to_show_for_resetting_step, "ALERT!!!", 0)
                counting = 4 
            
            counting+=1
            locate_probe_input_output_cable_connector = f"Step {counting}: \nLocate the Probe Input Output cables that are connected to the RF probe tips"
            image_input_output_cables = "locate_input_output_cables.jpg"  #CHANGE PICTURR
            image_input_output_cables = definitions.locating_image_and_returning_its_path(image_input_output_cables)
            input_output_cable_reply = definitions.show_image_and_message(image_input_output_cables, locate_probe_input_output_cable_connector)
            if input_output_cable_reply == "Cancel":
                reset_step+=1
                continue
            if input_output_cable_reply == None:
                raise SystemExit
            
            counting+=1
            input_path_on_probe = f"Step {counting}: \nWe will now remove the INPUT cable that is connected to the left side Probe tip. \nAs it is now, LEFT side."
            image_input_path = "probe_input_output_cabling.jpg"
            image_input_path = definitions.locating_image_and_returning_its_path(image_input_path)
            input_path_reply = definitions.show_image_and_message(image_input_path, input_path_on_probe)
            if input_path_reply == "Cancel":
                reset_step+=1
                continue
            if input_path_reply == None:
                raise SystemExit
               
            counting+=1
            unscrew_the_connection = f"Step {counting}: \n Unscrew the connector as shows in the image"
            image_unscrew_connector = "unscrew_left_side.jpg" 
            image_unscrew_connector = definitions.locating_image_and_returning_its_path(image_unscrew_connector)
            unscrew_connector_reply = definitions.show_image_and_message(image_unscrew_connector, unscrew_the_connection)
            if unscrew_connector_reply == "Cancel":
                reset_step+=1
                continue
            if unscrew_connector_reply == None:
                raise SystemExit
            
            counting+=1
            lift_up_and_remove_plate = f"Step {counting}: \nHold the cable while lifting the metal vertical plate to release the cable from the slot of the Tophat. \nBe careful not to bend the cable"
            image_lift_up_vertical_holding_cable_plate = "lift_metal_holder_left.jpg"
            image_lift_up_vertical_holding_cable_plate = definitions.locating_image_and_returning_its_path(image_lift_up_vertical_holding_cable_plate)
            remove_vertical_plate_reply = definitions.show_image_and_message(image_lift_up_vertical_holding_cable_plate, lift_up_and_remove_plate)
            if remove_vertical_plate_reply == "Cancel":
                reset_step+=1
                continue
            if remove_vertical_plate_reply == None:
                raise SystemExit
            
            
            counting+=1
            locate_Power_Input_Output_ladybugs = f"Step {counting}: \nLocate the Power Meters for Input and Output that are on the front panel test rack. \nThey have been labelled as PIN and POUT, respectively."
            image_power_in_out_ladybugs = "locate_pm_input_output_lb.jpg"
            image_power_in_out_ladybugs = definitions.locating_image_and_returning_its_path(image_power_in_out_ladybugs)
            power_sensors_reply = definitions.show_image_and_message(image_power_in_out_ladybugs, locate_Power_Input_Output_ladybugs)
            if power_sensors_reply == "Cancel":
                reset_step+=1
                continue
            if power_sensors_reply == None:
                raise SystemExit
            
            counting+=1
            remove_pout_ladybug = f"Step {counting}: \nRemove the POUT power meter ladybug from the front panel."
            image_remove_pout_ladybug = "remove_pout_lb.jpg"
            image_remove_pout_ladybug = definitions.locating_image_and_returning_its_path(image_remove_pout_ladybug)
            remove_pout_lb_reply = definitions.show_image_and_message(image_remove_pout_ladybug, remove_pout_ladybug)
            if remove_pout_lb_reply == "Cancel":
                reset_step+=1
                continue
            if remove_pout_lb_reply == None:
                raise SystemExit
            
            counting+=1
            connect_input_trace_cable_to_pout_lb = f"Step {counting}: \nNext, connect the Input Probe Path Cable end directly (using a thru adapter) to the POUT power meter Ladybug"
            image_connect_input_to_pout_lb = "connect_input_trace_cable_to_pout_lb.jpg"
            image_connect_input_to_pout_lb = definitions.locating_image_and_returning_its_path(image_connect_input_to_pout_lb)
            connect_input_trace_to_pout_lb = definitions.show_image_and_message(image_connect_input_to_pout_lb, connect_input_trace_cable_to_pout_lb)
            if connect_input_trace_to_pout_lb == "Cancel":
                reset_step+=1
                continue
            if connect_input_trace_to_pout_lb == None:
                raise SystemExit
            
            
            Ampl = -75.5
            #PERFORM THE calibration to OBTAIN 0 DBM AT THE POUT SIDE 
            #FUNCTIONS TO OBTAIN THE POWER 
            print("\n===============================================================")
            print("SigGen Power Input \tPower Meter LB reading")
            
            input_trace_cable_offset, amplitud_offset, pout_ladybug_calVal = cal_func.calibrating_outputs_at_0dBm(sigGenAddr, Ampl, freq, pin_lb_ini, pout_lb_ini)
            print(f"Power Input calibration offset: {input_trace_cable_offset}")
            print(f"amplitude reading from SigGen : {amplitud_offset}")
            print("\n===============================================================")
            
            
            # #we need to turn the RF signal OFF from the signal Generator
            ctrl_commands.SigGen_RF_OFF(sigGenAddr)
            
            
            counting+=1
            place_the_input_trace_back = f"Step {counting}: \nDisconnect the INPUT cable from the POUT power meter and connect it back to the left side probe tip"
            image_connect_input_path_back = "input_trace_back.jpg"
            image_connect_input_path_back = definitions.locating_image_and_returning_its_path(image_connect_input_path_back)
            connect_input_trace_back = definitions.show_image_and_message(image_connect_input_path_back, place_the_input_trace_back)
            if connect_input_trace_back == "Cancel":
                reset_step+=1
                continue
            if connect_input_trace_back == None:
                raise SystemExit
            
            counting+=1
            place_the_cable_holder_plate_back = f"Step {counting}: \nPlace the vertical cable holder back to its slot in the Tophat."
            image_metal_holder_cable_plate = "place_holder_cable_back.jpg"
            image_metal_holder_cable_plate = definitions.locating_image_and_returning_its_path(image_metal_holder_cable_plate)
            metal_input_cable_holder_reply = definitions.show_image_and_message(image_metal_holder_cable_plate, place_the_cable_holder_plate_back)
            if metal_input_cable_holder_reply == "Cancel":
                reset_step+=1
                continue
            if metal_input_cable_holder_reply == None:
                raise SystemExit
            
            counting+=1
            connect_pout_back = f"Step {counting}: \nConnect the POUT meter lady bug back to the front panel"
            image_connect_pout_lb_back = "connect_pout_lb_back.jpg"
            image_connect_pout_lb_back = definitions.locating_image_and_returning_its_path(image_connect_pout_lb_back)
            connect_pout_back_to_panel = definitions.show_image_and_message(image_connect_pout_lb_back, connect_pout_back)
            if connect_pout_back_to_panel == "Cancel":
                reset_step+=1
                continue
            if connect_pout_back_to_panel == None:
                raise SystemExit
                
            #missing step
            
            break
        
        
        # =============================================================================
        # PHASE C: Calibration at Output path
        # At this stage, the intention is to calculate the path loss at the
        # output side. 
        # This is accomplished by connecting the output path side to one of the 
        # power meters and measure cable loss.
        # Step 15 - 20
        # =============================================================================
        reset_step = 0
        phase_to_run = "PHASE C"
        while True:
            if reset_step >= 1:
                message_to_show_for_resetting_step = f"Because YOU cancel the step sequence. \nThe system has been reset.\nStarting from the beggining of phase {phase_to_run}"
                ctypes.windll.user32.MessageBoxW(0, message_to_show_for_resetting_step, "ALERT!!!", 0)
                counting = 14
            
            counting+=1
            locate_output_trace_path = f"Step {counting}: \nNext, we will calibrate the ouput path side. \nIt should be  on the right side oposite to the INPUT probe tip"
            image_output_cable_path = "locate_output_probe_trace.jpg"
            image_output_cable_path = definitions.locating_image_and_returning_its_path(image_output_cable_path)
            locate_outpath_cable_trace_reply = definitions.show_image_and_message(image_output_cable_path, locate_output_trace_path)
            if locate_outpath_cable_trace_reply == "Cancel":
                reset_step+=1
                continue
            if locate_outpath_cable_trace_reply == None:
                raise SystemExit
            
            
            counting+=1
            remove_the_connection_output_path_cable = f"Step {counting}: \nUnscrew the connector to remove the cable from the RF right side probe"
            image_ouput_path_unscrew = "unscrew_right_side.jpg"
            image_ouput_path_unscrew = definitions.locating_image_and_returning_its_path(image_ouput_path_unscrew)
            remove_output_path_connection_reply = definitions.show_image_and_message(image_ouput_path_unscrew, remove_the_connection_output_path_cable)
            if remove_output_path_connection_reply == "Cancel":
                reset_step+=1
                continue
            if remove_output_path_connection_reply == None:
                raise SystemExit
            
            counting+=1
            remove_metal_ouput_cable_holder = f"Step {counting}: \nRemove the vertal metal cable holder while holding the OUPUT cable. \nMake sure cable is carefully removed."
            image_output_cable_holder = "lift_metal_holder_right.jpg"
            image_output_cable_holder = definitions.locating_image_and_returning_its_path(image_output_cable_holder)
            metal_output_cable_holder_reply = definitions.show_image_and_message(image_output_cable_holder, remove_metal_ouput_cable_holder)
            if metal_output_cable_holder_reply == "Cancel":
                reset_step+=1
                continue
            if metal_output_cable_holder_reply == None:
                raise SystemExit
            
            counting+=1
            locate_sigGen_rf_ouput = f"Step {counting}: \nLocate the Signal Generator RF Ouput connection cable"
            image_sigGen_rf_output = "locate_sigGen_rf_output.jpg"
            image_sigGen_rf_output = definitions.locating_image_and_returning_its_path(image_sigGen_rf_output)
            sigGen_output_reply = definitions.show_image_and_message(image_sigGen_rf_output, locate_sigGen_rf_ouput)
            if sigGen_output_reply == "Cancel":
                reset_step+=1
                continue
            if sigGen_output_reply == None:
                raise SystemExit
            
            counting+=1
            disconnect_cable_from_SigGen = f"Step {counting}: \nRemove the cable from the Signal Generator RF Output connector"
            image_disconnect_cable_from_SigGen = "disconnect_cable_from_sigGen.jpg"
            image_disconnect_cable_from_SigGen = definitions.locating_image_and_returning_its_path(image_disconnect_cable_from_SigGen)
            disconnect_cable_reply = definitions.show_image_and_message(image_disconnect_cable_from_SigGen, disconnect_cable_from_SigGen)
            if disconnect_cable_reply == "Cancel":
                reset_step+=1
                continue
            if disconnect_cable_reply == None:
                raise SystemExit
            
            counting+=1
            connect_output_path_trace_to_the_sigGen = f"Step {counting}: \nNow, you will need to connect the RF ouput path trace to the Signal Generator RF Output. \nThis is done to get the cable path loss"
            image_connect_output_path_to_sigGen = "connect_output_path_to_sigGen.jpg"
            image_connect_output_path_to_sigGen = definitions.locating_image_and_returning_its_path(image_connect_output_path_to_sigGen)
            connect_output_path_reply = definitions.show_image_and_message(image_connect_output_path_to_sigGen, connect_output_path_trace_to_the_sigGen)
            if connect_output_path_reply == "Cancel":
                reset_step+=1
                continue
            if connect_output_path_reply == None:
                raise SystemExit
            
            # MEASURE THE CABLE PATH LOSS USING THE LADYBUG......
            # USE THE SAME FUNCTION TO GET THE POWER 
            Ampl = 0.0
            get_cable_path_loss = cal_func.calibrating_cable_get_path_loss(sigGenAddr, Ampl, freq, pout_lb_ini)
            print(f"\nCABLE PATH LOSS: {round(get_cable_path_loss,5)}")
            print("\n===============================================================")
            
            time.sleep(0.2)
            # #we need to turn the RF signal OFF from the signal Generator
            ctrl_commands.SigGen_RF_OFF(sigGenAddr)
            
            
            break
        
        
        # =============================================================================
        # PHASE D: Measure Harmonics Losses
        # In this phase, our intention is to measure the Harmonics Cable loss
        # Step 21 - 25
        # =============================================================================
        reset_step = 0
        phase_to_run = "PHASE D"
        while True:
            if reset_step >= 1:
                message_to_show_for_resetting_step = f"Because YOU cancel the step sequence. \nThe system has been reset.\nStarting from the beggining of phase {phase_to_run}"
                ctypes.windll.user32.MessageBoxW(0, message_to_show_for_resetting_step, "ALERT!!!", 0)
                counting = 20
                
            counting+=1
            locate_pout_power_meter = f"Step {counting}: \nLocate the power meter POUT LadyBug mounted on the front panel"
            image_power_in_out_ladybugs = "locate_pout_pm.jpg"
            image_power_in_out_ladybugs = definitions.locating_image_and_returning_its_path(image_power_in_out_ladybugs)
            locate_POUT_powwer_meter = definitions.show_image_and_message(image_power_in_out_ladybugs, locate_pout_power_meter)
            if locate_POUT_powwer_meter == "Cancel":
                reset_step+=1
                continue
            if locate_POUT_powwer_meter == None:
                raise SystemExit
            
            counting+=1
            disconnect_the_POUT_power_meter_lb = f"Step {counting}: \nRemove the POUT Power Meter Ladybug from the front panel"
            image_disconect_pout_lb = "disconnect_pout_pm_lb.jpg"
            image_disconect_pout_lb = definitions.locating_image_and_returning_its_path(image_disconect_pout_lb)
            disconnect_pout_lb_reply = definitions.show_image_and_message(image_disconect_pout_lb, disconnect_the_POUT_power_meter_lb)
            if disconnect_pout_lb_reply == "Cancel":
                reset_step+=1
                continue
            if disconnect_pout_lb_reply == None:
                raise SystemExit
            
            counting+=1
            locate_the_SpecAnalyzer = f"Step {counting}: \nLocate the Spectrum/Signal Analyzer in the test rack"
            image_locate_specAn = "locate_the_specAn.jpg"
            image_locate_specAn = definitions.locating_image_and_returning_its_path(image_locate_specAn)
            locate_specAn_reply = definitions.show_image_and_message(image_locate_specAn, locate_the_SpecAnalyzer)
            if locate_specAn_reply == "Cancel":
                reset_step+=1
                continue
            if locate_specAn_reply == None:
                raise SystemExit
            
            counting+=1
            disconnect_cable_from_specAn = f"Step {counting}: \nDisconnect cable from the Spectrum Analyzer"
            image_disconnect_cable_specAn = "disconnect_cable_from_specAn.jpg"
            image_disconnect_cable_specAn = definitions.locating_image_and_returning_its_path(image_disconnect_cable_specAn)
            disconnect_specAn_cable_reply = definitions.show_image_and_message(image_disconnect_cable_specAn, disconnect_cable_from_specAn)
            if disconnect_specAn_cable_reply == "Cancel":
                reset_step+=1
                continue
            if disconnect_specAn_cable_reply == None:
                raise SystemExit
            
            counting+=1
            connect_specAn_cable_to_pout_lb = f"Step {counting}: \nConnect the SPEC_AN cable to the ladybug POUT Power Meter LadyBug"
            image_connect_specAn_cable_to_pout_lb = "connect_SA_cable_to_pout_lb.jpg"
            image_connect_specAn_cable_to_pout_lb = definitions.locating_image_and_returning_its_path(image_connect_specAn_cable_to_pout_lb)
            connect_specAn_cable_to_pout = definitions.show_image_and_message(image_connect_specAn_cable_to_pout_lb, connect_specAn_cable_to_pout_lb)
            if connect_specAn_cable_to_pout == "Cancel":
                reset_step+=1
                continue
            if connect_specAn_cable_to_pout == None:
                raise SystemExit
            
            
            # measure_2ND_AND_3RD_HARMONICS... 
            
            Ampl = 0.0
            second_harmonics_freq = 2 * freq
            second_harmonics = cal_func.calibrating_cable_get_path_loss(sigGenAddr, Ampl, second_harmonics_freq, pout_lb_ini)
            third_harmonics_freq =  3 * freq
            third_harmonics = cal_func.calibrating_cable_get_path_loss(sigGenAddr, Ampl, third_harmonics_freq, pout_lb_ini)
            
            print(f"Second Harmonics Reading: {round(second_harmonics,5)}")
            print(f"Third Harmonics Reading: {round(third_harmonics,5)}")
            print("\n===============================================================")
            
            time.sleep(0.2)
            #we need to turn the RF signal OFF from the signal Generator
            ctrl_commands.SigGen_RF_OFF(sigGenAddr)
            
            break
        
        
        # =============================================================================
        # PHASE E: RETURN TO ORIGINAL CABLE SET UP
        # at this time, all cabling should go back to its original place.
        # Step 26 - 32
        # =============================================================================
        reset_step = 0
        phase_to_run = "PHASE E"
        while True:
            if reset_step >= 1:
                message_to_show_for_resetting_step = f"Because YOU cancel the step sequence. \nThe system has been reset.\nStarting from the beggining of phase {phase_to_run}"
                ctypes.windll.user32.MessageBoxW(0, message_to_show_for_resetting_step, "ALERT!!!", 0)
                counting = 25
            
            counting+=1
            connect_the_SA_cable = f"Step {counting}: \nNow, you need to place the SA (Spectrum Analyzer) cable back to its place"
            image_connect_cable_back_to_SA = "connect_the_SA_cable.jpg"
            image_connect_cable_back_to_SA = definitions.locating_image_and_returning_its_path(image_connect_cable_back_to_SA)
            connect_specAn_cable_back = definitions.show_image_and_message(image_connect_cable_back_to_SA, connect_the_SA_cable)
            if connect_specAn_cable_back == "Cancel":
                reset_step+=1
                continue
            if connect_specAn_cable_back == None:
                raise SystemExit
            
            counting+=1
            disconnect_the_cable_from_SigGen = f"Step {counting}: \nRemove the Porbe output cable (labelled RIGHT) from the Signal Generator"
            image_disconect_cable_from_sigGen = "disconnect_cable_and_put_original_back.jpg"
            image_disconect_cable_from_sigGen = definitions.locating_image_and_returning_its_path(image_disconect_cable_from_sigGen)
            disconnect_pout_cable = definitions.show_image_and_message(image_disconect_cable_from_sigGen, disconnect_the_cable_from_SigGen)
            if disconnect_pout_cable == "Cancel":
                reset_step+=1
                continue
            if disconnect_pout_cable == None:
                raise SystemExit
            
            counting+=1
            connect_the_pout_cable_to_prober = f"Step {counting}: \nRecoonnect the probe RFOUT cable (labelled RIGH) that was revomed in the previous back onto the POUT right side of the Tophat."
            image_connect_pout_trace_back = "connect_the_pout_cable_back.jpg"
            image_connect_pout_trace_back = definitions.locating_image_and_returning_its_path(image_connect_pout_trace_back)
            connect_pout_trace_cable_back = definitions.show_image_and_message(image_connect_pout_trace_back, connect_the_pout_cable_to_prober)
            if connect_pout_trace_cable_back == "Cancel":
                reset_step+=1
                continue
            if connect_pout_trace_cable_back == None:
                raise SystemExit
            
            counting+=1
            place_the_metal_cable_holder_back = f'Step {counting}: \nPlace the metal vertical cable holder back to its place. \nBe careful not to bend the cable'
            image_metal_pout_cable_holder = "remove_output_trace_cable_holder.jpg"
            image_metal_pout_cable_holder = definitions.locating_image_and_returning_its_path(image_metal_pout_cable_holder)
            place_metal_cable_holder_back = definitions.show_image_and_message(image_metal_pout_cable_holder, place_the_metal_cable_holder_back)
            if place_metal_cable_holder_back == "Cancel":
                reset_step+=1
                continue
            if place_metal_cable_holder_back == None:
                raise SystemExit
            
            counting+=1
            connect_the_pout_lb = f"Step {counting}: \nConnect the POUT power meter lady bug back to its place, front panel."
            image_connect_the_pout_back = "connect_pout_lb_back.jpg"
            image_connect_the_pout_back = definitions.locating_image_and_returning_its_path(image_connect_the_pout_back)
            connect_pout_lb_back = definitions.show_image_and_message(image_connect_the_pout_back, connect_the_pout_lb)
            if connect_pout_lb_back == "Cancel":
                reset_step+=1
                continue
            if connect_pout_lb_back == None:
                raise SystemExit
            
            counting+=1
            connect_sigGen_cable_back = f"Step {counting}: \nConnect the Signal Generator Cable back to its place"
            image_connect_sigGen_cable = "connect_sigGen_cable_back.jpg"
            image_connect_sigGen_cable = definitions.locating_image_and_returning_its_path(image_connect_sigGen_cable)
            connect_sigGen_cable_to_org_place = definitions.show_image_and_message(image_connect_sigGen_cable, connect_sigGen_cable_back)
            if connect_sigGen_cable_to_org_place == "Cancel":
                reset_step+=1
                continue
            if connect_sigGen_cable_to_org_place == None:
                raise SystemExit
            
            
            counting+=1
            place_metal_probe_cover = f"Step {counting}: \nPlace the PROBE cover back on top of the Tophat. \nHand-tie the screws. \Don't over tighten it, otherwise, Tophat can get distored and cause probing problems"
            image_place_metal_cover_back = "place_metal_probe_cover.jpg"
            image_place_metal_cover_back = definitions.locating_image_and_returning_its_path(image_place_metal_cover_back)
            place_metal_cover_back = definitions.show_image_and_message(image_place_metal_cover_back, place_metal_probe_cover)
            if place_metal_cover_back == "Cancel":
                reset_step+=1
                continue
            if place_metal_cover_back == None:
                raise SystemExit
        
            break
        
        
        try:
            pout_ladybug_calVal = round(pout_ladybug_calVal, 3)
        except:
            pass
        
        try:
            input_trace_cable_offset = round(input_trace_cable_offset,3)
        except:
            pass
        
        try:
            amplitud_offset = round(amplitud_offset, 5)
        except:
            pass
        
        try:
            get_cable_path_loss = round(get_cable_path_loss, 3)
        except:
            pass
        try:
            second_harmonics = round(second_harmonics, 3)
        except:
            pass
        
        try:
            third_harmonics = round(third_harmonics, 3)
        except:
            pass
        
        date_and_time = datetime.datetime.now()
        date_only = datetime.date.today()
        time_only = date_and_time.strftime("%H:%M:%S")
        
        calfile = configparser.ConfigParser()
        
        calfile['Date and Time'] = {'Creation Date': date_only,
                                        'Creation Time': time_only
                                        }
        
        calfile['Hardware'] = {'pin_power_meter': pin_lb,
                               'pout_power_meter': pout_lb,
                               'sigGen': 'GPIB0::2::INSTR',
                               'sigAnalyzer': 'GPIB0::10::INSTR',
                               'src_power_meter': 'GPIB0::19::INSTR',
                               'velox_prober': 'GPIB0::28::INSTR'
                               }
        
        calfile['Fund Meas'] = {'Freq': str(freq)}
        
        calfile['2H Cal'] = {'Freq': str(second_harmonics_freq)}
        
        calfile["3H Cal"] = {'Freq': str(third_harmonics_freq)}
        
        calfile['Test Conditions'] = {'calibration at ': str(pout_ladybug_calVal),
                                      'power_input_offset': str(input_trace_cable_offset),
                                      'amplitude_offset ':str(amplitud_offset),
                                      'pout_cable_loss': str(get_cable_path_loss),
                                      'updated_pout_landed_on_thru': str(get_cable_path_loss),
                                      'second_harmonics_val': str(second_harmonics),
                                      'third_harmonics_val': str(third_harmonics)
                                      }
        calfile['smu source'] = {'v_left': str(v_left),#"1",
                                 'v_center': str(v_center),# "7",
                                 'v_right': str(v_right),#"8",
                                 }
        
        date_only = date_and_time.strftime("%Y-%m-%d_%H_%M")
        construct_ini = os.path.join(userPath, userfileName)
        full_path = construct_ini + "_" + date_only + ".ini"
        with open(full_path, 'w+') as configfile:
            calfile.write(configfile)
        
        print("INI Cabling System Loss Calibration File has been successfully generated.....")
        print("\n===============================================================")


       

    # =============================================================================
    # Part2: Partial Calibration
    # In this stage, the user only calibrated the sequence by landing the probe tips on a thru
    # And the result will be the loss that the thru has
    # this new number will be updated to a provided file, if only partial calibration is being run.
    # Otherwise, the file coming firectly from the calibration part 1 will be used.
    # 
    # Also, notice that we are going to perform a power sweep based on user power levels.
    # We are going to create a file with all the outputs        
    # =============================================================================
    
    
    
    # #for partial we need to initiliaze some variables to avoid any conditions
    # full_path = r"C:\Harmonics_2p0\CALIBRATION_FILES\harmonics_calibration_sample_2023-08-14_15_12.ini"
    # power_level_file_location = r"C:\Harmonics_2p0\power_level_files\system_verification_power_levels.xlsx"
    
    
    # freq = 900000000
    # amplitud_offset = -42.6
    # pin_offset =-33.236
    # pout_offset = -44.637
    # second_harmonics = -17.62
    # third_harmonics = -18.182
    
    
    # freq = int(freq)
    # amplitud_offset = float(amplitud_offset)
    # pin_offset = float(input_trace_cable_offset)
    # # pout_offset = float(pout_offset)
    # second_harmonics = float(second_harmonics)
    # third_harmonics = float(third_harmonics)
    
    if partial_calibration == True or full_calibration == True:
        freq = int(freq)
        try:
            amplitud_offset = float(amplitud_offset)
        except:
            pass
        try:
            pin_offset = float(input_trace_cable_offset)
        except:
            pass
        try:
        # pout_offset = float(pout_offset)
            second_harmonics = float(second_harmonics)
        except:
            pass
        try:
            third_harmonics = float(third_harmonics)
        except:
            pass
        
        print("I am good here....")
        if full_calibration == False:
            # full_path = base_ini_file
            print(full_path)
            pin_offset, amplitud_offset, second_harmonics, third_harmonics = rw_on_files.get_INI_settings_conditions_from_file(full_path)
            print(pin_offset, amplitud_offset, second_harmonics, third_harmonics)
            pin_offset = float(pin_offset)
            amplitud_offset = float(amplitud_offset)
            second_harmonics = float(second_harmonics)
            third_harmonics = float(third_harmonics)
        print("\n===============================================================")
        print("PARTIAL CALIBRATION HAS BEEN ENABLE AND WILL BE EXECUTED")
        
        
        
       
        
        partical_cal_message = "If you have been properly train, continue with the PARTIAL CALIBRATION. \n\nOtherwise, consult with trained team members before proceeding"
        image_partial_message = None
        partial_calibration_message_reply = definitions.show_image_and_message(image_partial_message, partical_cal_message)
        if partial_calibration_message_reply == "Cancel" or partial_calibration_message_reply == None:
            raise SystemExit
        else:
            lower_microscope_and_ISS_mode = "1.-lower down the microscope \n\n2.- drive the probe to the ISS"
            image_lower_microscope = "lower_microscope.jpg"
            image_lower_microscope = definitions.locating_image_and_returning_its_path(image_lower_microscope) 
            lower_microscope_and_drive_to_ISS_mode = definitions.show_image_and_message(image_lower_microscope, lower_microscope_and_ISS_mode)
            if lower_microscope_and_drive_to_ISS_mode == "Cancel" or lower_microscope_and_drive_to_ISS_mode == None:
                raise SystemExit
            
            
            locate_thru_make_contact = "\n3- locate the thru structure \n\n4.- land on the thru struture \n\n5.- we make the measurements"
            image_locate_thru = "locate_thru_and_land.jpg"
            image_locate_thru = definitions.locating_image_and_returning_its_path(image_locate_thru)
            locate_thru_make_contact_reply = definitions.show_image_and_message(image_locate_thru, locate_thru_make_contact)
            if locate_thru_make_contact_reply == "Cancel" or locate_thru_make_contact_reply == None:
                raise SystemExit
                    
            get_outpath_loss_updated_on_a_thru_structure = cal_func.send_signal_to_get_outputpath_loss_updated(sigGenAddr, amplitud_offset, freq, pout_lb_ini)
            print(f"POUT Reading after landing on the thru {get_outpath_loss_updated_on_a_thru_structure}")
            try:
                rw_on_files.update_INI_file_with_THRU_loss(full_path, get_outpath_loss_updated_on_a_thru_structure)
            except ValueError:
                print("There has been an error with the file you are using. \nIt was unable to update the value for the thru.\nManually update the number on the INI file")
                
            time.sleep(0.2)
            #we need to turn the RF signal OFF from the signal Generator
            ctrl_commands.SigGen_RF_OFF(sigGenAddr)
            
            
            calibrationName = "sys_harm_verification" + "_" + str(freq)
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
            userPath = os.getcwd()
            userPath = os.path.join(userPath, "SYS_HARM_VERIFICATION")
            if (os.path.isdir(userPath) == 0):
                pass
            fullPath = os.path.join(userPath, calibrationName)
            ip_shv = open(fullPath + "_" + timestamp + ".csv", 'w+')
            ip_shv.write("Lot, Wafer, Die, Device, Setup, Freq, Pin, Vl, Vc, Vr, Pin_act, Pout, IL, Il, Ic, Ir, 2H, 3H\n")
            #now it is time to build it up the file and get the reading from the actualcontrol system....
            get_pins_from_file = cal_func.get_power_levels_for_system_verification(power_level_file_location)
            if len(get_pins_from_file) > 0:
                
                #here is where we apply voltage bias to the thru
                
                for each_pin_level in get_pins_from_file:
                    #If ful calibration is false, we need to initialize the signal/spectrum analyzer
                    ctrl_commands.SigAnalyzer_init(SigAnaAddr, freq)
                    print(f"\nTarget Power {each_pin_level} dBm")
                    #make sure we are working with either intergers or floats
                    #we get new amplitude
                    ampl = float(amplitud_offset) + float(each_pin_level)
                    print(f"Amplitude injected at Signal Generator: {ampl} dBm")
                    if ampl > 0:
                        break
                    amplitude, pin_lb_reading, pout_lb_reading = cal_func.power_sequence_servo(sigGenAddr, ampl, freq, pin_lb_ini, each_pin_level, pout_lb_ini)
                    pout_lb_reading -= get_outpath_loss_updated_on_a_thru_structure
                    pin_lb_reading -= pin_offset
                    insertion_loss = float(pin_lb_reading) - float(pout_lb_reading)
                    print(f"Insertion Loss : {insertion_loss} dBm")
                    
                    #the value from the signal/generator
                    sec_harm_freq = freq * 2
                    trd_harm_freq = freq * 3
                    sec_harm = ctrl_commands.SigAnalyzer_read(SigAnaAddr, sec_harm_freq)
                    try:
                        sec_harm = float(sec_harm)
                        sec_harm-=second_harmonics
                        sec_harm = round(sec_harm,3)
                    except:
                        sec_harm = str(sec_harm)
                        
                    rd_harm = ctrl_commands.SigAnalyzer_read(SigAnaAddr, trd_harm_freq)
                    try:
                        rd_harm = float(rd_harm)
                        rd_harm-= third_harmonics
                        rd_harm = round(rd_harm, 3)
                    except:
                        rd_harm = str(rd_harm)
                        
                    print(f"Second Harmonics reading: {sec_harm}")
                    print(f"Third Harmonics reading: {rd_harm}")
                    il = ic = ir = None
                    ip_shv.write(str(lot) + "," + str(wafer) + "," + str(die) + "," + str(device) + "," + str(setup) + "," + str(freq) + "," + str(each_pin_level) + "," + str(v_left) + "," + str(v_center)  + "," + str(v_right) + "," +  str(pin_lb_reading) + "," + str(pout_lb_reading) + "," + str(insertion_loss) + "," + str(il) + "," + str(ic) + "," + str(ir) + "," + str(sec_harm) + "," + str(rd_harm) + "\n")
            ip_shv.close()
            ctrl_commands.clean_SigAnalyzer(SigAnaAddr)
    
    #we need to turn the RF signal OFF from the signal Generator
    ctrl_commands.SigGen_RF_OFF(sigGenAddr)
    
    if full_calibration:    
        print("\nFull - and - Partial  Calibration have been successfully executed.")
        print("\n===============================================================")
        return 0
    elif partial_calibration:
        print("\nPartial Calibration has been successfully executed.")
        print("\n===============================================================")
        return 0
    else:
        pass
    return 0