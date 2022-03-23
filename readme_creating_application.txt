I recommend creating a new anaconda enviornment just for doing this, becuase I had an issue with pyqt versions using the same environment that spyder is installed into
###################
#
# From the 5G python environment
#
###################



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

pyinstaller -F 5G_Wizard.spec

This will create an exe and the /dist folder