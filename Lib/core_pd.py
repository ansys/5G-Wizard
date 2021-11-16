# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 13:56:36 2021

@author: asligar
"""
# ------------------------------------------------------------------------------
# Standard Python Module Imports
import os
import sys
import json
import numpy as np
from Lib.Codebook import Codebook_Utils
from Lib.NearField_Setup import NearField_Utils
from Lib.FarField_Setup import FarField_Utils
from Lib.NearFieldsProcessing import Load_NF_Fields
from Lib.FarFieldsProcessing import Load_FF_Fields
from Lib.FarFieldsProcessing import envelope_pattern_all_jobs
from Lib.Reporter import Report_Module
from Lib.MultiSetup import Read_Multi_Setup
from Lib.CreateReports_in_AEDT import AEDT_CreateReports
from Lib.Html_Report import Html_Writer
import Lib.Utillities as utils

from pyaedt import Hfss
from pyaedt import Desktop
#from AEDTLib.HFSS import HFSS
#from AEDTLib.Desktop import Desktop
print(sys.path)


oDesktop = None

###########
# TODO
# multi thread averaging calculation
# support codebook with single beam id or no codebook (case of wifi6 with only 1 port)
# gui
# format output
###########

class PD():
    def __init__(self,aedtapp,output_path = './output/'):
        print('Calculating PD...')
        self.aedtapp = aedtapp
        self.version = '2021.2'
        self.multirun_state = False
        self.multi_setup_file_path = ''
        self.freq = 28e9
        
        self.project_name = ''
        self.design_name = ''
        self.surface_name= ''
        self.averaging_area = utils.convert_units(1,'cm^2', 'meter^2') #area should be in meters^2
        self.setup_name = ""
        self.path_to_codebook = ''
        self.pd_type = 'PD_n_plus'
        self.renormalize = False
        self.renorm_values = 1

        
        current_date_and_time =utils.round_time()
        current_date_and_time_string = str(current_date_and_time).replace(':','').replace(' ','_')
        self.summary_file_name =  'Summary_' + current_date_and_time_string + '.json'
        
        self.base_output_path = output_path + current_date_and_time_string + '/PD/'
        self.output_path = self.base_output_path

    def get_desktop_settings(self):
        self.current_autosave_state = self.aedtapp.odesktop.GetAutoSaveEnabled()
        self.current_updatereports_state = self.aedtapp.odesktop.GetRegistryInt('Desktop/Settings/ProjectOptions/HFSS/UpdateReportsDynamicallyOnEdits') 
    def disable_desktop_settings(self):
        self.aedtapp.odesktop.EnableAutoSave(False)
        self.aedtapp.odesktop.SetRegistryInt('Desktop/Settings/ProjectOptions/HFSS/UpdateReportsDynamicallyOnEdits', 0)
        
    def restore_desktop_settings(self):
        self.aedtapp.odesktop.EnableAutoSave(self.current_autosave_state)
        self.aedtapp.odesktop.SetRegistryInt('Desktop/Settings/ProjectOptions/HFSS/UpdateReportsDynamicallyOnEdits', 
                                        self.current_updatereports_state)
    def run_pd(self,projectname = '5G_28GHz_AntennaModule'):

        
        #get current state of autosave, will restore after script completes
        self.get_desktop_settings()
        self.disable_desktop_settings()
        
        
        if self.multirun_state:
            all_jobs = Read_Multi_Setup(self.multi_setup_file_path,calc_type='PD',version =  self.version)
            #validation of setup is not complete
            if not all_jobs.is_valid:
                print("Multi-run setup file is not valid")
                return False
            if not all_jobs.validate_multi_setup(self.aedtapp):
                print("Multi-run setup file is not valid")
                return False

            jobs = all_jobs.jobs
        else:
            #select parameters
            job_dict = {}
            
            job_dict['Project_Name'] = self.project_name
            job_dict['Design_Name'] = self.design_name
            job_dict['Solution_Name'] = self.setup_name
            job_dict['Averaging_Area'] = self.averaging_area
            job_dict['Codebook_Name'] = self.path_to_codebook
            job_dict['Evaluation_Surface'] = self.surface_name
            job_dict['Freq'] = self.freq
            job_dict['PD_Type'] = self.pd_type
            #only one job
            jobs = {0:job_dict}
    
        job_ids = list(jobs.keys())

            
        pd_max_dict_all_jobs = {}
        for job in jobs.keys():
            print('Runnning JobID ' + str(job))
            
            #output_path = self.base_output_path +jobs[job]['Project_Name'] + '\\'+ jobs[job_ids[0]]['Design_Name'] + '\\'
            output_path = self.base_output_path  + 'JobID_' + str(job) + '/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                
            job_summary_name = 'job_summary.json'
            job_sum_path_name = output_path + job_summary_name   
            
            variation_dict = self.aedtapp.available_variations.nominal_w_values_dict
            output_dict = jobs[job]
            output_dict['Variation'] = variation_dict
            
            utils.write_dictionary_to_json(path=job_sum_path_name,dict_to_write=output_dict)
            
            ant_param_dict  = {}
            
            update_fields = True
            
            #read parameters from job dictionary
            #allow PD to be entered as'pd_n+' or pd_n_plus
            pd_type = jobs[job]['PD_Type']
            pd_type_map = {'pd_n+':'pd_n_plus','pd_tot+':'pd_tot_plus','pd_mod+':'pd_mod_plus'}
            if pd_type.lower() in ['pd_n+','pd_tot+','pd_mod+']:
                pd_type = pd_type_map[pd_type.lower()]
            
            selected_project = jobs[job]['Project_Name']
            selected_design = jobs[job]['Design_Name']
            if selected_project not in self.aedtapp.project_list:
                print('ERROR: Project ' + selected_project + 'Does Not Exist')
                return False
            if selected_design not in self.aedtapp.design_list:
                print('ERROR: Design ' + selected_design + 'Does Not Exist')
                return False
            self.aedtapp = Hfss(selected_project,specified_version=self.version)
            self.aedtapp.set_active_design(selected_design)
            print('Active Design: ' + selected_design)
            self.solution_type = self.aedtapp.solution_type
            
            freq = jobs[job]['Freq']
            
            path_to_codebook = jobs[job]['Codebook_Name']
            
            setup_name = jobs[job]['Solution_Name']
            setup_name_only = setup_name.split(':')[0]
            sweep_name_only = setup_name.split(':')[1]
            
            if setup_name_only not in self.aedtapp.get_setups():
                print("ERROR: Setup " + setup_name + " does not exist in design")
                return False
            
            sweeps = self.aedtapp.get_sweeps(setup_name_only)
            sweeps.append("LastAdaptive")
            full_setup_names = []

            if sweep_name_only not in sweeps:
                print("ERROR: Setup " + setup_name + ":" + sweep_name_only +  " does not exist in design")
                return False
            
            surface_name = jobs[job]['Evaluation_Surface']
            averaging_area = jobs[job]['Averaging_Area']
            
            
            wl = 3e8/freq
        
            #import codebook
            codebook = Codebook_Utils(self.aedtapp,path_to_codebook)
            codebook.codebook_import()
            beam_ids = codebook.beam_ids
            #create near field setup
            
            nearfield_setup = NearField_Utils(self.aedtapp)
            
            cs_name = nearfield_setup.create_cs_sheet_center(surface_name)
            if not cs_name:
                return False
            #sample space shoudl be 1mm or lambda/10, whichever is less
            lambda_by_ten = wl/10 #should be wl/10
            if lambda_by_ten>1e-3:
                grid_size = 1e-3
            else:
                grid_size  = lambda_by_ten
            
            #only for testing, 
            #grid_size=1e-3
            
        
            #use_true_size will force teh grid to align to user defined rectangle
            #this can happen becuase of length/grid size does not equal integer value
            #use_true_size=False will strictly follow the grid size defined and may extend
            #slightly beyond the user defined rectangle, but never shrink it

            nf_setup_name = nearfield_setup.generate_nearfield_setup("nf_setup_name",
                                                                         cs_name,
                                                                         grid_size = grid_size,
                                                                         use_true_size=False)
            if not nf_setup_name:
                print('ERROR: Unable to insert near field setup, make sure design has an ABC/PML boundary')
                return False
            
            
            #export fields, save to results directory with some sub folders
            save_path = (self.aedtapp.project_path + '\\'+self.aedtapp.project_name +  '.aedtresults\\' + 
                         self.aedtapp.design_name  + '.results\\'+ surface_name + '.nfd\\')
            
            #get edit sources current values, we will reset this after we extract the 
            #fields for each port excited by itself. Edit source in HFSS or not needed
            #for any averaging, but are useful to view beam patterns and resutls in HFSS
            current_edit_sources_status = codebook.edit_sources_array
            
            #only export port names that exist in the codebook, helpful in cases where
            #multiple modules exist in the design but are not being used for evaluation
            port_names_to_export = codebook.port_names_in_codebook

            
            #exctract antenna parameters (ie peak gain, radiated power...etc)
            
            farfield_setup = FarField_Utils(self.aedtapp)
            farfield_setup.insert_infinite_sphere()
            
    
            for beam_id in codebook.unique_beams:
                print('Calculating Far Field Quantities for Beam ' + str(beam_id))
                codebook.add_or_edit_variable('beamID',beam_id)
                ant_param_dict[beam_id] = farfield_setup.get_antenna_parameters(setup_name,
                                                                       farfield_setup.name,
                                                                       freq)
                if not ant_param_dict[beam_id]:
                    print('ERROR: Unable to get solution data, make sure solution exists')
                    return False
            #rearragne the antenna parameters
            #right now they are in format data[job][antenna_params][beam_id]
            #just so it is easy to sort the data later I am unnesting them
            #pd_max_dict['AntennaParameters'] = ant_param_dict #but still leaving original, will just ignore when plotting
            peak_directivity = []
            peak_realized_gain = []
            peak_gain = []
            radiated_power = []
            accepted_power = []
            incident_power = []
            for b in codebook.unique_beams:
                peak_directivity.append(ant_param_dict[b]['PeakDirectivity'])
                peak_gain.append(ant_param_dict[b]['PeakGain'])
                peak_realized_gain.append(ant_param_dict[b]['PeakRealizedGain'])
                radiated_power.append(ant_param_dict[b]['RadiatedPower'])
                accepted_power.append(ant_param_dict[b]['AcceptedPower'])
                incident_power.append(ant_param_dict[b]['IncidentPower']) 
            
            
            #extract fields for each port excited individually
            nfd_files_dict = nearfield_setup.export_all_nfd(nf_setup_name,
                                           ports = port_names_to_export,
                                           freq=freq,
                                           setup_name = setup_name,
                                           export_path=save_path,
                                           overwrite=update_fields)
            
            #set edit sources back to values that represent codebook, this allows fields to be seen in AEDT
            codebook.edit_sources(current_edit_sources_status)
            codebook.add_or_edit_variable('beamID',beam_ids[0])
            
    
            
            
            #Load Fields from nfd files
            #this just reads the data from file into memory
            fields_data = Load_NF_Fields(nfd_files_dict,
                                      nearfield_setup.actual_length,
                                      nearfield_setup.actual_width,
                                      nearfield_setup.length_n,
                                      nearfield_setup.width_n)
            
            
            

            
            #there are two ways to renormalize, one from the entry specified
            #by the user in the GUI or through a data column in the codebook
            #the codebook will always override any other user settings
            override_renorm_from_codebook = False


            overriding_renorm_values = []
            for each in codebook.unique_beams:
                if 'Prad_Renorm' in codebook.input_vector[each].keys():
                    overriding_renorm_values.append(codebook.input_vector[each]['Prad_Renorm'])
                    override_renorm_from_codebook = True
                    self.renormalize = True

            if override_renorm_from_codebook:
                print('Renormlization values detected in codebook, using those values')
                self.renorm_values = overriding_renorm_values
                    
                    
            fields_data.renormalize = self.renormalize
            #update fields_data with radiated power and list of renormalized powers
            if self.renormalize:
                fields_data.prad= radiated_power #this is the radiated power for all original beams
                fields_data.renorm_values = self.renorm_values


            #because PD is going to be equivlant for beam pairs
            #for example Beam1 with Beam5 as as pair is teh same as Beam 5 with Beam 1 as a pair
            fields_data.unique_beams = codebook.unique_beams
            #recombine fields based on steering vector (codebook.input_vector)
            
            results = fields_data.combine_fields(codebook.input_vector,
                                                 reshape=[nearfield_setup.width_n,nearfield_setup.length_n])
            
            #surface normal needed for PD calculations
            surface_normal = nearfield_setup.norm_unitvec
            
            #from the fields calculate different types of PD as defined in spec
            if pd_type.lower()=='pd_n_plus':
                pd_local = fields_data.get_PD_n_plus_local(results,surface_normal)
            if pd_type.lower()=='pd_tot_plus':
                pd_local.lower()== fields_data.get_PD_tot_plus_local(results,surface_normal)
            if pd_type.lower()=='pd_mod_plus':
                pd_local = fields_data.get_PD_mod_plus_local(results,surface_normal)
    
            
            #or calculate them all at once, which is just a wrapped up call to each of the previous functions
            #pd_all_types_local = fields_data.get_PD_all_types(results,surface_normal)
            
            
            #averaging of poynting vector using technique described in spec
            #if we watned pd_tot+ or mod+ we would call this with the approriate data input
    
            pd_avg = fields_data.average_pd(pd_local,averaging_area,grid_size)
            
            #print('Averaging Calculation Time: ' + str(np.round(time_to_average,2)))

            #write out raw data to hd5f format as defined in spec
            #there are two seperate calls, on does all the original data, this is stored
            #in a nested dictionary, so it was just easiest to write a seperate functino for this
            output_rawdata_dict = utils.write_out_fields_2levels(name = surface_name,
                                                         output_path = output_path,
                                                         data = results)
            #write out averaged data, this is not a nested dictionary, 
            # so slightly different way to write out data
            output_avgdata_dict = utils.write_out_fields_1level(name = surface_name,
                                                         output_path = output_path,
                                                         data = pd_avg,
                                                         qty=pd_type)
            if self.renormalize:
                print("INFO: Radiated power has been renormalized, exported hd5f data will only reflect this renormlization in P, not E or H")
            
            #get a list of module name if defined in the codebook, just used for
            #labeling teh data later
            module_name_list = []
            for each in codebook.unique_beams:
                if 'Module_Name' in codebook.input_vector[each].keys():
                    module_name_list.append(codebook.input_vector[each]['Module_Name'])
                    
                    
            #max value after averaging for all beam ids
            pd_max = fields_data.get_max_for_each_beam(pd_avg,label=pd_type)
            pd_max_dict = {'EvalSurface':surface_name,
                           'Freq':freq,
                           'Averaging_Area':jobs[job]['Averaging_Area'],
                           'PD_Max':pd_max,
                           'PD_Type':pd_type,
                           'Paths_To_Raw_Data':output_rawdata_dict,
                           'Paths_To_Avg_Data':output_avgdata_dict}
            
            if len(module_name_list)==len(pd_max):
                pd_max_dict['Module_Name'] = module_name_list
            
            pd_max_dict['Renormalized PD'] = fields_data.renormalize
            if fields_data.renormalize:
                pd_max_dict['RadiatedPower'] = fields_data.renorm_values
                pd_max_dict['RadiatedPower_NoRenorm'] = radiated_power  #adding this for ease of plotting (will only show when renormalized)
            else:
                pd_max_dict['RadiatedPower'] = radiated_power

            pd_max_dict['PeakDirectivity'] = peak_directivity 
            pd_max_dict['PeakRealizedGain'] = peak_realized_gain 
            pd_max_dict['PeakGain'] = peak_gain 
            pd_max_dict['AcceptedPower'] = accepted_power 
            pd_max_dict['IncidentPower'] = incident_power

            pd_max_dict['JobID']  = job
            
            pd_max_local = fields_data.get_max_for_each_beam(pd_local,label='Local') #label is just to display in console
            
            csv_name = output_path + 'JobID_' + str(job) + '.csv'
            utils.write_csv(pd_max_dict,csv_name)
<<<<<<< HEAD
=======
            csv_name_sorted = output_path + 'JobID_' + str(job) + '_SortedByPD.csv'
            utils.write_csv(pd_max_dict,csv_name_sorted,sort_by_pd=True)
>>>>>>> 89bf2e89954d81e549986bc19e13ed722cb8ab62
            ##################################################################
            #Visualizing results
            #################################################################
            
            report_name_base_str = surface_name + '_' + str(freq*1e-9) + 'GHz'
            
            #job_id is passed in becuase it is used to determine relativ path
            reports = Report_Module(self.aedtapp,self.base_output_path,job_id = job)
            show_plots=False #too many plots are being created for some codebooks. Will not display them for now
            close_reports = True
            if self.multirun_state:
                show_plots = False
                close_reports=True
            #plotting peak values versus beam id
            # save_name = 'max_'+ pd_type + '_bar_' + report_name_base_str
            # full_path = reports.max_vs_beam_bar(pd_max,save_name=save_name,save_plot=True,show_plot = show_plots)
            


            if close_reports:
                reports.close_all_reports()
            save_name = 'max_'+ pd_type + '_line_' + report_name_base_str
            reports.max_vs_beam_line(pd_max,save_name=save_name,save_plot=True,show_plot = show_plots)
            if close_reports:
                reports.close_all_reports()
            
            
            #plot the averaged PD for every beamID
            for beam in pd_avg.keys():
                pd = pd_avg[beam]
                plot_title = 'sPD-avg, ' +pd_type + ': Beam ID ' + str(beam) + ', Avg. Area:' + str(averaging_area*1e4) + 'cm^2'
                save_name = 'avg_' + pd_type + '_beamid_' + str(beam) + '_' + report_name_base_str
                reports.plot_pd(pd,fields_data.pos,title=plot_title, save_plot=True,save_name=save_name)
            
            if close_reports:
                reports.close_all_reports()
            
            #plot the local PD for every beamID
            # for beam in pd_local.keys():
            #     pd = pd_local[beam]
            #     plot_title = 'Local Power Density: Beam ID ' + str(beam)
            #     save_name = 'local_' + pd_type + '_beamid_' + str(beam) + '_' +report_name_base_str
            #     reports.plot_pd(pd,
            #                     fields_data.pos,
            #                     title=plot_title, 
            #                     save_plot=True,
            #                     save_name=save_name)
            # if self.multirun_state:
            #     reports.close_all_reports()
            # save_name = 'max_pd_local_line_' + report_name_base_str
            # reports.max_vs_beam_line(pd_max_local,
            #                             save_name=save_name,
            #                             save_plot=True,
            #                             title='PD Max Local',
<<<<<<< HEAD
            #                             show_plot = show_plots)      
            
            
            reports.field_plot_3d_pyvista(fields_data,
                                        save_name ="Interactive_PD_Pattern",
                                        save_plot=True,
                                        show_plot=True,
                                        output_path = '',
                                        show_cad=True)
=======
            #                             show_plot = show_plots)       
>>>>>>> 89bf2e89954d81e549986bc19e13ed722cb8ab62
            if close_reports:
                reports.close_all_reports()
            
            #write all image locations to dictionary
            pd_max_dict['Paths_To_Images'] = reports.all_figure_paths
            
            #savwe all data to single dict, will be written to json later
            pd_max_dict_all_jobs[job] = pd_max_dict
    

            
        # save_name = 'PD_Summary_Table'
        # reports.pd_table(pd_max_dict_all_jobs,
        #                  save_plot=True,
        #                  save_name=save_name,
        #                  override_path =self.base_output_path )
        
        if close_reports:
            reports.close_all_reports()
        
        
        utils.write_dictionary_to_json(path=self.base_output_path+self.summary_file_name,
                                       dict_to_write=pd_max_dict_all_jobs)
        
        
        self.restore_desktop_settings()
        print('Done')
        
        self.pd_max_dict_all_jobs = pd_max_dict_all_jobs
        
        for job_id_temp in self.pd_max_dict_all_jobs.keys():
            html_out = Html_Writer(self.base_output_path,'Summary_Job_' +str(job_id_temp))
            html_out.generate_html_pd(pd_max_dict_all_jobs[job_id_temp])
        
        return True
        