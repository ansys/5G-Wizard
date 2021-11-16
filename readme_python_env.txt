#Here is one way to get everything up and running. Other options exists, one area that you may want to consider changing is the python envionrment manager. It doesn't matter what evionrment manager you use, as long as you can install all the required packages


Install anaconda:
https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe

###################
#act
# Create a anaconda envionrment
#
# conda create -n 5g_wizard python=3.8
# activate 5g_wizard 
#
###################

#Install packages, by typing the following in your anaconda prompt
#browse to 5G wizard directory and run

pip install -r requirements.txt


# You can use any IDE, if you want to use Spyder, install by typing >> conda install spyder=5.1.5
