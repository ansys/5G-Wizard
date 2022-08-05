# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 14:33:30 2021

@author: asligar
"""

import os
import json
import glob
import jinja2
import numpy as np
import shutil


class Html_Writer():
    def __init__(self,base_path,name='Job_ID0'):
        script_path = os.path.realpath(__file__)
        self.script_path = script_path.replace('Lib\Html_Report.py','')
        self.base_path = base_path
        self.name = name
        #move stylesheet to correct location
        if not os.path.exists(self.base_path + 'static/'):
            os.makedirs(self.base_path + 'static/')
        
        files_in_static = glob.glob('./static/*.*')
        for each in files_in_static:
            shutil.copy2(each, self.base_path + 'static\\')
        
        
    # def get_jobs(self):
    #     job_folders = [name for name in os.listdir(self.base_path) if os.path.isdir(self.base_path + name)]
    #     job_ids = [name.split('_')[1] for name in os.listdir(test_path) if os.path.isdir(test_path + name)]
    #     return job_folders

    def get_design_info(self,job_id):

        job_folder_name = 'JobID_' + str(job_id)
        json_for_job = self.base_path + job_folder_name + '/job_summary.json'
        
        does_file_exist= os.path.isfile(json_for_job)
        if does_file_exist:
            f = open(json_for_job,)
            data = json.load(f)
        else:
            data = {}

        return data
    # def get_json_file_all_jobs(self):
    #     json_for_all_jobs = glob.glob(self.base_path  + '*.json',recursive=False)
    #     return json_for_all_jobs
    
    def generate_html_pd(self,data):
        
        
        title = 'Power Density Summary Report: '
        
        design_info_dict = self.get_design_info(data['JobID'])
        title = 'Power Density Summary Report: ' + design_info_dict['Design_Name']
        beam_ids =data['BeamID']
        if 'Module_Name' in data.keys():
            headings_pd_summary = ('Project_Name','Design_Name','Solution_Name','Codebook_Name','PD_Type','EvalSurface','Averaging_Area','Freq','Renormalized PD','Module_Name')
        else:
            headings_pd_summary = ('Project_Name','Design_Name','Solution_Name','Codebook_Name','PD_Type','EvalSurface','Averaging_Area','Freq','Renormalized PD')
            
        data_pd_summary = []
        for heading in headings_pd_summary:
            if heading in data.keys():
                if type(data[heading])==list:
                    data_pd_summary.append(data[heading][0])
                else:
                    data_pd_summary.append(data[heading])
            elif heading in design_info_dict.keys():
                if type(design_info_dict[heading])==list:
                    data_pd_summary.append(design_info_dict[heading][0])
                else:
                    data_pd_summary.append(design_info_dict[heading])
                
        data_pd_summary = tuple(data_pd_summary)
        
        
        if data['Renormalized PD']==True:
            headings_pd_vals = ('BeamID','Beam_PairID','PD_Max','IncidentPower','AcceptedPower','RadiatedPower','RadiatedPower_NoRenorm','PeakRealizedGain')
        else:
            headings_pd_vals = ('BeamID','Beam_PairID','PD_Max','IncidentPower','AcceptedPower','RadiatedPower','PeakRealizedGain')
            
        data_pd_vals_all = []
        for idx, beam_id in enumerate(beam_ids):
            data_pd_vals_row = []
            for heading in headings_pd_vals:
                if heading=='BeamID':
                    data_pd_vals_row.append(beam_id)
                elif heading=='Beam_PairID':
                    val = data['Beam_PairID'][idx]
                    if val == -1:
                        val='None'
                    data_pd_vals_row.append(val)
                elif type(data[heading])==dict:
                    val = np.round(data[heading][beam_id],5)
                    data_pd_vals_row.append(val)
                else:
                    val = np.round(data[heading][idx],5)
                    data_pd_vals_row.append(val)
            data_pd_vals_row = tuple(data_pd_vals_row)
            data_pd_vals_all.append(data_pd_vals_row)
        data_pd_vals_all = tuple(data_pd_vals_all)
        
        all_images = []
        
        for idx, each in enumerate(data['Paths_To_Images']):
            if type(data['Paths_To_Images'])==dict:
                all_images.append('\"' + data['Paths_To_Images'][each]+'\"')
            else:
                all_images.append('\"'  + data['Paths_To_Images'][idx]+'\"')

        outputfile = self.base_path +self.name +'.html'

        subs = jinja2.Environment( 
                      loader=jinja2.FileSystemLoader('./')      
                      ).get_template('./template/template_pd.html').render(title=title,
                                                             headings_pd_summary=headings_pd_summary,
                                                             data_pd_summary=data_pd_summary,
                                                             headings_pd_vals=headings_pd_vals,
                                                             data_pd_vals_all=data_pd_vals_all,
                                                             all_images=all_images)
        # lets write the substitution to a file
        with open(outputfile,'w') as f: f.write(subs)
        print(f"INFO: Summary report written to {outputfile}")
        #all_job_folders = self.get_jobs()
        
    def generate_html_cdf(self,data,multirun_file = ''):
        
        
        title = 'CDF Summary Report: '
        
        if data['JobID']!='All':
            design_info_dict = self.get_design_info(data['JobID'])
            multirun_file=False
            title = 'CDF Summary Report: ' + design_info_dict['Design_Name']
            
        else:
            design_info_dict = {'Multi-Run':multirun_file}
            multirun_file=True
            title = 'CDF Density Summary Report: Multi-Run '
        
        percentiles =list(data['Percentile'])
        if 'Module_Name' in data.keys():
            headings_cdf_summary = ('Project_Name','Design_Name','Solution_Name','Codebook_Name','Freq','CS_Name','Module_Name')
        elif not multirun_file:
            headings_cdf_summary = ('Project_Name','Design_Name','Solution_Name','Codebook_Name','Freq','CS_Name')
        else:
            headings_cdf_summary = ('Multi-Run',)
            
        data_cdf_summary = []
        for heading in headings_cdf_summary:
            if heading in data.keys():
                if type(data[heading])==list:
                    data_cdf_summary.append(data[heading][0])
                else:
                    data_cdf_summary.append(data[heading])
            elif heading in design_info_dict.keys():
                if type(design_info_dict[heading])==list:
                    data_cdf_summary.append(design_info_dict[heading][0])
                else:
                    data_cdf_summary.append(design_info_dict[heading])
                
        data_cdf_summary = tuple(data_cdf_summary)
        
        
        if data['CDF_Renormalized']==True:
            headings_cdf_vals = ('Percentile','CDF_Value','CDF_Value_Renorm')
        else:
            headings_cdf_vals = ('Percentile','CDF_Value')
            
        data_cdf_vals_all = []
        for idx, perc in enumerate(percentiles):
            data_cdf_vals_row = []
            for heading in headings_cdf_vals:
                if type(data[heading])==dict:
                    val = np.round(data[heading][perc],2)
                    data_cdf_vals_row.append(val)
                else:
                    val = np.round(data[heading][idx],2)
                    data_cdf_vals_row.append(val)
            data_cdf_vals_row = tuple(data_cdf_vals_row)
            data_cdf_vals_all.append(data_cdf_vals_row)
        data_cdf_vals_all = tuple(data_cdf_vals_all)
        
        all_images = []
        
        for idx, each in enumerate(data['Paths_To_Images']):
            if type(data['Paths_To_Images'])==dict:
                all_images.append('\"'  + data['Paths_To_Images'][each]+'\"')
            else:
                all_images.append('\"' + data['Paths_To_Images'][idx]+'\"')

        outputfile = self.base_path +self.name +'.html'

        subs = jinja2.Environment( 
                      loader=jinja2.FileSystemLoader('./')      
                      ).get_template('./template/template_cdf.html').render(title=title,
                                                             headings_pd_summary=headings_cdf_summary,
                                                             data_pd_summary=data_cdf_summary,
                                                             headings_pd_vals=headings_cdf_vals,
                                                             data_pd_vals_all=data_cdf_vals_all,
                                                             all_images=all_images)
        # lets write the substitution to a file
        with open(outputfile,'w') as f: f.write(subs)
        print('Results Written: ' + outputfile)
        #all_job_folders = self.get_jobs()
# with document(title='Photos') as doc:
#     h1('Photos')
#     for path in photos:
#         div(img(src=path), _class='photo')


# with open('gallery.html', 'w') as f:
#     f.write(doc.render())