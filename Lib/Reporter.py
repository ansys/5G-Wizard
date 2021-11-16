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
from matplotlib import cm
import pyvista as pv
import math


class Report_Module():
    def __init__(self,aedtapp,output_path,overwrite=True,job_id='0'):
        
        self.full_path = output_path  + 'JobID_' + str(job_id) + '/'
        self.relative_path = './JobID_' + str(job_id) + '/'
        self.output_path = output_path
        self.absolute_path = os.path.abspath(self.full_path)
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


    def polar_plot_3d(self,data,
                        save_name ="3D_Polar_Plot_Envelope",
                        save_plot=True,
                        show_plot=True,
                        output_path = '',
                        dB=True,
                        multiple_angles = True):
    
        if dB:
            ff_data = 10*np.log10(data['RealizedGain'])
            #renormalize to 0 and 1 
            ff_max_dB = np.max(ff_data)
            ff_min_dB = np.min(ff_data)
            ff_data_renorm = (ff_data-ff_min_dB)/(ff_max_dB-ff_min_dB)
        else:
            ff_data = data['RealizedGain']
            #renormalize to 0 and 1 
            ff_max = np.max(ff_data)
            ff_min = np.min(ff_data)
            ff_data_renorm = (ff_data-ff_max)/(ff_max-ff_min)
        legend = []
        
        theta = np.deg2rad(np.array(data['Theta']))
        phi = np.deg2rad(np.array(data['Phi']))
        phi_grid,theta_grid = np.meshgrid(phi, theta)
        
        r = np.reshape(ff_data_renorm,(len(data['Theta']),len(data['Phi'])))
        
        x = r * np.sin(theta_grid) * np.cos(phi_grid)
        y = r * np.sin(theta_grid) * np.sin(phi_grid)
        z = r * np.cos(theta_grid)
        
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1, 1, 1, projection="3d")
        my_col = cm.jet(r/np.amax(r))
        plot = ax1.plot_surface(
            x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap("jet"),facecolors = my_col, linewidth=0, antialiased=True, alpha=0.9)
        #fig1.set_size_inches(22.5, 22.5)
        plt.colorbar(plot)
        
        if output_path  == '':
            output_path = self.output_path
        else:
            output_path = self.full_path


        if save_plot:
           if multiple_angles:
               list_of_observations= [(0,0),(0,90),(0,180),(0,270),(90,0),(45,45),(45,-45),(-45,-45)]
               for n, observe in enumerate(list_of_observations):
                   ax1.view_init(elev=observe[0], azim=observe[1])
                   save_name = save_name + '_' + str(n) + '.png'
                   save_name_full = self.full_path + save_name
                   save_name_relative = self.relative_path + save_name 
                   plt.savefig(save_name_full,dpi=300)
                   self.all_figure_paths.append(save_name_relative)
           else:
                save_name_full = self.full_path + save_name + '.png'
                save_name_relative = self.relative_path + save_name + '.png'
                plt.savefig(save_name_full,dpi=300)
                self.all_figure_paths.append(save_name_relative)
        if show_plot:
            plt.show()
            
    def polar_plot_3d_pyvista(self,data,
                            save_name ="Interactive_Envelope_Pattern",
                            show_plot=True,
                            output_path = '',
                            dB=True,
                            show_cad=True,
                            position = np.zeros(3),
                            rotation = np.eye(3)):
        if dB:
            ff_data = 10*np.log10(data['RealizedGain'])
            #renormalize to 0 and 1 
            ff_max_dB = np.max(ff_data)
            ff_min_dB = np.min(ff_data)
            ff_data_renorm = (ff_data-ff_min_dB)/(ff_max_dB-ff_min_dB)
            display_name = "RealizedGain (dB)"
        else:
            ff_data = data['RealizedGain']
            #renormalize to 0 and 1 
            ff_max = np.max(ff_data)
            ff_min = np.min(ff_data)
            ff_data_renorm = (ff_data-ff_max)/(ff_max-ff_min)
            display_name = "RealizedGain"
            
        theta = np.deg2rad(np.array(data['Theta']))
        phi = np.deg2rad(np.array(data['Phi']))
        phi_grid,theta_grid = np.meshgrid(phi, theta)
        
        r_no_renorm = np.reshape(ff_data,(len(data['Theta']),len(data['Phi'])))
        r = np.reshape(ff_data_renorm,(len(data['Theta']),len(data['Phi'])))
        
        x = r * np.sin(theta_grid) * np.cos(phi_grid)
        y = r * np.sin(theta_grid) * np.sin(phi_grid)
        z = r * np.cos(theta_grid)
        
        #for color display
        mag = np.ndarray.flatten(r_no_renorm,order='F')
        
        # create a mesh that can be displayed
        ff_mesh = pv.StructuredGrid(x,y,z)
        #ff_mesh.scale(ff_scale)
        #ff_mesh.translate([float(position[0]),float(position[1]),float(position[2])])
        ff_mesh[display_name] = mag
        



        #plot everything together

        rotation_euler = self.rotationMatrixToEulerAngles(rotation)*180/np.pi
        #ff_mesh.rotate_vector(rotation_vector)
        if show_plot:
            p = pv.Plotter()
        else:
            p = pv.Plotter(off_screen=True)
        ff = p.add_mesh(ff_mesh,smooth_shading=True,cmap="jet")
        if show_cad:
            def toggle_vis_ff(flag):
                ff.SetVisibility(flag)
            def toggle_vis_cad(flag):
                cad.SetVisibility(flag)
            def scale(value=1):
                ff.SetScale(value,value,value)
                ff.SetPosition(position)
                ff.SetOrientation(rotation_euler)
                #p.add_mesh(ff_mesh, smooth_shading=True,cmap="jet")
                return
            
            def screenshot():
                scale_slider.EnabledOff()
                ff_toggle.Off()
                cad_toggle.EnabledOff()
                help_text.VisibilityOff()
                #p.view_xy()
                p.update()
                increment=1
                #print("Window size ", p.window_size)
                file_name = self.get_new_file_name()
                p.screenshot(file_name, transparent_background=False)
                scale_slider.EnabledOn()
                ff_toggle.EnabledOn()
                cad_toggle.EnabledOn()
                help_text.VisibilityOn()
                p.update()
                self.all_figure_paths.append(file_name)
            
            scale_slider = p.add_slider_widget(scale, [0, 10], title='Scale Plot',value=5)
            ff_toggle = p.add_checkbox_button_widget(toggle_vis_ff, value=True)
            oEditor = self.aedtapp.odesign.SetActiveEditor("3D Modeler")
            cad_file = self.absolute_path +'/geometry.obj'
            

            non_model_objects = oEditor.GetObjectsInGroup('Non Model')
            all_objects = oEditor.GetMatchedObjectName('*')
            
            s = set(non_model_objects)
            model_objects = [x for x in all_objects if x not in s]
            
            objects_to_display = []
            for each in model_objects:
                if 'radi' not in each.lower():
                    objects_to_display.append(each)
            print("INFO: Exporting Geometry for Display")
            oEditor.ExportModelMeshToFile(cad_file, objects_to_display)
            print("...Done")
            if os.path.exists(cad_file):
                cad_mesh = pv.read(cad_file)
                color_display_type = ''
                if 'MaterialIds' in cad_mesh.array_names:
                    color_display_type = cad_mesh['MaterialIds']
                else:
                    color_display_type=None
                cad = p.add_mesh(cad_mesh,scalars=color_display_type,show_scalar_bar=False,opacity=0.5)
                cad_toggle = p.add_checkbox_button_widget(toggle_vis_cad, value=True,position=(10,70))
            else:
                Print('WARNING: Unable to display CAD Geometry, ' + cad_file + ' is not found')
        help_text = p.add_text("Press \'S\' to Generate Screenshot", position='upper_left', font_size=18, color=None)
        p.add_key_event("s", screenshot)
        
        if not show_plot:
            file_name =  self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            scale_slider.EnabledOff()
            help_text.VisibilityOff()
            p.screenshot(file_name)
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.view_xy()
            p.screenshot(file_name)
            p.view_yz()
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.screenshot(file_name)
            p.view_xz()
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.screenshot(file_name)
        else:
            p.show()
        
        
    def field_plot_3d_pyvista(self,fields_data,
                            save_name ="Interactive_PD_Plot",
                            save_plot=True,
                            show_plot=True,
                            output_path = '',
                            show_cad=True):


        data=fields_data.p_avg_all_beams[0]
        beam_ids = list(fields_data.p_avg_all_beams.keys())
        xyz = []
        for xn in range(fields_data.pos_in_global.shape[0]):
            for yn in range(fields_data.pos_in_global.shape[1]):
                xyz.append([fields_data.pos_in_global[xn][yn][0],fields_data.pos_in_global[xn][yn][1],fields_data.pos_in_global[xn][yn][2]])
        
        xyz =np.array(xyz)*1000 #need to double check if obj is always export in mm or meter, or something else

        pos = np.ndarray.flatten(fields_data.pos_in_global,order='C')

        fields_mesh = pv.PolyData(xyz)
        mag = np.ndarray.flatten(fields_data.p_avg_all_beams[beam_ids[0]],order='C')
        fields_mesh[str(beam_ids[0])] = mag

        pd_surface = fields_mesh.delaunay_2d()

        if show_plot:
            p = pv.Plotter()
        else:
            p = pv.Plotter(off_screen=True)
        

        p.add_mesh(pd_surface,smooth_shading=True,cmap="jet",opacity=0.5,name='PD')
                
        first_beam = np.min(beam_ids)
        last_beam = np.max(beam_ids)
        beam_text = p.add_text("Beam ID: 0", position='lower_left', font_size=18, color=None)
        def beam_select(value=1):
            beam_select = str(int(value))
            p.remove_actor('PD')
            mag = np.ndarray.flatten(fields_data.p_avg_all_beams[int(value)],order='C')
            fields_mesh[str(beam_ids[0])] = mag
            pd_surface = fields_mesh.delaunay_2d()
            p.add_mesh(pd_surface,smooth_shading=True,cmap="jet",opacity=0.5,name='PD')
            beam_text.ClearAllTexts()
            beam_text.SetText(0,"Beam ID: " + beam_select)
            p.update()
            return
        
        if show_cad:
            def toggle_vis_cad(flag):
                cad.SetVisibility(flag)

            def screenshot():
                beam_slider.EnabledOff()
                ff_toggle.Off()
                cad_toggle.EnabledOff()
                help_text.VisibilityOff()
                #p.view_xy()
                p.update()
                increment=1
                #print("Window size ", p.window_size)
                file_name = self.get_new_file_name()
                p.screenshot(file_name, transparent_background=False)
                beam_slider.EnabledOn()
                ff_toggle.EnabledOn()
                cad_toggle.EnabledOn()
                help_text.VisibilityOn()
                p.update()
                self.all_figure_paths.append(file_name)
            
            #import geometry
            oEditor = self.aedtapp.odesign.SetActiveEditor("3D Modeler")
            cad_file = self.absolute_path +'/geometry.obj'
            
            non_model_objects = oEditor.GetObjectsInGroup('Non Model')
            all_objects = oEditor.GetMatchedObjectName('*')
            
            s = set(non_model_objects)
            model_objects = [x for x in all_objects if x not in s]
            
            objects_to_display = []
            for each in model_objects:
                if 'radi' not in each.lower():
                    objects_to_display.append(each)
            print("INFO: Exporting Geometry for Display")
            oEditor.ExportModelMeshToFile(cad_file, objects_to_display)
            print("...Done")
            if os.path.exists(cad_file):
                cad_mesh = pv.read(cad_file)
                color_display_type = ''
                if 'MaterialIds' in cad_mesh.array_names:
                    color_display_type = cad_mesh['MaterialIds']
                else:
                    color_display_type=None
                cad = p.add_mesh(cad_mesh,scalars=color_display_type,show_scalar_bar=False,opacity=0.5)
                cad_toggle = p.add_checkbox_button_widget(toggle_vis_cad, value=True,position=(10,70))
            else:
                Print('WARNING: Unable to display CAD Geometry, ' + cad_file + ' is not found')
                
            #add widgets
            beam_slider = p.add_slider_widget(beam_select, [first_beam, last_beam], title='Beam Select',value=0)
        help_text = p.add_text("Press \'S\' to Generate Screenshot", position='upper_left', font_size=18, color=None)
        
        p.add_key_event("s", screenshot)
        
        if not show_plot:
            file_name =  self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            scale_slider.EnabledOff()
            help_text.VisibilityOff()
            p.screenshot(file_name)
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.view_xy()
            p.screenshot(file_name)
            p.view_yz()
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.screenshot(file_name)
            p.view_xz()
            file_name = self.get_new_file_name()
            self.all_figure_paths.append(file_name)
            p.screenshot(file_name)
        else:
            p.show()
    def rotationMatrixToEulerAngles(self,R) :

        sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
        singular = sy < 1e-6
        if  not singular :
            x = math.atan2(R[2,1] , R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])
        else :
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0
        return np.array([x, y, z])
    
    def get_new_file_name(self):
        increment=1
        #print("Window size ", p.window_size)
        file_name = self.absolute_path + "\\geo_envelope_overlay" + str(increment) + ".png"
        while os.path.exists(file_name):
            increment+=1
            file_name = self.absolute_path + "\\geo_envelope_overlay" + str(increment) + ".png"
        return file_name