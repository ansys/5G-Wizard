# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:47:02 2021

@author: asligar
"""

from Lib.core_pd import PD
from Lib.core_cdf import CDF
import Lib.Utillities as utils
import os
import pyaedt 
from pyaedt import Hfss
from pyaedt import Desktop
from Validation import Validate_Reference_Data

version_file = 'aedt_version.txt'
if os.path.exists(version_file):
    with open(version_file) as f:
        version = f.readline()
else:
    version =  None

def run_pd(aedtapp,selected_project,selected_design):
    multi_run_enabled = False
    wizard = PD(aedtapp)
    wizard.version = version
    if multi_run_enabled:
        wizard.multirun_state = multi_run_enabled
        wizard.multi_setup_file_path = './example_projects/Multi_Setup_Run_PD.csv'

    else:
        wizard.multirun_state = multi_run_enabled
        selected_project = selected_project
        selected_design = selected_design
        selected_setup = "Setup1:LastAdaptive"
        selected_freq = 28e9
        #codebook_path = './example_projects/CodebookExample_Hpol_Renormalize.csv'
        codebook_path = './example_projects/CodebookExample_Hpol.csv'

        selected_eval_surf = '50mm_Surface'
        selected_area = '1cm^2' #area in cm^2 as a string
        selected_pd_type = 'PD_n_plus'
        renormalize = False
        renorm_values= [1,.5,1,.5,.1]
    
        wizard.freq = selected_freq
        wizard.project_name = selected_project
        wizard.design_name = selected_design
        wizard.surface_name= selected_eval_surf
        wizard.averaging_area = utils.convert_units(selected_area,newUnits= 'meter^2') #area should be in meters^2
        wizard.setup_name = selected_setup
        wizard.path_to_codebook = codebook_path
        wizard.pd_type = selected_pd_type
        wizard.renormalize = renormalize
        wizard.renorm_values = renorm_values
    wizard.run_pd()
    return wizard
def run_cdf(aedtapp,selected_project,selected_design):
    multi_run_enabled = False
    wizard = CDF(aedtapp)
    wizard.version = version
    if multi_run_enabled:
        wizard.multirun_state = multi_run_enabled
        wizard.multi_setup_file_path = './example_projects/Multi_Setup_Run_CDF.csv'

    else:
        wizard.multirun_state = multi_run_enabled
        selected_project = selected_project
        selected_design = selected_design
        selected_setup = "Setup1:LastAdaptive"
        selected_freq = 28e9
        renormalize = False
        renormalize_dB = True
        renorm_value= 10
        
        codebook_path = './example_projects/CodebookExample_Hpol.csv'

        cs_name = 'Global'
        
    
        wizard.freq = selected_freq
        wizard.project_name = selected_project
        wizard.design_name = selected_design

        wizard.setup_name = selected_setup
        wizard.path_to_codebook = codebook_path
        wizard.cs_name = cs_name
        wizard.renormalize = renormalize
        wizard. renormalize_dB = renormalize_dB
        wizard.renorm_value = renorm_value
        
    wizard.run_cdf()
    return wizard

def run_validate():
    validation = Validate_Reference_Data()
    validation_results = validation.run()

if __name__ == '__main__':
    selected_project = '5G_28GHz_AntennaModule'
    selected_design = '4x1_array1'
    #with Desktop(specified_version=version,new_desktop_session =False,close_on_exit =False):
    with Hfss(selected_project,selected_design,non_graphical=False, new_desktop_session=False,specified_version=version) as aedtapp:

        #wizard_pd = run_pd(aedtapp,selected_project,selected_design)
        wizard_cdf = run_cdf(aedtapp,selected_project,selected_design)


    #run_validate()
    
    

    
    
