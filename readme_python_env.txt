#Here is one way to get everything up and running. Other options exists, one area that you may want to consider changing is the python envionrment manager. It doesn't matter what evionrment manager you use, as long as you can install all the required packages


Install anaconda:
https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe


#Create a new anaconda environment:
#Open an anaconda prompt and type:
>conda create -n env_name python=3.8
>activate env_name

#This will activate your python environment

#Install packages, by typing the following

pip install pywin32
pip install numpy
pip install h5py
pip install -U matplotlib
pip install pyaedt==0.3.25
pip install scipy
conda install spyder=5.0.5
