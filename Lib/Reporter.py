# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:50:47 2021

@author: asligar
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from datetime import date



class Report_Module():
    def __init__(self,aedtapp,output_path,overwrite=True,job_id='0'):
        
        self.full_path = output_path  + 'JobID_' + str(job_id) + '/'
        self.relative_path = './JobID_' + str(job_id) + '/'
        self.output_path = output_path
        self.aedtapp = aedtapp

        self.overwrite = overwrite
        self.all_figure_paths = []
        plt.close('all')
        #create directory if it doesn't exist, used to save results
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        
    def close_all_reports(self):
        plt.close('all')
        
    def max_vs_beam_bar(self,pd_max,title='Max Power Density',
                           pd_type_label = 'PD', 
                           save_name ="max_pd_bar" ,
                           save_plot=False,
                           show_plot=True):

            
        plt.bar(range(len(pd_max)), list(pd_max.values()), align='center')
        plt.xticks(range(len(pd_max)), list(pd_max.keys()))
        plt.xlabel("Beam IDs")
        plt.ylabel(pd_type_label)
        plt.title(title)
        if save_plot:
            save_name = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name,dpi=300)
            self.all_figure_paths.append(save_name_relative)
        if show_plot:
            plt.show()
            
        if not show_plot:
            plt.close('all')
        
    def max_vs_beam_line(self,pd_max,title='Max Power Density',
                            pd_type_label = 'PD', 
                            save_name ="max_pd_line",
                            save_plot=False,
                            show_plot=True):
        beam_ids = list(pd_max.keys())
        pd_max_vals = list(pd_max.values())


        fig, ax = plt.subplots()
        ax.plot(beam_ids,pd_max_vals)
        
        ax.set(xlabel='Beam IDs', ylabel=pd_type_label,
               title=title)
        ax.grid()
        
        if save_plot:
            save_name_full = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name_full,dpi=300)
            self.all_figure_paths.append(save_name_relative)
        if show_plot:
            plt.show()
            
        if not show_plot:
            plt.close('all')

    def plot_pd(self,pd,pos,title='Power Density', save_plot=False,save_name='pd',show_plot=True):
        
        fig, ax = plt.subplots(figsize=(5, 5))
        
        x_pos = pos[:,:,0]
        y_pos = pos[:,:,1]


        levels = np.linspace(np.nanmin(pd),np.nanmax(pd),64)
        plt.contourf(x_pos,y_pos,pd,cmap='rainbow',
                      levels=levels, extend='both')

        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title(title)
        
        #plt.axis('off')
        
        if save_plot:
            save_name_full = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name_full,dpi=300)
            self.all_figure_paths.append(save_name_relative)
        if not show_plot:
            plt.close('all')

    def pd_table(self,data,save_name='pd_table', save_plot=False,override_path=None):
        
        if override_path:
            output_path = override_path
        else:
            output_path = self.output_path
        job_ids = list(data.keys())
        
        table_data = []

        job_ids_list = list(job_ids)
        all_columns = list(data[job_ids_list[0]].keys())
        
        #remove columns of data we don't want to plot
        try:
            all_columns.remove("Paths_To_Avg_Data")
        except ValueError:
            pass
        try:
            all_columns.remove("Paths_To_Raw_Data")
        except ValueError:
            pass
        try:
            all_columns.remove("Paths_To_Images")
        except ValueError:
            pass
        try:
            all_columns.remove("PeakDirectivity")
        except ValueError:
            pass
        try:
            all_columns.remove("PeakRealizedGain")
        except ValueError:
            pass
        try:
            all_columns.remove("AcceptedPower")
        except ValueError:
            pass
        try:
            all_columns.remove("IncidentPower")
        except ValueError:
            pass
        try:
            all_columns.remove("RadiatedPower_NoRenorm")
        except ValueError:
            pass
        


        column_labels = all_columns
        row_labels = []
        for job in job_ids:

            beam_ids = list(data[job]['PD_Max'].keys())
            
            for n, beam_id in enumerate(beam_ids):
                row_data= []
                row_labels.append(str(job) + "_" + str(beam_id))
                for col in all_columns:
                    if isinstance( data[job][col], dict):
                        col_data = data[job][col][beam_id]
                    elif isinstance( data[job][col], list):
                        col_data = data[job][col][n]
                    else:
                        col_data = data[job][col]
                        if col.lower()=='freq':
                            col_data = str(np.round(float(col_data)*1e-9,2))+'GHz'
                        if col.lower()=='averaging_area':
                            col_data = str(np.round(float(col_data)*1e4,2))+'cm^2'
                    try:
                        float(col_data)
                        col_data = np.round(col_data,2)
                    except:
                        pass
                    row_data.append(col_data)
                table_data.append(row_data)


        title_text = 'PD Summary Report'
        footer_text = str(date.today())
        fig_background_color = 'black'
        fig_border = 'steelblue'
        
        
        # cell_text = []
        # for row in table_data:
        #     cell_text.append([f'{x:1.1f}' for x in row])
        # Get some lists of color specs for row and column headers
        rcolors = plt.cm.BuPu(np.full(len(row_labels), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_labels), 0.1))
        # Create the figure. Setting a small pad on tight_layout
        # seems to better regulate white space. Sometimes experimenting
        # with an explicit figsize here can produce better outcome.
        plt.figure(linewidth=2,
                   edgecolor=fig_border,
                   facecolor=fig_background_color,
                   tight_layout={'pad':1},
                   #figsize=(5,3)
                  )
        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=table_data,
                              rowLabels=row_labels,
                              rowColours=rcolors,
                              rowLoc='right',
                              colColours=ccolors,
                              colLabels=column_labels,
                              loc='center')
        # Scaling is the only influence we have over top and bottom cell padding.
        # Make the rows taller (i.e., make cell y scale larger).
        the_table.scale(1, 1.5)
        # Hide axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        # Hide axes border
        plt.box(on=None)
        # Add title
        plt.suptitle(title_text)
        # Add footer
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        # Force the figure to update, so backends center objects correctly within the figure.
        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()
        # Create image. plt.savefig ignores figure edge and face colors, so map them.
        fig = plt.gcf()
        
        if save_plot:
            save_name_full = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name_full,
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=300
                        )
            self.all_figure_paths.append(save_name_relative)
            


            
    def plot_far_field_rect(self,data,qty_str='',title='',
                            save_plot=False,
                            save_name='ff_plot'
                            ,dB=True,
                            output_path='',
                            show_plot=True,
                            levels = 64):
        
        fig, ax = plt.subplots(figsize=(5, 5))
        
        if qty_str=='':
            qty_to_plot = data
        else:
            qty_to_plot = data[qty_str]
        qty_to_plot = np.reshape(qty_to_plot,(data['nTheta'],data['nPhi']))
        th,ph = np.meshgrid(data['Theta'], data['Phi'])

        if dB:
            factor =20
            if 'Gain' in qty_str:
                factor =10
            qty_to_plot = factor*np.log10(np.abs(qty_to_plot))

        if title=='':            
            plt.title(qty_str)
        else:
            plt.title(title)
            
        plt.xlabel('Theta (degree)')
        plt.ylabel('Phi (degree)')

        plt.contourf(th,ph,qty_to_plot.T,levels=levels,cmap='jet',)
        
        plt.colorbar()

        print('Peak '+ qty_str + ': ' +  str(np.max(qty_to_plot)))


        if save_plot:
            save_name_full = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name_full,dpi=300)
            self.all_figure_paths.append(save_name_relative)
        if not show_plot:
            plt.close('all')
    def polar_plot(self,data, qty_str,title=''):
 
        qty_to_plot = data[qty_str]
        qty_to_plot = np.reshape(qty_to_plot,(data['nPhi'],data['nTheta']))
        th,ph = np.meshgrid(data['Theta'], data['Phi'])
        if 'Gain' in qty_str:
            factor =10
        else:
            factor =20
            
        ax = plt.subplot(111, projection="polar")
        legend = []


        theta = data['Theta']
        r = np.array(qty_to_plot)
        ax.plot(theta, r)
        ax.grid(True)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)


        ax.set_title("Realized Gain Total", va="bottom")
        fig = plt.gcf()
        fig.set_size_inches(22.5, 22.5)
        
    def plot_xy(self,x,y,title='xy plot', 
                            xlabel = 'x',
                            ylabel= 'y',
                            save_name ="yx_plot",
                            save_plot=False,
                            show_plot=True,
                            output_path = '',
                            dB=True):


        if dB:
            x=10*np.log10(x)
        fig, ax = plt.subplots()
        ax.plot(x,y)
    
        ax.set(xlabel=xlabel, ylabel=ylabel,
               title=title)
        ax.grid()
        
        if output_path  == '':
            output_path = self.output_path
        else:
            output_path = self.full_path


        if save_plot:
           
            save_name_full = self.full_path + save_name + '.png'
            save_name_relative = self.relative_path + save_name + '.png'
            plt.savefig(save_name_full,dpi=300)
            self.all_figure_paths.append(save_name_relative)
        if show_plot:
            plt.show()
