I recommend creating a new anaconda enviornment just for doing this, becuase I had an issue with pyqt versions using the same environment that spyder is installed into
###################
#
# Create a anaconda envionrment
#
# conda create -n pyside_env python=3.8
# activate pyside_env
#
###################


#install libraries
pip install pywin32
pip install pythonnet
pip install numpy
pip install h5py
pip install -U matplotlib
pip install pyinstaller
pip install pyaedt==0.3.25
pip install PySide6
pip install Jinja2

#if pywin32 not found, try installing with >>conda install -c conda-forge pywin32

############################
#
# Creating a GUI
#
#############################
Create *.ui file using QTDesigner
type pyside-designer into anaconda prompt
C:\Users\asligar\Anaconda3\envs\gpu_radar38\Lib\site-packages\PySide2\designer.exe
this will launch designer.exe

at terminal, convert ui to python needed for pyside6
pyside6-uic gui_v0.ui > gui_v0.py


##############################
#
# Creating an executable
#
###############################
from anaconda prompt (with enviroinment active that contains above libs) browse to directory where the python scripts are located
type:

pyinstaller -F 5G_Wizard.py

This will create an exe. Move the .ui file to the same location as the exe in order to run.