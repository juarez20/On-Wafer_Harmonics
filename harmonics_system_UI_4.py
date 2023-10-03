# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal 

import easygui as easygui
import configparser
import time
import csv
import sys
import os

import initialize_system_and_load_files as init_sys
import functions_and_definitions as definitions_m

import reading_files_to_get_settings_for_TEST as get_test_sequeces
import reading_and_writing_on_files as read_write_f
import calibration_functions_and_readbacks as cal_func_reads
import data_container_lists as data_lists

import Calibration_Sequence_AUTO_STEP as calibration_sequence
import test_dies_index_wafermap as testing_dies

import Calibration_Sequence_AUTO_STEP as cal_syst
import test_dies_index_wafermap as test_dies

import threading
from threading import*

global system_interrupt
system_interrupt = False
global t1

global all_process


QtCore.pyqtRemoveInputHook()

global exit_event
exit_event = threading.Event()

class start_calibration_worker_function(QObject):
    finished = pyqtSignal()
    
    def run_calibration(self, full_calibration, partial_calibration, pin_lb, pout_lb, sigGenAddr, Ampl, freq, pin_lb_ini, pout_lb_ini, userPath, userfileName, lot, wafer, die, device, setup, v_left, v_center, v_right, SigAnaAddr, full_path, power_level_file_location):
        finished_cal = calibration_sequence.harmonics_calibration_sequence(full_calibration, partial_calibration, pin_lb, pout_lb, sigGenAddr, Ampl, freq, pin_lb_ini, pout_lb_ini, userPath, userfileName, lot, wafer, die, device, setup, v_left, v_center, v_right, SigAnaAddr, full_path, power_level_file_location)
        # self.stop_system_run()
        self.finished.emit()
        
    def stop_system_run(self):
        self.run_calibration = False
       

class start_test_sequence_worker_function(QObject):
    finished = pyqtSignal()
    def run_harm_test(self, probe_addr, die_probing_index_file, get_subdies_index_and_label, smuAddr, v_left_addr, v_center_addr, v_right_addr, voltages_level_list, sigGenAddr, Amp, freq, power_level_list, addr_pin, addr_pout, SigAnaAddr, second_harmonics, third_harmonics, user_file_name, userPath, Lot, Wafer, pin_offset_val, pout_offset_val, reading_bias_current):
        finished_test = testing_dies.probing_dies_through_indexes_provided_by_user(probe_addr, die_probing_index_file, get_subdies_index_and_label, smuAddr, v_left_addr, v_center_addr, v_right_addr, voltages_level_list, sigGenAddr, Amp, freq, power_level_list, addr_pin, addr_pout, SigAnaAddr, second_harmonics, third_harmonics, user_file_name, userPath, Lot, Wafer, pin_offset_val, pout_offset_val, reading_bias_current)        
        self.finished.emit()
        
    def stop_system_run(self):
        self.run_harm_test = False
    
class Ui_harmonics_system(object):
    # def __init__(self, parent=None):
    #     super().__init__(parent)
    
    def setupUi(self, harmonics_system):
        harmonics_system.setObjectName("harmonics_system")
        harmonics_system.setWindowModality(QtCore.Qt.ApplicationModal)
        harmonics_system.resize(920, 710)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setKerning(False)
        harmonics_system.setFont(font)
        harmonics_system.setMouseTracking(True)
        harmonics_system.setWhatsThis("")
        harmonics_system.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(harmonics_system)
        self.centralwidget.setObjectName("centralwidget")
        self.load_ini_file_label = QtWidgets.QLabel(self.centralwidget)
        self.load_ini_file_label.setGeometry(QtCore.QRect(20, 10, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.load_ini_file_label.setFont(font)
        self.load_ini_file_label.setMouseTracking(True)
        self.load_ini_file_label.setObjectName("load_ini_file_label")
        self.load_ini_fil_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.load_ini_fil_entry.setGeometry(QtCore.QRect(20, 40, 811, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.load_ini_fil_entry.setFont(font)
        self.load_ini_fil_entry.setWhatsThis("")
        self.load_ini_fil_entry.setAccessibleName("")
        self.load_ini_fil_entry.setText("")
        self.load_ini_fil_entry.setObjectName("load_ini_fil_entry")
        self.ini_search_button = QtWidgets.QToolButton(self.centralwidget)
        self.ini_search_button.setGeometry(QtCore.QRect(840, 40, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(20)
        font.setKerning(False)
        self.ini_search_button.setFont(font)
        self.ini_search_button.setObjectName("ini_search_button")
        self.load_map_level_file_label = QtWidgets.QLabel(self.centralwidget)
        self.load_map_level_file_label.setGeometry(QtCore.QRect(20, 70, 345, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.load_map_level_file_label.setFont(font)
        self.load_map_level_file_label.setMouseTracking(True)
        self.load_map_level_file_label.setObjectName("load_map_level_file_label")
        self.die_map_pwr_level_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.die_map_pwr_level_entry.setGeometry(QtCore.QRect(20, 100, 811, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.die_map_pwr_level_entry.setFont(font)
        self.die_map_pwr_level_entry.setWhatsThis("")
        self.die_map_pwr_level_entry.setAccessibleName("")
        self.die_map_pwr_level_entry.setText("")
        self.die_map_pwr_level_entry.setObjectName("die_map_pwr_level_entry")
        self.map_level_search = QtWidgets.QToolButton(self.centralwidget)
        self.map_level_search.setGeometry(QtCore.QRect(840, 100, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(20)
        font.setKerning(False)
        self.map_level_search.setFont(font)
        self.map_level_search.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.map_level_search.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.map_level_search.setObjectName("map_level_search")
        self.pin_lb_addr_label = QtWidgets.QLabel(self.centralwidget)
        self.pin_lb_addr_label.setGeometry(QtCore.QRect(20, 130, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.pin_lb_addr_label.setFont(font)
        self.pin_lb_addr_label.setMouseTracking(True)
        self.pin_lb_addr_label.setObjectName("pin_lb_addr_label")
        self.pin_lb_addr_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.pin_lb_addr_entry.setGeometry(QtCore.QRect(20, 160, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.pin_lb_addr_entry.setFont(font)
        self.pin_lb_addr_entry.setWhatsThis("")
        self.pin_lb_addr_entry.setAccessibleName("")
        self.pin_lb_addr_entry.setText("")
        self.pin_lb_addr_entry.setObjectName("pin_lb_addr_entry")
        self.pout_lb_addr_label = QtWidgets.QLabel(self.centralwidget)
        self.pout_lb_addr_label.setGeometry(QtCore.QRect(20, 190, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.pout_lb_addr_label.setFont(font)
        self.pout_lb_addr_label.setMouseTracking(True)
        self.pout_lb_addr_label.setObjectName("pout_lb_addr_label")
        self.pout_lb_addr_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.pout_lb_addr_entry.setGeometry(QtCore.QRect(20, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.pout_lb_addr_entry.setFont(font)
        self.pout_lb_addr_entry.setWhatsThis("")
        self.pout_lb_addr_entry.setAccessibleName("")
        self.pout_lb_addr_entry.setText("")
        self.pout_lb_addr_entry.setObjectName("pout_lb_addr_entry")
        
        self.freq_label = QtWidgets.QLabel(self.centralwidget)
        self.freq_label.setGeometry(QtCore.QRect(20, 270, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.freq_label.setFont(font)
        self.freq_label.setMouseTracking(True)
        self.freq_label.setObjectName("freq_label")
        
        self.freq_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.freq_entry.setGeometry(QtCore.QRect(20, 300, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.freq_entry.setFont(font)
        self.freq_entry.setWhatsThis("")
        self.freq_entry.setAccessibleName("")
        self.freq_entry.setText("")
        self.freq_entry.setObjectName("freq_entry")
        
        
        
        self.lot_label = QtWidgets.QLabel(self.centralwidget)
        self.lot_label.setGeometry(QtCore.QRect(20, 320, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.lot_label.setFont(font)
        self.lot_label.setMouseTracking(True)
        self.lot_label.setObjectName("lot_label")
        
        self.lot_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.lot_entry.setGeometry(QtCore.QRect(20, 350, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.lot_entry.setFont(font)
        self.lot_entry.setWhatsThis("")
        self.lot_entry.setAccessibleName("")
        self.lot_entry.setText("")
        self.lot_entry.setObjectName("lot_entry")
        
        self.wafer_name_label = QtWidgets.QLabel(self.centralwidget)
        self.wafer_name_label.setGeometry(QtCore.QRect(20, 380, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.wafer_name_label.setFont(font)
        self.wafer_name_label.setMouseTracking(True)
        self.wafer_name_label.setObjectName("wafer_name_label")
        self.wafer_name_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.wafer_name_entry.setGeometry(QtCore.QRect(20, 410, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.wafer_name_entry.setFont(font)
        self.wafer_name_entry.setWhatsThis("")
        self.wafer_name_entry.setAccessibleName("")
        self.wafer_name_entry.setText("")
        self.wafer_name_entry.setObjectName("wafer_name_entry")
        
        self.die_setup_label = QtWidgets.QLabel(self.centralwidget)
        self.die_setup_label.setGeometry(QtCore.QRect(200, 380, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.die_setup_label.setFont(font)
        self.die_setup_label.setMouseTracking(True)
        self.die_setup_label.setObjectName("die_setup_label")
        
        self.die_setup_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.die_setup_entry.setGeometry(QtCore.QRect(200, 410, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.die_setup_entry.setFont(font)
        self.die_setup_entry.setWhatsThis("")
        self.die_setup_entry.setAccessibleName("")
        self.die_setup_entry.setText("")
        self.die_setup_entry.setObjectName("die_setup_entry")
        
        
        
        
        self.enable_bias_reading_box = QtWidgets.QCheckBox(self.centralwidget)
        self.enable_bias_reading_box.setGeometry(QtCore.QRect(380, 410, 480, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setKerning(False)
        self.enable_bias_reading_box.setFont(font)
        self.enable_bias_reading_box.setStyleSheet("")
        self.enable_bias_reading_box.setChecked(True)
        self.enable_bias_reading_box.setObjectName("enable_bias_reading_box")
        
        
        self.test_sequence_label = QtWidgets.QLabel(self.centralwidget)
        self.test_sequence_label.setGeometry(QtCore.QRect(220, 140, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setKerning(False)
        self.test_sequence_label.setFont(font)
        self.test_sequence_label.setMouseTracking(True)
        self.test_sequence_label.setObjectName("test_sequence_label")
        self.subsite_label_label = QtWidgets.QLabel(self.centralwidget)
        self.subsite_label_label.setGeometry(QtCore.QRect(510, 140, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setKerning(False)
        self.subsite_label_label.setFont(font)
        self.subsite_label_label.setMouseTracking(True)
        self.subsite_label_label.setObjectName("subsite_label_label")
        self.test_sequence_refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_sequence_refresh_button.setGeometry(QtCore.QRect(420, 360, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setKerning(False)
        self.test_sequence_refresh_button.setFont(font)
        self.test_sequence_refresh_button.setObjectName("test_sequence_refresh_button")
        self.save_labels_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_labels_button.setGeometry(QtCore.QRect(740, 360, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setKerning(False)
        self.save_labels_button.setFont(font)
        self.save_labels_button.setObjectName("save_labels_button")
        
        self.load_subsite_label_file_button = QtWidgets.QToolButton(self.centralwidget)
        self.load_subsite_label_file_button.setGeometry(QtCore.QRect(740, 320, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.load_subsite_label_file_button.setFont(font)
        self.load_subsite_label_file_button.setObjectName("load_subsite_label_file_button")
        
        self.band_selection_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.band_selection_comboBox.setGeometry(QtCore.QRect(140, 540, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.band_selection_comboBox.setFont(font)
        self.band_selection_comboBox.setObjectName("band_selection_comboBox")
        self.band_selection_comboBox.addItem("")
        self.band_selection_comboBox.addItem("")
        
        self.band_selection_label = QtWidgets.QLabel(self.centralwidget)
        self.band_selection_label.setGeometry(QtCore.QRect(20, 540, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.band_selection_label.setFont(font)
        self.band_selection_label.setMouseTracking(True)
        self.band_selection_label.setObjectName("band_selection_label")
        
        self.wafer_mode_label = QtWidgets.QLabel(self.centralwidget)
        self.wafer_mode_label.setGeometry(QtCore.QRect(310, 540, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)        
        self.wafer_mode_label.setFont(font)
        self.wafer_mode_label.setMouseTracking(True)
        self.wafer_mode_label.setObjectName("wafer_mode_label")
        self.wafer_mode_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.wafer_mode_comboBox.setGeometry(QtCore.QRect(420, 540, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.wafer_mode_comboBox.setFont(font)
        self.wafer_mode_comboBox.setObjectName("wafer_mode_comboBox")
        self.wafer_mode_comboBox.addItem("")
        self.wafer_mode_comboBox.addItem("")
        # self.directory_saving_path_label = QtWidgets.QLabel(self.centralwidget)
        # self.directory_saving_path_label.setGeometry(QtCore.QRect(20, 450, 171, 41))
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        self.cal_mode_label = QtWidgets.QLabel(self.centralwidget)
        self.cal_mode_label.setGeometry(QtCore.QRect(540, 540, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.cal_mode_label.setFont(font)
        self.cal_mode_label.setMouseTracking(True)
        self.cal_mode_label.setObjectName("cal_mode_label")
        self.cal_mode_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.cal_mode_comboBox.setGeometry(QtCore.QRect(670, 540, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.cal_mode_comboBox.setFont(font)
        self.cal_mode_comboBox.setObjectName("wafer_mode_comboBox")
        self.cal_mode_comboBox.addItem("")
        self.cal_mode_comboBox.addItem("")
        
        
        self.directory_saving_path_label = QtWidgets.QLabel(self.centralwidget)
        self.directory_saving_path_label.setGeometry(QtCore.QRect(20, 450, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.directory_saving_path_label.setFont(font)
        self.directory_saving_path_label.setMouseTracking(True)
        self.directory_saving_path_label.setObjectName("directory_saving_path_label")
        self.file_name_label = QtWidgets.QLabel(self.centralwidget)
        self.file_name_label.setGeometry(QtCore.QRect(20, 490, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.file_name_label.setFont(font)
        self.file_name_label.setMouseTracking(True)
        self.file_name_label.setObjectName("file_name_label")
        self.directory_saving_path_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_saving_path_entry.setGeometry(QtCore.QRect(150, 460, 651, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.directory_saving_path_entry.setFont(font)
        self.directory_saving_path_entry.setWhatsThis("")
        self.directory_saving_path_entry.setAccessibleName("")
        self.directory_saving_path_entry.setText("")
        self.directory_saving_path_entry.setObjectName("directory_saving_path_entry")
        self.file_name_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.file_name_entry.setGeometry(QtCore.QRect(100, 500, 701, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.file_name_entry.setFont(font)
        self.file_name_entry.setWhatsThis("")
        self.file_name_entry.setAccessibleName("")
        self.file_name_entry.setText("")
        self.file_name_entry.setObjectName("file_name_entry")
        
        # self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        # self.tableWidget.setGeometry(QtCore.QRect(20, 540, 781, 301))
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # self.tableWidget.setFont(font)
        # self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(16)
        # self.tableWidget.setRowCount(0)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(3, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(4, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(5, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(6, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(7, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(8, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(9, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(10, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(11, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(12, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(13, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(14, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # item.setFont(font)
        # self.tableWidget.setHorizontalHeaderItem(15, item)
        self.calibration_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.calibration_radioButton.setGeometry(QtCore.QRect(540, 600, 131, 17))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(11)
        font.setKerning(False)
        self.calibration_radioButton.setFont(font)
        self.calibration_radioButton.setObjectName("calibration_radioButton")
        self.test_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.test_radioButton.setGeometry(QtCore.QRect(420, 600, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(11)
        font.setKerning(False)
        self.test_radioButton.setFont(font)
        self.test_radioButton.setObjectName("test_radioButton")
        self.start_commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.start_commandLinkButton.setGeometry(QtCore.QRect(440, 640, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(13)
        font.setKerning(False)
        self.start_commandLinkButton.setFont(font)
        self.start_commandLinkButton.setObjectName("start_commandLinkButton")
        self.stop_commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.stop_commandLinkButton.setGeometry(QtCore.QRect(570, 640, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        font.setKerning(False)
        self.stop_commandLinkButton.setFont(font)
        self.stop_commandLinkButton.setObjectName("stop_commandLinkButton")
        # self.ect_label = QtWidgets.QLabel(self.centralwidget)
        # self.ect_label.setGeometry(QtCore.QRect(20, 850, 221, 41))
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setKerning(False)
        # self.ect_label.setFont(font)
        # self.ect_label.setMouseTracking(True)
        # self.ect_label.setObjectName("ect_label")
        # self.ect_entry = QtWidgets.QLineEdit(self.centralwidget)
        # self.ect_entry.setGeometry(QtCore.QRect(220, 860, 581, 31))
        # font = QtGui.QFont()
        # font.setFamily("Cambria")
        # font.setPointSize(10)
        # font.setBold(False)
        # font.setItalic(False)
        # font.setWeight(50)
        # font.setKerning(False)
        # self.ect_entry.setFont(font)
        # self.ect_entry.setWhatsThis("")
        # self.ect_entry.setAccessibleName("")
        # self.ect_entry.setText("")
        # self.ect_entry.setObjectName("ect_entry")
        
        self.test_sequence_holder = QtWidgets.QListWidget(self.centralwidget)
        self.test_sequence_holder.setGeometry(QtCore.QRect(220, 170, 191, 211))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.test_sequence_holder.setFont(font)
        self.test_sequence_holder.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.test_sequence_holder.setObjectName("test_sequence_holder")
        
        self.subsite_label_holder = QtWidgets.QListWidget(self.centralwidget)
        self.subsite_label_holder.setGeometry(QtCore.QRect(510, 170, 221, 211))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.subsite_label_holder.setFont(font)
        self.subsite_label_holder.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.subsite_label_holder.setObjectName("subsite_label_holder")
        
        harmonics_system.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(harmonics_system)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(10)
        font.setKerning(False)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        harmonics_system.setStatusBar(self.statusbar)

        self.retranslateUi(harmonics_system)
        QtCore.QMetaObject.connectSlotsByName(harmonics_system)
        
        #Connecting all objects buttons and creating responses
        self.ini_search_button.clicked.connect(self.open_ini_cal_file)
        self.map_level_search.clicked.connect(self.load_map_pwr_level_file)
        self.add_test_sequence_to_Qlist()
        self.test_sequence_refresh_button.clicked.connect(self.add_test_sequence_to_Qlist)
        self.load_subsite_label_file_button.clicked.connect(self.load_subsite_stv_file)
        self.save_labels_button.clicked.connect(self.saving_subsite_labels_file)
        
        
        #FOR NOW whenpressing start we show all the content from the  UI
        self.start_commandLinkButton.clicked.connect(self.thread)
        self.stop_commandLinkButton.clicked.connect(self.stop_button_pressed)
        
        
        
        
        
        
    def retranslateUi(self, harmonics_system):
        _translate = QtCore.QCoreApplication.translate
        harmonics_system.setWindowTitle(_translate("harmonics_system", "Harmonics System "))
        self.load_ini_file_label.setText(_translate("harmonics_system", "Load Calibration File"))
        self.ini_search_button.setText(_translate("harmonics_system", "..."))
        self.load_map_level_file_label.setText(_translate("harmonics_system", "Load DIE MAP (for test) OR Power Level File (for calibration)"))
        self.map_level_search.setText(_translate("harmonics_system", "..."))
        self.pin_lb_addr_label.setText(_translate("harmonics_system", "Pin LB Addr"))
        self.pout_lb_addr_label.setText(_translate("harmonics_system", "Pout LB Addr"))
        self.freq_label.setText(_translate("harmonics_system", "Frequency (MHz)"))
        self.lot_label.setText(_translate("harmonics_system", "Lot"))
        self.wafer_name_label.setText(_translate("harmonics_system", "Wafer Name"))
        self.die_setup_label.setText(_translate("harmonics_system", "Die _ Setup"))
        self.enable_bias_reading_box.setText(_translate("harmonics_system", "Enable (checked) - Disable (unchecked) Current Reading"))
        self.test_sequence_label.setText(_translate("harmonics_system", "Test Sequence Selection"))
        self.subsite_label_label.setText(_translate("harmonics_system", "Subsite Label Selection"))
        self.test_sequence_refresh_button.setText(_translate("harmonics_system", "Refresh"))
        self.save_labels_button.setText(_translate("harmonics_system", "Save..."))
        self.load_subsite_label_file_button.setText(_translate("harmonics_system", "..."))
        self.band_selection_comboBox.setItemText(0, _translate("harmonics_system", "Low Band"))
        self.band_selection_comboBox.setItemText(1, _translate("harmonics_system", "High Band"))
        self.band_selection_label.setText(_translate("harmonics_system", "Band Selection"))
        self.wafer_mode_label.setText(_translate("harmonics_system", "WAFER MODE"))
        self.wafer_mode_comboBox.setItemText(0, _translate("harmonics_system", "DIE"))
        self.wafer_mode_comboBox.setItemText(1, _translate("harmonics_system", "FULL"))
        
        self.cal_mode_label.setText(_translate("harmonics_system", "CALIBRATION MODE"))
        self.cal_mode_comboBox.setItemText(0, _translate("harmonics_system", "FULL"))
        self.cal_mode_comboBox.setItemText(1, _translate("harmonics_system", "PARTIAL"))
        
        self.directory_saving_path_label.setText(_translate("harmonics_system", "Directory Saving Path"))
        self.file_name_label.setText(_translate("harmonics_system", "File Name"))
        # item = self.tableWidget.horizontalHeaderItem(0)
        # item.setText(_translate("harmonics_system", "Lot"))
        # item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText(_translate("harmonics_system", "Wafer"))
        # item = self.tableWidget.horizontalHeaderItem(2)
        # item.setText(_translate("harmonics_system", "Die"))
        # item = self.tableWidget.horizontalHeaderItem(3)
        # item.setText(_translate("harmonics_system", "Subdie"))
        # item = self.tableWidget.horizontalHeaderItem(4)
        # item.setText(_translate("harmonics_system", "Freq"))
        # item = self.tableWidget.horizontalHeaderItem(5)
        # item.setText(_translate("harmonics_system", "Target Power"))
        # item = self.tableWidget.horizontalHeaderItem(6)
        # item.setText(_translate("harmonics_system", "Output Power"))
        # item = self.tableWidget.horizontalHeaderItem(7)
        # item.setText(_translate("harmonics_system", "Insertion Loss"))
        # item = self.tableWidget.horizontalHeaderItem(8)
        # item.setText(_translate("harmonics_system", "V left"))
        # item = self.tableWidget.horizontalHeaderItem(9)
        # item.setText(_translate("harmonics_system", "V center"))
        # item = self.tableWidget.horizontalHeaderItem(10)
        # item.setText(_translate("harmonics_system", "V right"))
        # item = self.tableWidget.horizontalHeaderItem(11)
        # item.setText(_translate("harmonics_system", "I left"))
        # item = self.tableWidget.horizontalHeaderItem(12)
        # item.setText(_translate("harmonics_system", "I center"))
        # item = self.tableWidget.horizontalHeaderItem(13)
        # item.setText(_translate("harmonics_system", "I right"))
        # item = self.tableWidget.horizontalHeaderItem(14)
        # item.setText(_translate("harmonics_system", "2 Harm"))
        # item = self.tableWidget.horizontalHeaderItem(15)
        # item.setText(_translate("harmonics_system", "3 Harm"))
        self.calibration_radioButton.setText(_translate("harmonics_system", "CALIBRATION"))
        self.test_radioButton.setText(_translate("harmonics_system", "TEST"))
        self.start_commandLinkButton.setText(_translate("harmonics_system", "START"))
        self.stop_commandLinkButton.setText(_translate("harmonics_system", "STOP"))
        # self.ect_label.setText(_translate("harmonics_system", "Estimated Completion Time"))

    def open_ini_cal_file(self):
        fileName = easygui.fileopenbox(title='Select INI File', default="*", filetypes=["*.ini"])
        if fileName == None:
            pass
        else:
            # f = open(fileName, 'r')
            # with f:
            #     data = f.read()
            self.load_ini_fil_entry.setText(fileName)
            self.show_values_on_UI(fileName)

    def show_values_on_UI(self, file_ini):
        config = configparser.ConfigParser()
        config.sections()
        config.read(file_ini)
        self.pin_lb_addr_entry.setText(config['Hardware']['pin_power_meter'])
        self.pout_lb_addr_entry.setText(config['Hardware']['pout_power_meter'])

    def load_map_pwr_level_file(self):
        mp_l_file = easygui.fileopenbox(title='Select MAP - PWR LEVEL file', default="*")
        if mp_l_file is None:
            pass
        else:
            self.die_map_pwr_level_entry.setText(mp_l_file)
    
    def add_test_sequence_to_Qlist(self):
        list_of_test_sequences = get_test_sequeces.get_all_the_name_of_the_files_for_the_SETUPs()
        self.test_sequence_holder.clear()
        time.sleep(0.5)
        self.test_sequence_holder.addItems(list_of_test_sequences)
        # for each_sequence in list_of_test_sequences:
    
    def load_subsite_stv_file(self):
        self.subsite_label_holder.clear()
        time.sleep(0.2)
        stv_file = easygui.fileopenbox(title="Load .STV file", default="*", filetypes=["*.stv"])
        if stv_file is None:
            pass
        else:
            #read the file 
            try:
                get_subdies_lables = read_write_f.create_subdie_mapping_container(stv_file)
                for each_label in get_subdies_lables:
                    each_label = str(each_label[0]) +", " +  str(each_label[1]) +", " +  str(each_label[2]) +", " +  str(each_label[3])
                    
                    self.subsite_label_holder.addItem(each_label)
            except:
                print("Please check that your file has no extra character in line like a 'SPACE' \nAlso, check that the STV and TXT file has the guidelines needed.")
            
    def saving_subsite_labels_file(self):
        selected_subsite_labels = [item.text() for item in self.subsite_label_holder.selectedItems()]
        #converting list into list of lists
        temp_selected_list = []
        for each_list in selected_subsite_labels:
            temp_list = each_list.split(', ')
            temp_selected_list.append(temp_list)
            
        
        save_file_labels = easygui.filesavebox(title="Save Subsite Label Selection", filetypes=["*.stv"])
        save_file_labels = save_file_labels + ".stv"
        with open(save_file_labels, 'w', newline="") as temp_file:
            writer = csv.writer(temp_file)
            writer.writerows(temp_selected_list)
            
        # temp_subsite_file = open(save_file_labels, 'w')
        # temp_subsite_file = csv.write(temp_subsite_file)
        # temp_subsite_file.writerrows(selected_subsite_labels)
        
    def get_all_the_content_from_UI(self):
        ini_file_entry = self.load_ini_fil_entry.text()
        die_map_pwr_level_file = self.die_map_pwr_level_entry.text()
        pin_lb_addr = self.pin_lb_addr_entry.text()
        pout_lb_add = self.pout_lb_addr_entry.text()
        lot_description = self.lot_entry.text()
        wafer_name = self.wafer_name_entry.text()
        test_sequence_selection = [test_sequence.text() for test_sequence in self.test_sequence_holder.selectedItems()]
        subsite_label_selection = [subsite_selection.text() for subsite_selection in self.subsite_label_holder.selectedItems()]
        # print(subsite_label_selection)
        # print(subsite_label_selection[0])
        # new_subsite_label_mode = list(subsite_label_selection[0].split(", "))
        # print(new_subsite_label_mode)
        band_selection = self.band_selection_comboBox.currentText()
        wafer_mode = self.wafer_mode_comboBox.currentText()        
        directory_saving_path = self.directory_saving_path_entry.text()
        file_name = self.file_name_entry.text()
        
        cal_mode = self.cal_mode_comboBox.currentText()
        freq = self.freq_entry.text()
        die_setup = self.die_setup_entry.text()
        return ini_file_entry, die_map_pwr_level_file, pin_lb_addr, pout_lb_add, lot_description, wafer_name, test_sequence_selection, subsite_label_selection, band_selection, wafer_mode, directory_saving_path, file_name, cal_mode, freq, die_setup
    
    
    def update_the_main_UI(self):
        print("go back to the main window")
        
        
    def thread(self):
        global t1
        t1 = Thread(target=self.long_running_tasks)
        t1.start()
        
    
    def long_running_tasks(self):
        ui_content = self.get_all_the_content_from_UI()
        ini_file_entry_lr = ui_content[0]
        die_map_pwr_level_file_lr = ui_content[1]
        pin_lb_addr_lr = ui_content[2]
        pout_lb_addr_lr = ui_content[3]
        lot_description_lr = ui_content[4]
        wafer_name_lr = ui_content[5]
        test_sequence_selection_lr = ui_content[6]
        subsite_label_selection_lr = ui_content[7]
        band_selection_lr = ui_content[8]
        wafer_mode_lr = ui_content[9]
        directory_saving_path_lr = ui_content[10]
        file_name_lr = ui_content[11]
        cal_mode_lr = ui_content[12]
        freq_lr = ui_content[13]
        die_setup_lr = ui_content[14]
        
        #getting content from the INI file
        get_entire_values_from_ini_file = read_write_f.reading_the_entire_INI_file(ini_file_entry_lr)
        pin_lb_addr_lr_i = get_entire_values_from_ini_file[0]
        pout_lb_addr_lr_i = get_entire_values_from_ini_file[1] 
        sigGen_addr_lr = get_entire_values_from_ini_file[2]
        sigAna_addr_lr = get_entire_values_from_ini_file[3]
        src_meter_addr_lr = get_entire_values_from_ini_file[4]
        prober_addr_lr = get_entire_values_from_ini_file[5]
        pin_offset_lr = get_entire_values_from_ini_file[6] 
        amplitude_offset = get_entire_values_from_ini_file[7] 
        pout_offset_lr = get_entire_values_from_ini_file[8] 
        sec_harm_offset_lr = get_entire_values_from_ini_file[9] 
        trd_harm_offset_lr = get_entire_values_from_ini_file[10]
        left_smu_addr_lr = get_entire_values_from_ini_file[11]
        center_smu_addr_lr =  get_entire_values_from_ini_file[12]
        right_smu_addr_lr = get_entire_values_from_ini_file[13]
        
        # print(self.enable_bias_reading_box)
        enable_reading_current = False
        if self.enable_bias_reading_box.isChecked():
            print("We should measure bias")
            enable_reading_current = True

        #checking and show the image for the
        band_range = ""
        band_image_to_show = ''
        if band_selection_lr  == "Low Band":
            band_range = "Low Band"
            band_image_to_show = 'low_band_side.jpg'
        elif band_selection_lr == "High Band":
            band_range = "High Band"
            band_image_to_show = 'high_band_side.jpg'
            
        band_band_check_message = f"{band_range} has been selected. Please move the knobs pointing to the correct direction"
        image_band_select = band_image_to_show
        image_band_select = definitions_m.locating_image_and_returning_its_path(image_band_select)
        image_band_reply = definitions_m.show_image_and_message(image_band_select, band_band_check_message)
        if image_band_reply == "Cancel" or image_band_reply == None:
            raise SystemExit()
            
            
        
        if self.calibration_radioButton.isChecked():
            self.calibration_radioButton.setEnabled(False)
            self.test_radioButton.setEnabled(False)
            
            #Create a QThread object
            self.thread = QThread()
            #Create a worker object
            self.worker = start_calibration_worker_function()
            #move the worker to the thread
            self.worker.moveToThread(self.thread)
            #connect signals and slots
            if cal_mode_lr == "FULL":
                full_calibration = True
            else:
                full_calibration = False
            if cal_mode_lr == "PARTIAL":
                partial_calibration = True
            else:
                partial_calibration = False
            
            Ampl_for_cal = 75.5
            
            #we now need to adjust the frequency using the function lllss
            freq_lr = cal_func_reads.normalizing_freq_entry_value(freq_lr)
            
            #initializing the conditions
            pin_lb_ini, pout_lb_ini, dc_source = init_sys.initializing_instruments_0_reply(pin_lb_addr_lr, pout_lb_addr_lr, sigGen_addr_lr, freq_lr, sigAna_addr_lr, src_meter_addr_lr, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr)
            device = "test"
            setup = "Harmonics"
            
            self.thread.started.connect(lambda:self.worker.run_calibration(full_calibration, partial_calibration, pin_lb_addr_lr, pout_lb_addr_lr, sigGen_addr_lr, Ampl_for_cal, freq_lr, pin_lb_ini, pout_lb_ini, directory_saving_path_lr, file_name_lr, lot_description_lr, wafer_name_lr, die_setup_lr, device, setup, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr, sigAna_addr_lr, ini_file_entry_lr, die_map_pwr_level_file_lr))
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
    
            self.thread.start()
            
            self.calibration_radioButton.setEnabled(True) 
            self.test_radioButton.setEnabled(True)
            self.start_commandLinkButton.setEnabled(True)
            
            cal_syst.harmonics_calibration_sequence(full_calibration, partial_calibration, pin_lb_addr_lr, pout_lb_addr_lr, sigGen_addr_lr, Ampl_for_cal, freq_lr, pin_lb_ini, pout_lb_ini, directory_saving_path_lr, file_name_lr, lot_description_lr, wafer_name_lr, die_setup_lr, device, setup, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr, sigAna_addr_lr, ini_file_entry_lr, die_map_pwr_level_file_lr)
            
            self.start_commandLinkButton.setEnabled(True)
            self.calibration_radioButton.setEnabled(True)
            self.test_radioButton.setEnabled(True)
            
            
        if self.test_radioButton.isChecked():
            #Create a worker object
            self.worker_1 = start_test_sequence_worker_function()
            #Create a QThread object
            self.thread_1 = QThread()
            
            #move the worker to the thread
            self.worker_1.moveToThread(self.thread_1)
            
            freq_lr = cal_func_reads.normalizing_freq_entry_value(freq_lr)
            pin_lb_ini, pout_lb_ini, dc_source = init_sys.initializing_instruments_0_reply(pin_lb_addr_lr, pout_lb_addr_lr, sigGen_addr_lr, freq_lr, sigAna_addr_lr, src_meter_addr_lr, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr)
            
            # if str(freq_lr) == str()            
            #we need to supply all the name of the selected test sequences becasue we cannot proccess them outside the function., 
            # we can create the list of list in here.
            # and passing the values as place holders instead of stand-alone arguments....
            
            #let us process all the tes sequences before, and we can send a all the conditions before 
            voltages_level_mlist, power_level_mlist = data_lists.get_master_volatgeLevels_and_pwrLvls_lists(test_sequence_selection_lr)
            print("Voltage Values and Power Levels")
            print(voltages_level_mlist)
            print(power_level_mlist)
            
            self.thread_1.started.connect(lambda:self.worker_1.run_harm_test(prober_addr_lr, die_map_pwr_level_file_lr, subsite_label_selection_lr, src_meter_addr_lr, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr, voltages_level_mlist, sigGen_addr_lr, amplitude_offset, freq_lr, power_level_mlist, pin_lb_ini, pout_lb_ini, sigAna_addr_lr,  sec_harm_offset_lr, trd_harm_offset_lr, file_name_lr, directory_saving_path_lr, lot_description_lr, wafer_name_lr, pin_offset_lr, pout_offset_lr, enable_reading_current))
            
            # self.show()
            self.worker_1.finished.connect(self.thread_1.quit)
            self.worker_1.finished.connect(self.worker_1.deleteLater)
            self.thread_1.finished.connect(self.thread_1.deleteLater)
            
            self.start_commandLinkButton.setEnabled(False)
            self.calibration_radioButton.setEnabled(False)
            self.test_radioButton.setEnabled(False)
            
            self.thread_1.start()
            
            self.thread_1.finished.connect(
                lambda: self.start_commandLinkButton.setEnabled(True))
            self.thread_1.finished.connect(
                lambda: self.calibration_radioButton.setEnabled(True))
            self.thread_1.finished.connect(
                lambda: self.test_radioButton.setEnabled(True))
            
            # test_dies.run_harm_test(prober_addr_lr, die_map_pwr_level_file_lr, subsite_label_selection_lr, src_meter_addr_lr, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr, voltages_level_mlist, sigGen_addr_lr, amplitude_offset, freq_lr, power_level_mlist, pin_lb_ini, pout_lb_ini, sigAna_addr_lr,  sec_harm_offset_lr, trd_harm_offset_lr, file_name_lr, directory_saving_path_lr, lot_description_lr, wafer_name_lr, pin_offset_lr, pout_offset_lr)
            run_only_once = False
            while run_only_once == False:
                global system_interrupt
                if system_interrupt:# == True:
                    print("SYSTEM IS NOW INTERRUPTTED AND ALL PROCESS MUST END")
                    break
                global exit_event
                if exit_event.is_set():
                    break
                
                if run_only_once == False:
                    test_dies.probing_dies_through_indexes_provided_by_user(prober_addr_lr, die_map_pwr_level_file_lr, subsite_label_selection_lr, src_meter_addr_lr, left_smu_addr_lr, center_smu_addr_lr, right_smu_addr_lr, voltages_level_mlist, sigGen_addr_lr, amplitude_offset, freq_lr, power_level_mlist, pin_lb_ini, pout_lb_ini, sigAna_addr_lr,  sec_harm_offset_lr, trd_harm_offset_lr, file_name_lr, directory_saving_path_lr, lot_description_lr, wafer_name_lr, pin_offset_lr, pout_offset_lr, enable_reading_current)
                    run_only_once = True
                    
            
            self.start_commandLinkButton.setEnabled(True)
            self.calibration_radioButton.setEnabled(True)
            self.test_radioButton.setEnabled(True)
            
    
    def kill(self):
        # raise SystemExit #the gui goes unresponsive
        # sys.exit(EXIT_STATUS_ERROR)
        # sys.exit(1)
        pass
        
    def stop_button_pressed(self):
        self.thread = start_calibration_worker_function()
        self.thread.stop_system_run()
        global system_interrupt
        system_interrupt = True
        
        global exit_event
        exit_event.set()
        
        global t1
        # self.kill()
        t1.join(0.5)
        if not t1.is_alive():
            print("TerminatingProgram....")
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if app is None:
       app = QtWidgets.QApplication(sys.argv)
    app.setStyle('windowsvista')
    harmonics_system = QtWidgets.QMainWindow()
    ui = Ui_harmonics_system()
    ui.setupUi(harmonics_system)
    harmonics_system.show()
    sys.exit(app.exec_())
