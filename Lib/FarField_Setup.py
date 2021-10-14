# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 11:43:07 2021

@author: asligar
"""

import numpy as np
import os
import Lib.Utillities as utils

class FarField_Utils():
    '''
    Various function used to extract far field from HFSS. Including creating
    a far field setup
    '''
    def __init__(self,aedtapp):
        self.aedtapp= aedtapp
        
    def insert_infinite_sphere(self,setup_name = "RadSetup_FF",overwrite = True,cs_name='Global'):
        oDesign = self.aedtapp.odesign
        
        oEditor = oDesign.SetActiveEditor("3D Modeler")
        existing_cs_names = oEditor.GetCoordinateSystems()
        if cs_name not in existing_cs_names:
            print('WARNING: ' + cs_name + ' Does not exist in Design. Check Setup. Using Global')
            cs_name='Global'
            
        oModule = oDesign.GetModule("BoundarySetup")
        does_rad_exist = oModule.GetBoundariesOfType('radiation')
        if len(does_rad_exist)==0:
            return False
        oModule = oDesign.GetModule("RadField")
        exisiting_setups = oModule.GetSetupNames('Infinite Sphere')
        original_setup_name =setup_name
    
        theta_start = '0deg'
        theta_stop = '180deg'
        theta_step = '5deg'
        phi_start = '-180deg'
        phi_stop = '180deg'
        phi_step = '5deg'
    
        use_local_cs = False
        if cs_name!='Global':
            use_local_cs = True
        setup_params = ["NAME:"+setup_name,    
            "UseCustomRadiationSurface:=", False,
            "ThetaStart:="        , theta_start ,
            "ThetaStop:="        , theta_stop,
            "ThetaStep:="        , theta_step,
            "PhiStart:="        , phi_start,
            "PhiStop:="        , phi_stop,
            "PhiStep:="        , phi_step,
            "UseLocalCS:="        , use_local_cs
            ]
            
        if use_local_cs:
            setup_params.append("CoordSystem:=")
            setup_params.append( cs_name)
            

        if setup_name in exisiting_setups:
            if overwrite == True:
                oModule.EditFarFieldSphereSetup(setup_name,setup_params) 
    
            else:
                n=1
                while setup_name in exisiting_setups:
                    setup_name = original_setup_name + "_" + str(n)
                    n+=1    
                oModule.InsertFarFieldSphereSetup(setup_params)
        else:
            oModule.InsertFarFieldSphereSetup(setup_params)
        self.name = setup_name
        return setup_name
    def get_antenna_parameters(self,sol_setup_name,ff_setup_name,freq):
        max_antenna_params_dict = {}
        qtys = ['PeakDirectivity','PeakGain','PeakRealizedGain','RadiatedPower','AcceptedPower','IncidentPower']
        oDesign = self.aedtapp.odesign
        oModule = oDesign.GetModule("ReportSetup")
        ctxt = ['Context:=',ff_setup_name]
        #sweeps=['Theta:=',['All'],'Phi:=',['All'],'Freq:=',[freq]]
        sweeps=['Freq:=',[freq]]
        for qty in qtys:
            try:
                solnData = oModule.GetSolutionDataPerVariation('Antenna Parameters', sol_setup_name, ctxt, sweeps, qty)
                data = solnData[0].GetRealDataValues(qty)
                max_antenna_params_dict[qty] = data[0]
            except:
                print("ERROR: exporting antenna parameters failed")
                return False

        return max_antenna_params_dict
    

        
    def export_all_ffd(self,ff_setup_name,freq='',setup_name = "Setup1:LastAdaptive",export_path='./',overwrite=True):
        '''
        Returns the embedded element patterns of all ports in array

        Parameters:
                oDesign: oDesign object passed from Ansys Automation Script
                setup_name (str): solution setup name, must include "lastAdaptive" or sweep name
                ff_setup (str): name of infinite sphere far fiefld setup that should be used
                freq (str): frequency point to extract, 

        Returns:
                results_dict (dict): dictionary with port names as keys and ffd file file path as value
        '''
        print('Exporting Embedded Element Patterns...')

        oDesign = self.aedtapp.odesign
        oModule = oDesign.GetModule("RadField")
        
        exported_name_base = 'eep'
        exported_name_map = exported_name_base + '.txt'
        
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        
        oModule.ExportElementPatternToFile(
            [
                "ExportFileName:="    , export_path  + exported_name_base + '.ffd',
                "SetupName:="        , ff_setup_name,
                "IntrinsicVariationKey:=", "Freq=\'"+str(freq)+"\'",
                "DesignVariationKey:="    , "",
                "SolutionName:="    , setup_name
            ])
        
        if os.path.exists(export_path + '/' + exported_name_map):
            with open(export_path + '/' + exported_name_map, 'r') as reader:
                lines = [line.split(None) for line in reader]
            reader.close()
            lines=lines[1:] #remove header
            
            path_dict={}
            for pattern in lines:
                if len(pattern)==2:
                    port = pattern[0]
                    if ':' in port:
                        port = port.split(':')[0]
                    path_dict[port]=export_path + '/' + pattern[1]+ '.ffd'
    
            return path_dict
        else:
            return False
    

    
    
