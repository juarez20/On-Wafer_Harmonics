# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:42:05 2023

@author: iolab
"""
import os, time
import pyvisa as visa
import ctypes
from ctypes import *

rm = visa.ResourceManager()
global LV_LB_API2

enable_cdll = cdll.LoadLibrary(os.path.abspath("C:\Program Files\LadyBug Technologies LLC\LadyBug Power Sensor Applications\LB_API2.dll"))
LV_LB_API2= enable_cdll #cdll.LoadLibrary("C:\\Program Files\LadyBug Technologies LLC\\LadyBug Power Sensor Applications\\LB_API2.dll")

def PM_initialization(Serial):
    # os.chdir("C:\\Program Files\\LadyBug Technologies LLC\\LadyBug Power Sensor Applications")
    LV_LB_API2= enable_cdll#CDLL("LB_API2.dll")
    #print LV_LB_API2
    #print LV_LB_API2.LB_SensorCnt()
    LV_LB_API2.LB_GetAddress_SN.restype=ctypes.c_int
    LV_LB_API2.LB_GetAddress_SN.argtypes=[ctypes.c_char_p]
    try:
        x=LV_LB_API2.LB_GetAddress_SN(Serial)
    except:
        Serial = Serial.encode("utf-8")
        x=LV_LB_API2.LB_GetAddress_SN(Serial)
    #print type(x),x
    LV_LB_API2.LB_InitializeSensor_Addr.argtypes=[ctypes.c_int]
    if(LV_LB_API2.LB_InitializeSensor_Addr(c_int(x))>0):
        print("Initialized")
        return x
    else:
        return None



def measure_PM(addr_x, freq):
    y=ctypes.c_double()
    #LV_LB_API2= enable_cdll#CDLL("LB_API2.dll")
    LV_LB_API2.LB_SetFrequency.argtypes=[ctypes.c_int,ctypes.c_double]
    if(LV_LB_API2.LB_SetFrequency(c_int(addr_x), c_double(freq))):
        #print "freq set :",freq
         pass
    LV_LB_API2.LB_GetFrequency.argtypes=[ctypes.c_int,ctypes.POINTER(c_double)]
    if(LV_LB_API2.LB_GetFrequency(c_int(addr_x), y)):
        #print y.value,
         pass
    LV_LB_API2.LB_MeasureCW.argtypes=[ctypes.c_int,ctypes.POINTER(c_double)]
    if(LV_LB_API2.LB_MeasureCW(c_int(addr_x), y)):
        #print y.value
        return y.value
    
# =============================================================================
# def SigAnalyzer_init(SigAnaAddr, freq):
#     SigAnal=rm.open_resource(SigAnaAddr)#("GPIB0::10::INSTR") 
#     SigAnal.write('*RST')
#     SigAnal.timeout = None
#     # --- Set reference oscillator to External, Auto Align ON
#     # --- vsekar, Dec12,2022
#     SigAnal.write("SENS:ROSC:SOUR EXT")
#     SigAnal.write("SENS:ROSC:EXT:FREQ 10e6")
#     # SigAnal.write("CAL:AUTO ON")
#     # ------------------------------------
#     SigAnal.write("SENS:FREQ:CENT %G" % (freq)) #(1.8E9))
#     SigAnal.write("SENS:FREQ:SPAN %d" %(1000))
#     SigAnal.write("DISP:WIND:TRAC:Y:RLEV -70") #Sets the Reference Level to -80dB
#     SigAnal.write("SENS:POW:RF:ATT %d" %(0))
#     SigAnal.write("SENS:BAND:VID:AUTO %d" %(0))
#     SigAnal.write("SENS:BAND:VID %d" %(10))
#     SigAnal.write("SENS:BAND:RES:AUTO %d" %(0))
#     SigAnal.write("SENS:BAND:RES %d" %(10))
#     # SigAnal.write("SENS:SWE:TIME:AUTO %d" %(0))
#     # SigAnal.write("SENS:SWE:TIME %G" %(0.684))
#     # SigAnal.write("CALC:MARK1:SET:CENT" )
#     # SigAnal.query("*OPC?") # dynamic wait for freq to settle
#     # out=SigAnal.query_ascii_values("CALC:MARK1:X?" )
#     # out2=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
#     # out1=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
#     # return out,out1,out2
# =============================================================================
def SigAnalyzer_init(SigAnaAddr, freq):
    SigAnal=rm.open_resource(SigAnaAddr)#("GPIB0::10::INSTR") 
    SigAnal.write('*RST')
    SigAnal.timeout = None
    # --- Set reference oscillator to External, Auto Align ON
    # --- vsekar, Dec12,2022
    
    # SigAnal.write("SENS:ROSC:SOUR EXT")
    # SigAnal.write("SENS:ROSC:EXT:FREQ 10e6")
    # SigAnal.write("CAL:AUTO ON")
    # ------------------------------------
    SigAnal.write("SENS:FREQ:CENT %G" %(freq))
    SigAnal.write("SENS:FREQ:SPAN %d" %(1000))
    SigAnal.write("SENS:BAND:VID:AUTO %d" %(1))
    SigAnal.write("DISP:WIND:TRAC:Y:RLEV -50")
    SigAnal.write("SENS:BAND:VID %d" %(100))
    SigAnal.write("SENS:BAND:RES:AUTO %d" %(1))
    SigAnal.write("SENS:BAND:RES %d" %(100))
    SigAnal.write("SENS:SWE:TIME:AUTO %d" %(0))
    # SigAnal.write("SENS:SWE:TIME %G" %(0.684))
    # SigAnal.write("CALC:MARK1:SET:CENT" )
    SigAnal.write("SENS:POW:RF:ATT %d" %(10))
    SigAnal.query("*OPC?") # dynamic wait for freq to settle
    out=SigAnal.query_ascii_values("CALC:MARK1:X?" )
    out2=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
    out1=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
    # print(out,out1,out2)
    return out,out1,out2

# SigAnalyzer_init("GPIB0::10::INSTR", 2700000000)

#rewriting some of the variable , asign mininful naming
# =============================================================================
# def SigAnalyzer_read(sigAnaAddr, freq):   
#     SigAnal=rm.open_resource(sigAnaAddr)#("GPIB0::10::INSTR") 
#     SigAnal.timeout = None
#     #SigAnal.values_format.datatype = 'd'
#     #SigAnal.write('*RST')
#     SigAnal.write("SENS:FREQ:CENT %G" %(freq))
# 
#     # this entire handshake sequence is necessary and optimized
#     # ----------------------------------------------------------
#     SigAnal.query("*OPC?") # wait for done signal
#     time.sleep(0.1) # wait a bit
#     SigAnal.query("*OPC?") # are you really done?
#     time.sleep(0.1) # wait a bit
#     SigAnal.query("*OPC?") # really really done?
#     # ----------------------------------------------------------
#     # time.sleep(0.1)  #Delay added after clear  #8 seconds here
#     # SigAnal.write(":TRAC1:TYPE AVER")
#     # time.sleep(0.1)
#     # SigAnal.write(":SENSe:AVErage 1") #this should be for tunrning the averaging on
#     # SigAnal.write(":SENSe:AVErage:COUN 10")
#     # time.sleep(0.9)
#     # SigAnal.write("CALC:MARK1:MODE POS")
#     time.sleep(0.2)
#     SigAnal.write("CALC:MARK1:X %d" %(freq))
#     peak_value = SigAnal.query("CALC:MARK1:Y?")
#     peak_value = float(peak_value)
#     peak_value = peak_value*1
#     # SigAnal.write(":SENSe:AVErage 0")
#     return(peak_value)
#     # out=SigAnal.query_ascii_values("CALC:MARK1:X?" )
#     # print(out)
#     # out1=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
#     # print(out1)
#     # # out2=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
#     # return out,out1,#out2
# =============================================================================
def SigAnalyzer_read(SigAnaAddr, freq):   
    SigAnal=rm.open_resource(SigAnaAddr)#("GPIB0::10::INSTR") 
    SigAnal.timeout = None
    #SigAnal.values_format.datatype = 'd'
    #SigAnal.write('*RST')
    SigAnal.write("SENS:FREQ:CENT %G" %(freq))

# =============================================================================
#     # this entire handshake sequence is necessary and optimized
#     # ----------------------------------------------------------
#     SigAnal.query("*OPC?") # wait for done signal
#     time.sleep(0.1) # wait a bit
#     SigAnal.query("*OPC?") # are you really done?
#     time.sleep(0.1) # wait a bit
#     SigAnal.query("*OPC?") # really really done?
#     # ----------------------------------------------------------
# 
# =============================================================================
    # out=SigAnal.query_ascii_values("CALC:MARK1:X?" )
    # out1=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
    # out2=SigAnal.query_ascii_values("CALC:MARK1:Y?" )
    # print(out,out1,out2)
    # out1 = out1[0]
    # return out1
    time.sleep(0.2)
    SigAnal.write(":SENSe:AVErage 1") #this should be for tunrning the averaging on
    SigAnal.write(":SENSe:AVErage:COUN 15")
    time.sleep(0.5)
    SigAnal.write("CALC:MARK1:MODE POS")
    time.sleep(0.5)   
    SigAnal.write("CALC:MARK1:X %d" %(freq))
    time.sleep(0.5)
    peak_value = SigAnal.query("CALC:MARK1:Y?")
    peak_value = float(peak_value)
    peak_value = peak_value*1
    SigAnal.write(":SENSe:AVErage 0")
    return peak_value


# SigAnalyzer_init("GPIB0::10::INSTR", 900000000)
# print(SigAnalyzer_read("GPIB0::10::INSTR", 900000000*3))
def clean_SigAnalyzer(SigAnAddr):
    SigAnal=rm.open_resource(SigAnAddr)
    SigAnal.write(":SYSTem:PRESet")

def SigGen(sigGenAddr, Amp, freq):
    E4428C = rm.open_resource(sigGenAddr)#('GPIB0::2::INSTR')
    E4428C.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G DBM' % (Amp))
    # E4428C.write(':INITiate:CONTinuous:ALL %d' % (1))
    E4428C.write(':SOURce:FREQuency:CW %d' % (freq))
    E4428C.write(':INITiate:CONTinuous:ALL %d' % (1))
    E4428C.write(':OUTPut:STATe %d' % (1))
    try:
        E4428C.write(":SOURce:MODulation:PULM:STATe %d" % (0))
        E4428C.write(":SOURce:MODulation:STATe %d" % (0))
    except:
        pass
    # E4428C.close()

# SigGen("GPIB0::2::INSTR", -75.9, 950000000)
def SigGen_pwr_only(sigGenAddr, Amp, freq):
    E4428C = rm.open_resource(sigGenAddr)
    E4428C.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G DBM' % (Amp))
    E4428C.write(':SOURce:FREQuency:CW %d' % (freq))
    
def SigGen_RF_OFF(sigGenAddr):
    E4428C = rm.open_resource(sigGenAddr)
    E4428C.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G DBM' % (-75.5))
    E4428C.write(':OUTPut:STATe %d' % (0))
    E4428C.close()


def HP4142_initialize(smuAddr, v_left_addr, v_center_addr, v_right_addr):
    HP4142 = rm.open_resource(smuAddr)
    HP4142.write("*RST\n")
    HP4142.write("CN "+str(v_left_addr)+","+str(v_center_addr)+","+str(v_right_addr)+"\n")
    HP4142.write("FMT 1;AV 64,1\n") #FMT command clears the output data buffer and specifies measurement data output format
    HP4142.write("MM 1,"+str(v_left_addr)+","+str(v_center_addr)+","+str(v_right_addr)+"\n") #MM command sets the measuremnt mode and measurement units:1 spot measurement
    status = HP4142.query_ascii_values("ERR?\n", converter='s')
    if("".join(status)[:4]=="0000"):
        print("HP4142B initialized")
    return HP4142


def HP4142_setting_voltages(smuAddr, v_left_addr, v_center_addr, v_right_addr, v_left_val, v_center_val, v_right_val):#VG, VB):
    HP4142=rm.open_resource(smuAddr)#("GPIB0::19::INSTR")
    HP4142.write("CN "+str(v_left_addr)+","+str(v_center_addr)+","+str(v_right_addr)+"\n")
    time.sleep(1)
    HP4142.write("FMT 1;AV 64,1\n")
    HP4142.write("MM 1,"+str(v_left_addr)+","+str(v_center_addr) +","+str(v_right_addr) +"\n")
    time.sleep(0.6)
    #need to check that the correct smus are being turned ON 
    checking_if_turn_on =  HP4142.query("LOP?")
    print("TURNING ON HP4142B")
    print(checking_if_turn_on)
    
    #DV command forces output voltages from the specified unit 
    #DV ch#, output range, output voltage, [,I compliance][,compliance polarity mode]
    # left_voltage_reading = HP4142.write("DV "+str(v_left_addr)+",0"+str(v_left_val)+",0.1\n")
    
    HP4142.write("DV "+str(v_left_addr)+",0,"+str(v_left_val))
    HP4142.write("DV "+str(v_center_addr)+",0,"+str(v_center_val))
    HP4142.write("DV "+str(v_right_addr)+",0,"+str(v_right_val))

# HP4142_initialize("GPIB0::19::INSTR", 1, 7, 8)
# HP4142_setting_voltages("GPIB0::19::INSTR", 1, 7, 8, -2.5, 0, -2.5)

def HP4142_getting_IgIb(smuAddr, v_left_addr, v_center_addr, v_right_addr):
    HP4142=rm.open_resource(smuAddr)#("GPIB0::19::INSTR") 
    #TI command is the trigger command for high speed spot current measurement.
    # HP4142.write("CN "+str(v_left_addr)+","+str(v_center_addr)+","+str(v_right_addr)+"\n")
    #TI ch#[,I measurement range]
    # HP4142.write("MM 1,"+str(v_left_addr)+","+str(v_center_addr) +","+str(v_right_addr) +"\n")
    time.sleep(3)#3.5
    left_current_reading = HP4142.query_ascii_values( "TI"+str(v_left_addr)+",0\n", converter='s')
    time.sleep(0.3) #3
    left_current_reading = left_current_reading[0][3:][:-2]
    time.sleep(0.3) #3
    center_current_reading = HP4142.query_ascii_values( "TI"+str(v_center_addr)+",0\n", converter='s')
    time.sleep(0.3) #3
    center_current_reading = center_current_reading[0][3:][:-2]
    time.sleep(0.3) #3
    right_current_reading = HP4142.query_ascii_values( "TI"+str(v_right_addr)+",0\n", converter='s')
    time.sleep(0.3) #3
    right_current_reading = right_current_reading[0][3:][:-2]
    return left_current_reading, center_current_reading, right_current_reading


def HP4142_sets_OFF(smuAddr,  v_left_addr, v_center_addr, v_right_addr):
    HP4142=rm.open_resource(smuAddr)
    #CL command disables the specified units by setting the output switches to OFF
    HP4142.write("CL "+str(v_left_addr)+","+str(v_center_addr)+","+str(v_right_addr)+"\n")
    time.sleep(2)
    #LOP? commands check if all the SMU units are being turn off.
    checking_all_smus_are_off = HP4142.query("LOP?")
    time.sleep(0.9)
    checking_all_smus_are_off = checking_all_smus_are_off.replace("LOP","")
    checking_all_smus_are_off = list(checking_all_smus_are_off.split(","))
    print(checking_all_smus_are_off)

# HP4142_sets_OFF("GPIB0::19::INSTR", 1, 7, 8)

def HP4142_debug(smuAddr):
    enable_ch_list = ["1", "7", "8"]
    cn_command = "CN "
    cn_command += ",".join(enable_ch_list)
    print(cn_command)
    print(type(cn_command))
    
    HP4142=rm.open_resource(smuAddr)#("GPIB0::19::INSTR") 
    HP4142.write("*RST\n")
    
    #CN enables the MPSMU channels
    #CN [ch#][,ch#][,ch#]......
    HP4142.write(cn_command)#("CN 1,4,8\n") #enable MPSMU1 MPSMU8
    
    #FMT command clears the HP4142B output data buffer and spoecifies measurement data output format.
    #FMT output data formatr [,output data mode]
    #needs to check  which one is better 1 or 2 depending on data processing, and 
    #also check what does AV 64 means, whats its purpose
    HP4142.write("FMT 2;AV 64,1\n") #enable MPSMU1 MPSMU8
    
    #MM command sets the measurement mode and measurement units
    #MM measurement mode, ch#, ch#, ch#, ch....#
    #MM 1 spot measurement...
    HP4142.write("MM 1,1,4,6,7,8\n") #set measurement mode to spot IV at MPSMU4
    
    status = HP4142.query_ascii_values("ERR?\n", converter='s')
    print(status)
    if("".join(status)[:4]=="0000"):
        print("HP4142B initialized")
    
    input("1: ")
    checking_lop = HP4142.query_ascii_values("LOP?", converter ='s')
    print(checking_lop)
    
    
    
    #DV forces output voltage from ther specified unit
    #DV ch#, output range, output voltage, [,I compliance][, complienace polarity mode]
    #ouput range = 0-auto range, 11: 2v limited auto range, 12:20v lar, 13: 40v lar, 14:100v lar
    
    HP4142.write("DV 7,0,0") #set measurement mode to spot IV at MPSMU4
    HP4142.write("DV 1,0,-2.5")
    HP4142.write("DV 8,0,-2.5") #set measurement mode to spot IV at MPSMU4
   
    input("checking values")
   #TI command is the trigger command for high speed spot current (I) measurement.
   #this command performs a high speed spot I measurement, independent of the source mode (V/I/ source mode, )
   #TI ch#[, I measurement range]
    output = HP4142.query_ascii_values("TI 7,0\n", converter='s')
    print(output)
    time.sleep(3)
    output=HP4142.query_ascii_values( "TI 8,0\n", converter='s')
    print(1)
    print(output)
    output=HP4142.query_ascii_values( "TI 1,0\n", converter='s')
    print(2)
    print(output)
    
    
    output=HP4142.query_ascii_values( "*OPC?\n")
    print(3)
    print(output)
    # output=HP4142.query_ascii_values()
    # print(4)
    print(HP4142)
    return HP4142


# HP4142_debug("GPIB0::19::INSTR")


def clear_Offsets_PM(addr_x):
    setResult  = ctypes.c_double()
    setFreq = ctypes.c_long()
    PulPwr=ctypes.c_double()
    PkPwr=ctypes.c_double()
    AvgPwr=ctypes.c_double()
    DutyCyc=ctypes.c_double()
    LV_LB_API2.LB_SetOffsetEnabled.argtypes = [ctypes.c_long, ctypes.c_bool]
    LV_LB_API2.LB_SetOffsetEnabled(ctypes.c_long(addr_x), ctypes.c_bool(0))
    #This is to test that the offsets were applied correctly
    LV_LB_API2.LB_MeasurePulse.argtypes=[ctypes.c_int,ctypes.POINTER(c_double), 
                                      ctypes.POINTER(c_double),ctypes.POINTER(c_double),
                                      ctypes.POINTER(c_double)]
    LV_LB_API2.LB_MeasurePulse(c_int(addr_x), PulPwr,PkPwr,AvgPwr,DutyCyc)
    return PulPwr.value, PkPwr.value, AvgPwr.value, DutyCyc.value
