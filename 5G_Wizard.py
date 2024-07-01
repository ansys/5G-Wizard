# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:24:58 2021

@author: asligar
"""
import sys
import os
import Lib.Utillities as utils
from Lib.core_pd import PD
from Lib.core_cdf import CDF
from Lib.Populate_GUI import GUI_Values
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget,QInputDialog, QHBoxLayout, QVBoxLayout, QDialog,QFileDialog,QCheckBox, QCommandLinkButton
from gui_v03 import Ui_Dialog

from Validation import Validate_Reference_Data
#from AEDTLib.HFSS import HFSS
#from AEDTLib.Desktop import Desktop
import pyaedt
from pyaedt import Hfss
from pyaedt import Desktop


version_file = 'aedt_version.txt'
if os.path.exists(version_file):
    with open(version_file) as f:
        version = f.readline()
else:
    version =  None

class MainWindow(QDialog):
    def __init__(self,aedtapp):

        super(MainWindow,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #super().__init__()
        self.gui_params = GUI_Values(aedtapp)
        self.aedtapp = aedtapp
        self.initGUI()
        self.multi_run_enabled=False
        
    def initGUI(self):
        
        #populate intial values

        project_names = self.gui_params.get_project_names()
        active_project = project_names[0]
        design_names = self.gui_params.get_design_names(active_project)
        self.activate_project(active_project,design_names[0])
        
        setup_names = self.gui_params.get_solution_setup_names(design_names[0])
        has_solution = self.gui_params.check_if_solution(setup_names[0])
        if has_solution:
            freqs = self.gui_params.get_freq_values(setup_names[0])
        else:
            freqs = ['No Solved Frequencies']
        
        
        eval_surfaces = self.gui_params.evaluation_surfaces()

        
        #uic.loadUi('gui_v0.ui',self)
        self.setWindowTitle("Ansys 5G Wizard v0.3: AEDT 2022.2")

        self.ui.project_name_input.clear()
        self.ui.project_name_input.addItems(project_names)
        self.ui.design_name_input.clear()
        self.ui.design_name_input.addItems(design_names)
        self.ui.solution_setup_input.clear()
        self.ui.solution_setup_input.addItems(setup_names)
        self.ui.freq_input.clear()
        self.ui.freq_input.addItems(freqs)  
        self.ui.eval_surf_input.clear()
        self.ui.eval_surf_input.addItems(eval_surfaces)  
        
        self.ui.project_name_input.currentTextChanged.connect(self.project_name_changed)
        self.ui.design_name_input.currentTextChanged.connect(self.design_name_changed)
        self.ui.solution_setup_input.currentTextChanged.connect(self.solution_name_changed)
        self.ui.variation_input.currentTextChanged.connect(self.set_design_to_variations)

        self.ui.pd_area_input.currentTextChanged.connect(self.custom_pd_area)
        
        self.ui.pd_renorm_input.currentTextChanged.connect(self.custom_pd_renorm)
        self.ui.cdf_renorm_input.currentTextChanged.connect(self.custom_cdf_renorm)
        
        self.ui.codebook_browse.clicked.connect(self.browse_codebook)
        self.ui.output_browse.clicked.connect(self.browse_output)
        
        #for testing, just setting this so I don't have to do it manually
        self.ui.codebook_text.setText('./example_projects/CodebookExample_Vpol.csv')
        self.ui.output_text_path.setText('./output/')
        
        #self.multi_run_checkbox.stateChanged.connect(lambda:self.multirun_state(self.multi_run_checkbox))
        self.ui.multi_run_checkbox.toggled.connect(lambda:self.multirun_state(self.ui.multi_run_checkbox))
        self.ui.multi_run_browse.clicked.connect(self.browse_multi_run)
        
        self.ui.calculate_pd.clicked.connect(self.run_pd_button)
        self.ui.calculate_cdf.clicked.connect(self.run_cdf_button)
        self.ui.validation_button.clicked.connect(self.run_validation_button)

    def activate_project(self,project_name,desig_name=None):
        self.aedtapp = pyaedt.Hfss(project=project_name,design=desig_name,specified_version=version)
        print('project changed: ' + project_name)
        self.gui_params = GUI_Values(self.aedtapp)
    def project_name_changed(self):
        selected_project = str(self.ui.project_name_input.currentText())
        self.activate_project(selected_project)
        design_names = self.gui_params.get_design_names(selected_project)
        self.ui.design_name_input.blockSignals(True)
        self.ui.design_name_input.clear()
        self.ui.design_name_input.addItems(design_names)
        self.ui.design_name_input.blockSignals(False)
        if design_names!='No Valid Designs':
            self.design_name_changed()
        
    def design_name_changed(self):
        selected_design = str(self.ui.design_name_input.currentText())

        setup_names = self.gui_params.get_solution_setup_names(selected_design)
        self.ui.solution_setup_input.setCurrentText(selected_design)
        self.ui.solution_setup_input.blockSignals(True)
        self.ui.solution_setup_input.clear()
        self.ui.solution_setup_input.addItems(setup_names)   
        self.ui.solution_setup_input.blockSignals(False)
        self.solution_name_changed()
        
        eval_surfaces = self.gui_params.evaluation_surfaces()
        self.ui.eval_surf_input.blockSignals(True)
        self.ui.eval_surf_input.clear()
        self.ui.eval_surf_input.addItems(eval_surfaces)   
        self.ui.eval_surf_input.blockSignals(False)

        cs_names = self.gui_params.get_cs_names()
        self.ui.cs_input.blockSignals(True)
        self.ui.cs_input.clear()
        self.ui.cs_input.addItems(cs_names)   
        self.ui.cs_input.blockSignals(False)
        
            
    def solution_name_changed(self):
        selected_setup = str(self.ui.solution_setup_input.currentText())
        self.update_available_variations()
        if selected_setup[0]!='No Valid Setups':
            has_solution = self.gui_params.check_if_solution(selected_setup)
            
            if has_solution:
                freqs = self.gui_params.get_freq_values(selected_setup)
            else:
                freqs = ['No Solved Frequencies']
            self.ui.freq_input.blockSignals(True)
            self.ui.freq_input.clear()
            self.ui.freq_input.addItems(freqs)   
            self.ui.freq_input.blockSignals(False)
        
    def update_available_variations(self):
        
        selected_setup = str(self.ui.solution_setup_input.currentText())
        if selected_setup!='No Valid Setups':
            list_of_variations, self.dict_of_variations = self.gui_params.available_variations(selected_setup)
            if len(list_of_variations)==1: #if only 1 variation no need to list anything other than nominal
                list_of_variations = ['Nominal']
        else:
            list_of_variations = ['Nominal']
        self.ui.variation_input.blockSignals(True)
        self.ui.variation_input.clear()
        self.ui.variation_input.addItems(list_of_variations)   
        self.ui.variation_input.blockSignals(False)
        self.ui.pd_area_input.setCurrentText('Nominal')

    def set_design_to_variations(self):
        selected_variation = str(self.ui.variation_input.currentText())
        selected_variation_key = int(selected_variation.split('=')[0]) #selected variation always has a key at the start of the string to tie it back to the original variation
        if not self.dict_of_variations:
            self.update_available_variations()
        p1 = ["NAME:AllTabs"]
        p1_global = ["NAME:AllTabs"]
        p2 = [ "NAME:LocalVariableTab",["NAME:PropServers", "LocalVariables"]]
        p2_global = [ "NAME:ProjectVariableTab",["NAME:PropServers", "ProjectVariables"]]
        vals_to_change = ["NAME:ChangedProps"]
        vals_to_change_global = ["NAME:ChangedProps"]
        variation_to_set = self.dict_of_variations[selected_variation_key]
        for var_name in variation_to_set.keys():
            if '$' in var_name: #global variables
                vals_to_change_global.append(["NAME:" + var_name, "Value:=", variation_to_set[var_name]])
            else:
                vals_to_change.append(["NAME:" + var_name, "Value:=", variation_to_set[var_name]])
        p2.append(vals_to_change)
        p1.append(p2)
        self.aedtapp.odesign.ChangeProperty(p1)
        if len(vals_to_change_global)>1:      
            p2_global.append(vals_to_change)
            p1_global.append(p2_global)
            self.aedtapp.oproject.ChangeProperty(p1_global)

    def custom_pd_area(self):
        if str(self.ui.pd_area_input.currentText())=='Custom...':
            #all_current_values = self.pd_area_input.allItems()
            #all_current_values = all_current_values[:-1] #remove custom from end of list
            
            units, done = QInputDialog.getText(self, 'PD Averaging Area', 'Enter Area:')

            val, units = self.correct_units(units)
            value_and_units = str(val) + units

            self.ui.pd_area_input.blockSignals(True)
            self.ui.pd_area_input.addItem(value_and_units)
            self.ui.pd_area_input.blockSignals(False)
            self.ui.pd_area_input.setCurrentText(value_and_units)

    def custom_pd_renorm(self):
        if str(self.ui.pd_renorm_input.currentText())=='Custom...':
            
            val_str, done = QInputDialog.getText(self, 'PD Renormalization', 'Enter Value(s):')
            val_str = val_str.lower()
            val_str = val_str.replace(" ","")
            val_str = val_str.rstrip('abcdefghijklmnopqrstuvwxyz') #remove any units that may have been entered
            if ',' not in val_str:
                val_str = val_str + 'W'
            self.ui.pd_renorm_input.blockSignals(True)
            self.ui.pd_renorm_input.addItem(val_str)
            self.ui.pd_renorm_input.blockSignals(False)
            self.ui.pd_renorm_input.setCurrentText(val_str)

    def custom_cdf_renorm(self):
        if str(self.ui.cdf_renorm_input.currentText())=='Custom...':
            
            val_str, done = QInputDialog.getText(self, 'CDF Renormalization', 'Enter Value:')
            val_str = val_str.lower()
            val_str = val_str.replace(" ","")
            val_str = val_str.rstrip('abcdefghijklmnopqrstuvwxyz') #remove any units that may have been entered
            self.ui.cdf_renorm_input.blockSignals(True)
            self.ui.cdf_renorm_input.addItem(val_str)
            self.ui.cdf_renorm_input.blockSignals(False)
            self.ui.cdf_renorm_input.setCurrentText(val_str)



    def correct_units(self,unit_str):
        unit_str= unit_str.replace(" ","")
        unit_str = unit_str.replace("^","")
        if len(unit_str)==0:
            value = 1
            units = 'cm^2'
        try: #only a number entered, no units
            value = abs(float(unit_str))
            units = 'cm^2'
        except:
            if unit_str.isalpha(): #only a string, no value entered
                value = 1
                units = 'cm^2'
            else: #alpha numeric value entered, remove units
                if unit_str[-1] =='2': #remove 2 value form units so easier to split
                    unit_str =unit_str.replace('2','')
                    unit_str = unit_str.lower()
                    value = unit_str.rstrip('abcdefghijklmnopqrstuvwxyz')
                    units = unit_str[len(value):] + '^2'
                    value = float(value)
                else: #units were incorrectly enetered like cm instead of cm^2 of cm2, add square units back
                    value = unit_str.rstrip('abcdefghijklmnopqrstuvwxyz')
                    units = unit_str[len(value):] + '^2'
                    value = float(value)
        return value, units

    

    def browse_codebook(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.csv);;All Files (*)", options=options)
        self.ui.codebook_text.setText(fileName)
        
    def browse_output(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder', options=options)
        self.ui.output_text_path.setText(folderpath)
            
    def multirun_state(self,state):
        if state.isChecked():
            self.multi_run_enabled = True
            self.ui.multirun_group.setEnabled(True)
            self.ui.codebook_group.setEnabled(False)
            self.ui.pd_setup_group.setEnabled(False)
            self.ui.cdf_setup_group.setEnabled(False)
            self.ui.solution_select_group.setEnabled(False)
        else:
            self.multi_run_enabled = False
            self.ui.multirun_group.setEnabled(False)
            self.ui.codebook_group.setEnabled(True)
            self.ui.pd_setup_group.setEnabled(True)
            self.ui.cdf_setup_group.setEnabled(True)
            self.ui.solution_select_group.setEnabled(True)
            
    def browse_multi_run(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.csv);;All Files (*)", options=options)
        self.ui.multi_run_text.setText(fileName)

    def validate_gui(self):
        
        #need to add check for no project open
        if self.multi_run_enabled:
            selected_multirun = str(self.ui.multi_run_text.text())
            if selected_multirun =="":
                return False
        else:
            selected_project = str(self.ui.project_name_input.currentText())
            selected_design = str(self.ui.design_name_input.currentText())
            selected_setup = str(self.ui.solution_setup_input.currentText())
            try:
                selected_freq = float(self.ui.freq_input.currentText())
            except:
                return False
            
            codebook_path = str(self.ui.codebook_text.text())
            output_path = str(self.ui.output_text_path.text())
            if (selected_project =="" or selected_design ==""  or selected_setup == "" or selected_freq=="" or codebook_path=="" or output_path=="" ):
                return False

            if selected_design=='No Valid Designs':
                return False
            if selected_setup=='No Valid Setups':
                return False
            if selected_freq=='No Solved Frequencies':
                return False


        return True

    def run_pd_button(self):
        print("running")


        if not self.validate_gui():
            print("selections are not valid")
            return

        output_path = str(self.ui.output_text_path.text())
        output_path = os.path.join(output_path, '')

        wizard = PD(self.aedtapp,output_path=output_path)
        wizard.version = version
        if self.multi_run_enabled:
            wizard.multirun_state = True
            selected_multirun = str(self.ui.multi_run_text.text())
            wizard.multi_setup_file_path = selected_multirun

        else:
            wizard.multirun_state = False
            selected_project = str(self.ui.project_name_input.currentText())
            selected_design = str(self.ui.design_name_input.currentText())
            selected_setup = str(self.ui.solution_setup_input.currentText())
            selected_freq = float(self.ui.freq_input.currentText())
            
            codebook_path = str(self.ui.codebook_text.text())
            

            if self.ui.ignore_beampair.isChecked():
                ignore_beampair = True
            else:
                ignore_beampair= False
            
            selected_eval_surf = str(self.ui.eval_surf_input.currentText())
            selected_area = str(self.ui.pd_area_input.currentText())
            selected_pd_type = str(self.ui.pd_type_input.currentText())
            selected_pd_renorm = str(self.ui.pd_renorm_input.currentText())
            selected_cdf_renorm= str(self.ui.cdf_renorm_input.currentText())

            pd_renorm=False
            renorm_values = 1
            if selected_pd_renorm != "None":
                pd_renorm = True
                renorm_values = selected_pd_renorm
            wizard.ignore_beampair = ignore_beampair
            wizard.freq = selected_freq
            wizard.project_name = selected_project
            wizard.design_name = selected_design
            wizard.surface_name= selected_eval_surf

            wizard.averaging_area = utils.convert_units(selected_area,newUnits= 'meter^2') #area should be in meters^2
            wizard.setup_name = selected_setup
            wizard.path_to_codebook = codebook_path
            wizard.pd_type = selected_pd_type

            wizard.renormalize = pd_renorm
            wizard.renorm_values = renorm_values
        
        wizard.run_pd()

    def run_cdf_button(self):
        print("running")

        if not self.validate_gui():
            print("selections are not valid")
            return

        output_path = str(self.ui.output_text_path.text())
        output_path = os.path.join(output_path, '')
        wizard = CDF(self.aedtapp,output_path=output_path)
        wizard.version = version
        if self.multi_run_enabled:
            wizard.multirun_state = True
            selected_multirun = str(self.ui.multi_run_text.text())
            wizard.multi_setup_file_path = selected_multirun

        else:
            wizard.multirun_state = False
            selected_project = str(self.ui.project_name_input.currentText())
            selected_design = str(self.ui.design_name_input.currentText())
            selected_setup = str(self.ui.solution_setup_input.currentText())
            selected_freq = float(self.ui.freq_input.currentText())
            selected_cs = str(self.ui.cs_input.currentText())
            codebook_path = str(self.ui.codebook_text.text())

            selected_cdf_renorm = self.ui.cdf_renorm_input.currentText()
            selected_db_of_lin = str(self.ui.cdf_dblin_input.currentText())

            cdf_renorm=False
            renorm_db=True
            renorm_value = 1
            if selected_cdf_renorm != "None":
                cdf_renorm = True
                renorm_value = float(selected_cdf_renorm)
                if selected_db_of_lin=='Linear':
                    renorm_db = False


            wizard.freq = selected_freq
            wizard.project_name = selected_project
            wizard.design_name = selected_design
            wizard.setup_name = selected_setup
            wizard.path_to_codebook = codebook_path
            wizard.cs_name = selected_cs



            wizard.renormalize = selected_cdf_renorm
            wizard. renormalize_dB = renorm_db
            wizard.renorm_value = renorm_value

        
        wizard.run_cdf()
        
    def run_validation_button(self):
        validation = Validate_Reference_Data()
        validation_results = validation.run()
if __name__ == '__main__':
    # with Desktop( specified_version=version,new_desktop_session =False,close_on_exit =False) as d:
    #     project_list = d.project_list()
    #     design_list = d.design_list(project_list[0])
    #     # aedtapp = Hfss(project_list[0],design_list[0],specified_version=version)
    aedtapp = pyaedt.Desktop(version=version, non_graphical=False, new_desktop=False)
    app = QApplication(sys.argv)
    myApp = MainWindow(aedtapp)
    myApp.show()
    
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('closing')
        
