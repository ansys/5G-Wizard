# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 07:56:52 2021

@author: asligar
"""

import sys
import os
import numpy as np
import scipy.io as sio
from Lib.NearFieldsProcessing import Load_NF_Fields
import h5py
import Lib.Utillities as utils
import matplotlib.pyplot as plt


class Validate_Reference_Data():
    def __init__(self,raw_data_input_file = './validation/raw_data_input.mat',output_dir = './validation/'):
        
        self.mat_raw_input = sio.loadmat(raw_data_input_file)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir
    def load_file(self,file_name):
        val_ref_path = 'validation\\References_A_6_2\\'
        pd_in = h5py.File(val_ref_path + file_name, 'r')
        value = np.asarray(pd_in['sav_vertex']['value'])
        value = np.rot90(np.fliplr(np.nan_to_num(value))) #different orientation than output from 5G wizard
        return value
    
    def reformat_data(self,data):
        '''
        The incput data from 5G wizard expects data as a dictionary, with the key
        beding the beam ID. the reference data does not have a beam ID, so
        just reformating to match dict[beam_id]

        '''
        data = data['0']
        return np.nan_to_num(data) #convert nan to zero
    
    
    def plot_data(self,list_of_data,list_of_titles=None,save_plot=False):
        
        fig, axs = plt.subplots(1,len(list_of_data))
        for n, data in enumerate(list_of_data):
            cs = axs[n].contourf(data)    
            if list_of_titles!=None:
                axs[n].set_title(list_of_titles[n])
                save_name  = list_of_titles[n].split(':')[1].replace('\n','')
            else:
                save_name='out'
    
        plt.show()
        if save_plot:
            fig.savefig(self.output_dir + save_name + '.png',dpi=300)
        return self.output_dir + save_name + '.png'
    def plot_data_3x1(self,list_of_data,list_of_titles=None,save_plot=True,save_name='out.png'):
    
        fig, axs = plt.subplots(1,3)
        fig.set_figheight(6)
        fig.set_figwidth(12)
        l0 = axs[0].contourf(list_of_data[0])
        l1 = axs[1].contourf(list_of_data[1])
        l2 = axs[2].contourf(list_of_data[2]*100,cmap='plasma')
        
        axs[0].set_title(list_of_titles[0])
        axs[1].set_title(list_of_titles[1])
        axs[2].set_title('Difference')
        
        fig.colorbar(l0, ax=list(axs[0:2]),orientation='vertical', pad=0.01,label='W/m^2',)
        fig.colorbar(l2, ax=axs[2],orientation='vertical', pad=0.01,label='Percentage (100%)',)
        
        plt.show()
        if save_plot:
            fig.savefig(self.output_dir + save_name + '.png',dpi=300)
            
        return self.output_dir + save_name + '.png'
    def run(self):
        summary_dict = {}
        output_image_names = []
        pd_n_notavg = self.load_file('Reference_Annex_A_6_2_sPD_n_plus_not_averaged.hdf5')
        pd_mod_notavg = self.load_file('Reference_Annex_A_6_2_sPD_mod_plus_not_averaged.hdf5')
        pd_tot_notavg = self.load_file('Reference_Annex_A_6_2_sPD_tot_plus_not_averaged.hdf5')
        
        pd_n_avg_1cm = self.load_file('Reference_Annex_A_6_2_sPD_n_plus_1cm2.hdf5')
        pd_n_avg_4cm = self.load_file('Reference_Annex_A_6_2_sPD_n_plus_4cm2.hdf5')
        
        pd_mod_avg_1cm = self.load_file('Reference_Annex_A_6_2_sPD_mod_plus_1cm2.hdf5')
        pd_mod_avg_4cm = self.load_file('Reference_Annex_A_6_2_sPD_mod_plus_4cm2.hdf5')
        
        pd_tot_avg_1cm = self.load_file('Reference_Annex_A_6_2_sPD_tot_plus_1cm2.hdf5')
        pd_tot_avg_4cm = self.load_file('Reference_Annex_A_6_2_sPD_tot_plus_4cm2.hdf5')
        
        
        pd_raw = self.mat_raw_input['pd_raw']
        
        #match format expected by 5G wizard which is a dictionary of field values, with a dcitionary of beam ids
        temp_dict = {'P':pd_raw}
        raw_data_dict= {'0':temp_dict} #beam id 0 (only 1 beam)
        surface_normal = np.array([0,0,1])
        
        nfd_files_dict = None
        length = .2
        width = .2
        length_n=101
        width_n=101
        averaging_area_1cm = .0001
        averaging_area_4cm = .0004
        grid_size=.002
        
        fields_data = Load_NF_Fields(nfd_files_dict,length,width,length_n,width_n)
        reshape_with_xyz=tuple(list([length_n,width_n]+[3]))
        fields_data.pos=np.reshape(fields_data.pos,reshape_with_xyz)
        
        
        pd_n_notavg_wiz = fields_data.get_PD_n_plus_local(raw_data_dict,surface_normal)
        pd_n_avg_1cm_wiz = fields_data.average_pd(pd_n_notavg_wiz,averaging_area_1cm,grid_size)
        pd_n_avg_4cm_wiz = fields_data.average_pd(pd_n_notavg_wiz,averaging_area_4cm,grid_size)
        pd_n_notavg_wiz = self.reformat_data(pd_n_notavg_wiz)
        pd_n_avg_1cm_wiz = self.reformat_data(pd_n_avg_1cm_wiz)
        pd_n_avg_4cm_wiz = self.reformat_data(pd_n_avg_4cm_wiz)
        
        pd_mod_notavg_wiz = fields_data.get_PD_mod_plus_local(raw_data_dict,surface_normal)
        pd_mod_avg_1cm_wiz = fields_data.average_pd(pd_mod_notavg_wiz,averaging_area_1cm,grid_size)
        pd_mod_avg_4cm_wiz = fields_data.average_pd(pd_mod_notavg_wiz,averaging_area_4cm,grid_size)
        pd_mod_notavg_wiz = self.reformat_data(pd_mod_notavg_wiz)
        pd_mod_avg_1cm_wiz = self.reformat_data(pd_mod_avg_1cm_wiz)
        pd_mod_avg_4cm_wiz = self.reformat_data(pd_mod_avg_4cm_wiz)
        
        
        pd_tot_notavg_wiz = fields_data.get_PD_tot_plus_local(raw_data_dict,surface_normal)
        pd_tot_avg_1cm_wiz = fields_data.average_pd(pd_tot_notavg_wiz,averaging_area_1cm,grid_size)
        pd_tot_avg_4cm_wiz = fields_data.average_pd(pd_tot_notavg_wiz,averaging_area_4cm,grid_size)
        pd_tot_notavg_wiz = self.reformat_data(pd_tot_notavg_wiz)
        pd_tot_avg_1cm_wiz = self.reformat_data(pd_tot_avg_1cm_wiz)
        pd_tot_avg_4cm_wiz = self.reformat_data(pd_tot_avg_4cm_wiz)
        
        #local comparisons
        print('    ')
        print('Local PD Evaluation Comparisons')
        print('##########')
        diff_local_pd_n = np.abs((pd_n_notavg_wiz-pd_n_notavg)/np.max(np.abs(pd_n_notavg)))
        print('PD_N_Plus Difference Over All Points: ' + str(np.max(diff_local_pd_n)))
        diff_local_pd_mod = np.abs((pd_mod_notavg_wiz-pd_mod_notavg)/np.max(np.abs(pd_mod_notavg)))
        print('PD_Mod_Plus Difference Over All Points: ' + str(np.max(diff_local_pd_mod)))
        diff_local_pd_tot = np.abs((pd_tot_notavg_wiz-pd_tot_notavg)/np.max(np.abs(pd_tot_notavg)))
        print('PD_Tot_Plus Difference Over All Points: ' + str(np.max(diff_local_pd_tot)))
        print('    ')
        
        summary_dict['Local_PD_N_Plus_Max_Difference'] =  np.max(diff_local_pd_n)
        summary_dict['Local_PD_Mod_Plus_Max_Difference'] =  np.max(diff_local_pd_mod)
        summary_dict['Local_PD_Tot_Plus_Max_Difference'] =  np.max(diff_local_pd_tot)
        
        #1cm averaging comparisons
        
        print('1cm Averaging PD Evaluation Comparisons')
        print('##########')
        diff_avg_pd_n_1cm = np.abs((pd_n_avg_1cm_wiz-pd_n_avg_1cm)/np.max(np.abs(pd_n_avg_1cm)))
        max_diff_avg_pd_n_1cm = np.max(diff_avg_pd_n_1cm)
        max_diff_avg_pd_n_1cm_perc = np.round(max_diff_avg_pd_n_1cm*100,6)
        print('PD_N_Plus Difference Over All Points: ' + str(max_diff_avg_pd_n_1cm_perc)+ ' %')
        print('Reference Max PD_N_Plus: ' + str(np.max(pd_n_avg_1cm)))
        print('5G Wizard Max PD_N_Plus: ' + str(np.max(pd_n_avg_1cm_wiz)))
        peak_diff_perct = np.abs(np.max(pd_n_avg_1cm)-np.max(pd_n_avg_1cm_wiz))/np.max(pd_n_avg_1cm)*100
        print('Peak Difference PD_N_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['N_Plus_Max_Diff_1cm_Avg_Pct'] =  np.max(max_diff_avg_pd_n_1cm_perc)
        summary_dict['N_Plus_AtPeak_Diff_1cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        
        diff_avg_pd_tot_1cm = np.abs((pd_tot_avg_1cm_wiz-pd_tot_avg_1cm)/np.max(np.abs(pd_tot_avg_1cm)))
        max_diff_avg_pd_tot_1cm = np.max(diff_avg_pd_tot_1cm)
        max_diff_avg_pd_tot_1cm_perc = np.round(max_diff_avg_pd_tot_1cm*100,6)
        print('PD_tot_Plus Difference Over All Points: ' + str(max_diff_avg_pd_tot_1cm_perc)+ ' %')
        print('Reference Max PD_tot_Plus: ' + str(np.max(pd_tot_avg_1cm)))
        print('5G Wizard Max PD_tot_Plus: ' + str(np.max(pd_tot_avg_1cm_wiz)))
        peak_diff_perct = np.abs(np.max(pd_tot_avg_1cm)-np.max(pd_tot_avg_1cm_wiz))/np.max(pd_tot_avg_1cm)*100
        print('Peak Difference PD_tot_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['Tot_Plus_Max_Diff_1cm_Avg_Pct'] =  np.max(max_diff_avg_pd_tot_1cm_perc)
        summary_dict['Tot_Plus_AtPeak_Diff_1cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        
        diff_avg_pd_mod_1cm = np.abs((pd_mod_avg_1cm_wiz-pd_mod_avg_1cm)/np.max(np.abs(pd_mod_avg_1cm)))
        max_diff_avg_pd_mod_1cm = np.max(diff_avg_pd_tot_1cm)
        max_diff_avg_pd_mod_1cm_perc = np.round(max_diff_avg_pd_mod_1cm*100,6)
        print('PD_mod_Plus Difference Over All Points: ' + str(max_diff_avg_pd_mod_1cm_perc) + ' %')
        print('Reference Max PD_mod_Plus: ' + str(np.max(pd_mod_avg_1cm)))
        print('5G Wizard Max PD_mod_Plus: ' + str(np.max(pd_mod_avg_1cm_wiz)))
        peak_diff_perct = np.abs(np.max(pd_mod_avg_1cm)-np.max(pd_mod_avg_1cm_wiz))/np.max(pd_mod_avg_1cm)*100
        print('Peak Difference PD_mod_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['Mod_Plus_Max_Diff_1cm_Avg_Pct'] =  np.max(max_diff_avg_pd_mod_1cm_perc)
        summary_dict['Mod_Plus_AtPeak_Diff_1cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        
        
        
        #4cm averaging comparisons
        print('4cm Averaging PD Evaluation Comparisons')
        print('##########')
        diff_avg_pd_n_4cm = np.abs((pd_n_avg_4cm_wiz-pd_n_avg_4cm)/np.max(np.abs(pd_n_avg_4cm)))
        max_diff_avg_pd_n_4cm = np.max(diff_avg_pd_n_4cm)
        max_diff_avg_pd_n_4cm_perc = np.round(max_diff_avg_pd_n_4cm*100,6)
        print('PD_N_Plus Difference Over All Points: ' + str(max_diff_avg_pd_n_4cm_perc)+ ' %')
        print('Reference Max PD_N_Plus: ' + str(np.max(pd_n_avg_4cm)))
        print('5G Wizard Max PD_N_Plus: ' + str(np.max(pd_n_avg_4cm_wiz)))
        peak_diff_perct = np.abs(np.max(pd_n_avg_4cm)-np.max(pd_n_avg_4cm_wiz))/np.max(pd_n_avg_4cm)*100
        print('Peak Difference PD_N_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['N_Plus_Max_Diff_4cm_Avg_Pct'] =  np.max(max_diff_avg_pd_n_4cm_perc)
        summary_dict['N_Plus_AtPeak_Diff_4cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        
        diff_avg_pd_tot_4cm = np.abs((pd_tot_avg_4cm_wiz-pd_tot_avg_4cm)/np.max(np.abs(pd_tot_avg_4cm)))
        max_diff_avg_pd_tot_4cm = np.max(diff_avg_pd_tot_4cm)
        max_diff_avg_pd_tot_4cm_perc = np.round(max_diff_avg_pd_tot_4cm*100,6)
        print('PD_tot_Plus Difference Over All Points: ' + str(max_diff_avg_pd_tot_4cm_perc)+ ' %')
        print('Reference Max PD_tot_Plus: ' + str(np.max(pd_tot_avg_4cm)))
        print('5G Wizard Max PD_tot_Plus: ' + str(np.max(pd_tot_avg_4cm_wiz)))
        peak_diff_perct =np.abs(np.max(pd_tot_avg_4cm)-np.max(pd_tot_avg_4cm_wiz))/np.max(pd_tot_avg_4cm)*100
        print('Peak Difference PD_tot_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['Tot_Plus_Max_Diff_4cm_Avg_Pct'] =  np.max(max_diff_avg_pd_tot_4cm_perc)
        summary_dict['Tot_Plus_AtPeak_Diff_4cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        
        diff_avg_pd_mod_4cm = np.abs((pd_mod_avg_4cm_wiz-pd_mod_avg_4cm)/np.max(np.abs(pd_mod_avg_4cm)))
        max_diff_avg_pd_mod_4cm = np.max(diff_avg_pd_tot_4cm)
        max_diff_avg_pd_mod_4cm_perc = np.round(max_diff_avg_pd_mod_4cm*100,6)
        print('PD_mod_Plus Difference Over All Points: ' + str(max_diff_avg_pd_mod_4cm_perc) + ' %')
        print('Reference Max PD_mod_Plus: ' + str(np.max(pd_mod_avg_4cm)))
        print('5G Wizard Max PD_mod_Plus: ' + str(np.max(pd_mod_avg_4cm_wiz)))
        peak_diff_perct =np.abs(np.max(pd_mod_avg_4cm)-np.max(pd_mod_avg_4cm_wiz))/np.max(pd_mod_avg_4cm)*100
        print('Peak Difference PD_mod_Plus: ' + str(peak_diff_perct)+ ' %')
        summary_dict['Mod_Plus_Max_Diff_4cm_Avg_Pct'] = np.max(max_diff_avg_pd_mod_4cm_perc)
        summary_dict['Mod_Plus_AtPeak_Diff_4cm_Avg_Pct'] = peak_diff_perct
        print('    ')
        

        
        titles = ['5G Wizard: \nLocal PD_N_Plus','Reference Data:\nLocal PD_N_Plus']
        report_path = self.plot_data([pd_n_notavg_wiz,pd_n_notavg],list_of_titles=titles)
        output_image_names.append(report_path)
        titles = ['5G Wizard: \nLocal PD_Tot_Plus','Reference Data: \nLocal PD_Tot_Plus']
        report_path = self.plot_data([pd_tot_notavg_wiz,pd_tot_notavg],list_of_titles=titles)
        output_image_names.append(report_path)
        titles = ['5G Wizard: \nLocal PD_Mod_Plus','Reference Data: \nLocal PD_Mod_Plus']
        report_path = self.plot_data([pd_mod_notavg_wiz,pd_mod_notavg],list_of_titles=titles)
        output_image_names.append(report_path)
        
        titles=['5G Wizard: \n1cm Avg PD_N_Plus','Reference Data: \n1cm Avg PD_N_Plus']
        report_path = self.plot_data([pd_n_avg_1cm_wiz,pd_n_avg_1cm],list_of_titles=titles)
        output_image_names.append(report_path)
        titles =['5G Wizard: \n1cm Avg PD_Tot_Plus','Reference Data: \n1cm Avg PD_Tot_Plus']
        report_path = self.plot_data([pd_tot_avg_1cm_wiz,pd_tot_avg_1cm],list_of_titles=titles)
        output_image_names.append(report_path)
        titles = ['5G Wizard: \n1cm Avg PD_Mod_Plus','Reference Data: \n1cm Avg PD_Mod_Plus']
        report_path = self.plot_data([pd_mod_avg_1cm_wiz,pd_mod_avg_1cm],list_of_titles=titles)
        output_image_names.append(report_path)
        
        titles=['5G Wizard: \n4cm Avg PD_N_Plus','Reference Data: \n4cm Avg PD_N_Plus']
        report_path = self.plot_data([pd_n_avg_4cm_wiz,pd_n_avg_4cm],list_of_titles=titles)
        output_image_names.append(report_path)
        titles=['5G Wizard: \n4cm Avg PD_Tot_Plus','Reference Data: \n4cm Avg PD_Tot_Plus']
        report_path = self.plot_data([pd_tot_avg_4cm_wiz,pd_tot_avg_4cm],list_of_titles=titles)
        output_image_names.append(report_path)
        titles=['5G Wizard: \n4cm Avg PD_Mod_Plus','Reference Data: \n4cm Avg PD_Mod_Plus']
        report_path = self.plot_data([pd_mod_avg_4cm_wiz,pd_mod_avg_4cm],list_of_titles=titles)
        output_image_names.append(report_path)
        
        titles=['Reference Data: \n4cm Avg PD_Tot_Plus','5G Wizard: \n4cm Avg PD_Tot_Plus']
        report_path = self.plot_data_3x1([pd_tot_avg_4cm,
                        pd_tot_avg_4cm_wiz,
                        diff_avg_pd_tot_4cm],
                        list_of_titles=titles,
                        save_name='4cm_PD_Tot_Plus_Compare')
        output_image_names.append(report_path)
        titles=['Reference Data: \n4cm Avg PD_Mod_Plus','5G Wizard: \n4cm Avg PD_Mod_Plus']
        report_path = self.plot_data_3x1([pd_mod_avg_4cm,
                        pd_mod_avg_4cm_wiz,
                        diff_avg_pd_mod_4cm],
                        list_of_titles=titles,
                        save_name='4cm_PD_Mod_Plus_Compare')
        output_image_names.append(report_path)
        titles=['Reference Data: \n4cm Avg PD_N_Plus','5G Wizard: \n4cm Avg PD_N_Plus']
        report_path = self.plot_data_3x1([pd_n_avg_4cm,
                        pd_n_avg_4cm_wiz,
                        diff_avg_pd_n_4cm],
                        list_of_titles=titles,
                        save_name='4cm_PD_N_Plus_Compare')
        output_image_names.append(report_path)
        
        titles=['Reference Data: \n1cm Avg PD_Tot_Plus','5G Wizard: \n1cm Avg PD_Tot_Plus']
        self.plot_data_3x1([pd_tot_avg_1cm,
                        pd_tot_avg_1cm_wiz,
                        diff_avg_pd_tot_1cm],
                        list_of_titles=titles,
                        save_name='1cm_PD_Tot_Plus_Compare')
        output_image_names.append(report_path)
        titles=['Reference Data: \n1cm Avg PD_Mod_Plus','5G Wizard: \n1cm Avg PD_Mod_Plus']
        self.plot_data_3x1([pd_mod_avg_1cm,
                        pd_mod_avg_1cm_wiz,
                        diff_avg_pd_mod_1cm],
                        list_of_titles=titles,
                        save_name='1cm_PD_Mod_Plus_Compare')
        output_image_names.append(report_path)
        titles=['Reference Data: \n1cm Avg PD_N_Plus','5G Wizard: \n1cm Avg PD_N_Plus']
        self.plot_data_3x1([pd_n_avg_1cm,
                        pd_n_avg_1cm_wiz,
                        diff_avg_pd_n_1cm],
                        list_of_titles=titles,
                        save_name='1cm_PD_N_Plus_Compare')
        output_image_names.append(report_path)
        
        summary_dict['OutputImages'] = output_image_names
        summary_dict = utils.dict_with_numpy_to_lists(summary_dict)
        utils.write_dictionary_to_json(path=self.output_dir+'validation_summary.json',dict_to_write=summary_dict)
        print('Validation Summary Exported: ' +self.output_dir+'validation_summary.json' )
        validation_results = self.output_dir+'validation_summary.json'
