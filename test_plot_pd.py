# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 11:29:36 2021

@author: asligar
"""
import json
import pyaedt 
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy import interpolate
import pyvista as pv
import os

cad_file = 'C:\\Users\\asligar\\OneDrive - ANSYS, Inc\\Desktop\\delete\\asdfasdf.obj'
mtl_file = 'C:\\Users\\asligar\\OneDrive - ANSYS, Inc\\Desktop\\delete\\asdfasdf.mtl'
file_path = 'C:\\Users\\asligar\\OneDrive - ANSYS, Inc\\Documents\\Scripting\\github\\5G-Wizard\\output\\2021-11-16_084353\\CDF\\JobID_0\\CDF.json'
with open(file_path) as f:
  data = json.load(f)
  
#plot envelope pattern on geometry

ff_data = data['RealizedGain']
ff_data_dB = 10*np.log10(data['RealizedGain'])
legend = []


theta = np.deg2rad(np.array(data['Theta']))
phi = np.deg2rad(np.array(data['Phi']))

ff_max_dB = np.max(ff_data_dB)
ff_min_dB = np.min(ff_data_dB)
ff_data_dB_renorm = (ff_data_dB-ff_min_dB)/(ff_max_dB-ff_min_dB)

r_no_renorm = np.reshape(ff_data_dB,(len(data['Theta']),len(data['Phi'])))
r = np.reshape(ff_data_dB_renorm,(len(data['Theta']),len(data['Phi'])))

phi_grid,theta_grid = np.meshgrid(phi, theta)

#test = interpolate.interp2d(r,phi_grid, theta_grid)

x = r * np.sin(theta_grid) * np.cos(phi_grid)
y = r * np.sin(theta_grid) * np.sin(phi_grid)
z = r * np.cos(theta_grid)




fig1 = plt.figure()
#fig1, ax1 = plt.subplots(1,1,1,projection="3d")
ax1 = fig1.add_subplot(1, 1, 1, projection="3d")
my_col = cm.jet(r/np.amax(r))
#plt.get_cmap("jet")
plot = ax1.plot_surface(
    x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap("jet"),facecolors = my_col, linewidth=0, antialiased=True, alpha=0.9)
#fig1.set_size_inches(22.5, 22.5)
plt.colorbar(plot)

list_of_observations= [(-45,-45)]
for n, observe in enumerate(list_of_observations):
    ax1.view_init(elev=observe[0], azim=observe[1])
    plt.show()


xx = np.ndarray.flatten(x,order='C')
yy = np.ndarray.flatten(y,order='C')
zz = np.ndarray.flatten(z,order='C')

mag = np.ndarray.flatten(r_no_renorm,order='F')

#for_point cloud
points = np.zeros((len(xx),3))
points[:,0]=xx
points[:,1]=yy
points[:,2]=zz


def rotationMatrixToEulerAngles(R) :

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

test = rotationMatrixToEulerAngles(np.eye(3))
# create a mesh that can be displayed
ff_mesh = pv.StructuredGrid(x,y,z)
#ff_mesh.scale(4)
#ff_mesh.translate([10,1,10])
#ff_mesh.rotate_vector(test)
ff_mesh["RealizedGain (dB)"] = mag


# Show the result in a plotter window
# p = pv.Plotter()
# p.add_mesh(ff_mesh, smooth_shading=True,cmap="jet")
# p.show()
pos = (10,10,10)
def scale(value=1):
    ff.SetScale(value,value,value)
    ff.SetPosition(pos)
    ff.SetOrientation(0,0,0)
    #p.add_mesh(ff_mesh, smooth_shading=True,cmap="jet")
    return




#plot everything together
cad_mesh = pv.read(cad_file)
def toggle_vis_ff(flag):
    ff.SetVisibility(flag)
def toggle_vis_cad(flag):
    cad.SetVisibility(flag)
p = pv.Plotter()

files = []
def get_new_file_name():
    increment=1
    #print("Window size ", p.window_size)
    file_name = "C:\\temp\\geo_envelope_overlay" + str(increment) + ".png"
    while os.path.exists(file_name):
        increment+=1
        file_name = "C:\\temp\\geo_envelope_overlay" + str(increment) + ".png"
    return file_name
def screenshot():
    
    #p.clear_slider_widgets()
    value.EnabledOff()
    ff_toggle.Off()
    cad_toggle.EnabledOff()
    help_text.VisibilityOff()
    #p.view_xy()
    p.update()
    file_name = get_new_file_name()
    files.append(file_name)
    p.screenshot(file_name, transparent_background=False)
    value.EnabledOn()
    ff_toggle.EnabledOn()
    cad_toggle.EnabledOn()
    help_text.VisibilityOn()
    p.update()
    return file_name
    #print("Camera position ", p.camera_position)
    

screenshot_keyboard = p.add_key_event("s", screenshot)

ff = p.add_mesh(ff_mesh,smooth_shading=True,cmap="jet",name='testtest')
p.remove_scalar_bar
value = p.add_slider_widget(scale, [.1, 10], title='Scale Far Field Plot',value=5)
ff_toggle = p.add_checkbox_button_widget(toggle_vis_ff, value=True)
color_display_type = ''
if 'MaterialIds' in cad_mesh.array_names:
    color_display_type = cad_mesh['MaterialIds']
else:
    color_display_type=None
cad = p.add_mesh(cad_mesh,scalars=color_display_type,show_scalar_bar=False,opacity=0.5)
cad_toggle = p.add_checkbox_button_widget(toggle_vis_cad, value=True,position=(10,70))
help_text = p.add_text("Press \'S\' to Generate Screenshot", position='upper_left', font_size=18, color=None)

show_plot=True
if not show_plot:
    file_name = get_new_file_name()
    value.EnabledOff()
    help_text.VisibilityOff()
    p.screenshot(file_name)
    file_name = get_new_file_name()
    p.view_xy()
    p.screenshot(file_name)
    p.view_yz()
    file_name = get_new_file_name()
    p.screenshot(file_name)
    p.view_xz()
    file_name = get_new_file_name()
    p.screenshot(file_name)
else:
    p.show()

 


