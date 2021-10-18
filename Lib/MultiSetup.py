# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 08:25:07 2021

@author: asligar
"""

import os
import csv
import Lib.Utillities as utils
from pyaedt import Hfss
import sys
class Read_Multi_Setup():
    def __init__(self,file_name,calc_type='',version =  "2021.2"):
        self.version =  version
        jobs = {}
        
        if not os.path.exists(file_name):
            print('ERROR: Multi-Run file does not exist, check path')
            print(file_name)
            sys.exit()
        
        self.calc_type = calc_type
        path, file  = os.path.split(file_name)
        self.path = path
        try:
            with open(file_name) as csvfile:
                header = csvfile.readline()
                header = header.replace(" ","").replace("\n","")
                header = header.split(',')
                
                reader = csv.DictReader(csvfile,fieldnames=tuple(header))
                
                
                for row in reader: #each row will corropsond to a beam id
                    job_dict = {}
                    header_keys = row.keys()
                    #these parametesr are always required
                    job_id = row['Job_ID']
                    job_dict['Project_Name'] = row['Project_Name'].strip()
                    job_dict['Design_Name'] = row['Design_Name'].strip()
                    job_dict['Solution_Name'] = row['Solution_Name'].strip()
                    freq_str = row['Freq'].strip()
                    freq_hz = utils.convert_units(freq_str,newUnits='Hz')
                    job_dict['Freq'] = freq_hz
                    cb_name = row['Codebook_Name'].strip()
                    cb_full_path = self.path + '\\' +cb_name
                    job_dict['Codebook_Name'] = cb_full_path
                    
                    #depending on the type of output requested, not all entries
                    #in the multi-run file are required. It will not read these
                    # if they don't exists, but if they are needed it will results in an error
                    #later
                    
                    #these are only required for PD
                    if calc_type.lower()=='pd':
                        if row.keys() >= {"Averaging_Area", "Evaluation_Surface","PD_Type"}:
                            avg_area_str = row['Averaging_Area'].strip()
                            avg_area_m2 = utils.convert_units(avg_area_str,newUnits='meter^2')
                            job_dict['Averaging_Area'] = avg_area_m2
                            job_dict['Evaluation_Surface'] = row['Evaluation_Surface'].strip()
                            job_dict['PD_Type'] = row['PD_Type'].strip()
                        
                    if calc_type.lower()=='cdf':
                        if row.keys() >= {"CS_Name"}: #these are only required for CDF
                            job_dict['CS_Name'] = row['CS_Name'].strip()
                        else:
                            job_dict['CS_Name'] = 'Global'
                            print('CS_Name is not defined in multi-run select file. Ignore if performing PD, only used for CDF. Using Global\n')
                            
                    if calc_type.lower()=='pd':
                        if 'Averaging_Area' not in row.keys():
                            avg_area_m2 = utils.convert_units('1cm^2',newUnits='meter^2')
                            job_dict['Averaging_Area'] = avg_area_m2
                            print('Averaging_Area is not defined in multi-run select file. Ignore if performing CDF, only used for PD. Using 1cm^2\n')
                        if 'Evaluation_Surface'  not in row.keys():
                            print('Evaluation_Surface is not defined in multi-run select file. Ignore if performing CDF, only used for PD. Correct Input File\n')
                        if 'PD_Type'  not in row.keys():
                            job_dict['PD_Type'] = 'PD_n_plus'
                            print('PD_Type is not defined in multi-run select file. Ignore if performing CDF, only used for PD. Using PD_n_plus\n')
                            
                        
                    jobs[job_id] = job_dict
            path, filename = os.path.split(file_name)
            filename = filename.replace(".csv","")
            self.name = filename
            self.jobs = jobs
        except:
            print("input file format does not contain all needed data, see example")
            sys.exit()
    def validate_multi_setup(self,aedtapp):
        #not yet complete
        #will check all possible setups to make sure everything will run
        for job in self.jobs.keys():
            #check if codebooks exists
            cb_name = self.jobs[job]['Codebook_Name']
            #cb_full_path = self.path + '\\' +cb_name
            if not os.path.exists(cb_name):
                print('Codebook ' + cb_name + " does not exist")
                print('Codebook location should be relative or in same location as multi_run file')
                return False
            
            if self.jobs[job]['Project_Name'] not in aedtapp.project_list:
                print('ERROR: Project ' + selected_project + 'Does Not Exist')
                return False
            else:
                aedtapp = Hfss(self.jobs[job]['Project_Name'],specified_version=self.version)
            if self.jobs[job]['Design_Name'] not in aedtapp.design_list:
                print('ERROR: Design ' + selected_design + 'Does Not Exist')
                return False
            
            
            solution = self.jobs[job]['Solution_Name'].split(':')
            setup_name = solution[0].strip()
            sweep_name = solution[1].strip()
            if setup_name not in aedtapp.get_setups():
                print('Solution Setup ' + setup_name + " does not exist")
                return False
            all_sweeps = aedtapp.get_sweeps(setup_name)
            all_sweeps.append("LastAdaptive")
            if sweep_name not in all_sweeps:
                print('Sweep ' + sweep_name + " does not exist")
                return False 

            #check if eval surfaces exists
            if self.calc_type.lower()=='pd':
                if 'Evaluation_Surface' in self.jobs[job].keys():
                    eval_surf = self.jobs[job]['Evaluation_Surface']
                    oEditor = aedtapp.odesign.SetActiveEditor("3D Modeler")
                    object_name = oEditor.GetMatchedObjectName(eval_surf)
                    if len(object_name)!=1:
                        print('Evaluation Surface ' + eval_surf + " does not exist")
                        return False 
                
            
                if self.jobs[job]['PD_Type'].lower() !='pd_n_plus':
                    if self.jobs[job]['PD_Type'].lower() !='pd_mod_plus':
                        if self.jobs[job]['PD_Type'].lower() !='pd_tot_plus':
                            print("PD type is " + self.jobs[job]['PD_Type'].lower())
                            print('PD_Type must be pd_n_plus, pd_tot_plus or pd_mod_plus')
                            return False 
                    
                    
            # if not aedtapp.osolution.HasFields(self.jobs[job]['Solution_Name'],"nominal"):
            #     print('No Saved Fields for ' +solution)
            #     return False 
            #check if solved frequency exists
   
            
            
            return True