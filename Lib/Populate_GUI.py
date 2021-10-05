# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 11:48:53 2021

@author: asligar
"""

import numpy as np
class GUI_Values():
    def __init__(self,aedtapp):
        self.aedtapp = aedtapp
    def get_app(self):
        return self.aedtapp
    def get_project_names(self,):
        return list(self.aedtapp.odesktop.GetProjectList())
    def get_design_names(self,project_name):
        design_list = self.aedtapp.design_list
        if len(design_list)==0:
            design_list = 'No Valid Designs'
        return design_list
    def get_solution_setup_names(self,design_name):
        self.aedtapp.set_active_design(design_name)
        setups = self.aedtapp.get_setups()
        if len(setups)==0:
            setups = 'No Valid Setups'
            list_avail_setups = [setups]
        else:
            list_avail_setups = []
            for setup in setups:
                list_avail_setups.append(setup+ ':LastAdaptive')
                sweeps = self.get_sweep_names(setup)
                for sweep in sweeps:
                    list_avail_setups.append(setup + ':' + sweep)
        return list_avail_setups
        
    def get_sweep_names(self,setup_name):
        return self.aedtapp.get_sweeps(setup_name)

    def get_freq_values(self,setup_name):
        osolution = self.aedtapp.odesign.GetModule("Solutions")
        freqs = list(osolution.GetSolveRangeInfo(setup_name))
        return freqs
    def check_if_solution(self,setup_name):
        osolution = self.aedtapp.odesign.GetModule("Solutions")
        has_solution=False
        if setup_name!='No Valid Setups':
            has_solution = osolution.HasFields(setup_name,"nominal")
        return has_solution

    def evaluation_surfaces(self):
        oEditor = self.aedtapp.odesign.SetActiveEditor("3D Modeler")
        oObjects_sheets = oEditor.GetObjectsInGroup( "Sheets" )
    
        rectangle_objects = []
        for each in oObjects_sheets:
            edge_IDs = oEditor.GetEdgeIDsFromObject(each) 
            if len(edge_IDs)==4: 
                rectangle_objects.append(each)
        if len(rectangle_objects) == 0:
            rectangle_objects.append("No Valid Objects")
        
        return rectangle_objects
    
    def get_cs_names(self):
        '''
        Get coordinate systems that exist in the design

        '''
        oeditor = self.aedtapp.odesign.SetActiveEditor("3D Modeler")
        existing_cs_names = oeditor.GetCoordinateSystems()
        return existing_cs_names

    def available_variations(self,setup_name):
        '''
        get solved variations for specified setup name

        '''
        av = self.aedtapp.available_variations
        available_variations = av.variations(setup_name)
        
        if available_variations:
            self.unique_variations(available_variations)
        else:
            print("No Valid Variations Found for Design")
            self.variations_strings = ['Nominal']
            self.truncated_dict = {}
        return self.variations_strings, self.truncated_dict


    def unique_variations(self,variations):
        '''
        Reduce the number of values displayed in the UI
        by only showing variables that have changed
        '''
        
        dict_of_variations = {}
        for n, name_or_val in enumerate(variations):
            for m, nv in enumerate(name_or_val): #for some reason pyaedt returns a list for variables with a single value
                if isinstance(nv, list): #this will be the value
                    name_or_val[m]= nv[0] #get first value since I am not sure there will ever be more than 1 value
                else:
                    name_or_val[m]= nv.replace(':=','') #this is variable name, but remove the :=
            dict_of_names_and_vals = dict(zip(name_or_val[::2], name_or_val[1::2]))
            dict_of_variations[n] = dict_of_names_and_vals

        #get which variables have changed within all the available variations
        all_var_names = list(dict_of_variations[0].keys())
        if dict_of_variations:
            num_variations = len(dict_of_variations)
        else:
            num_variations=0
        list_of_changed_variables = []
        for variable in all_var_names:
            values = []
            for variation in dict_of_variations.keys():
                values.append(dict_of_variations[variation][variable])
            if len(set(values))>1:
                list_of_changed_variables.append(variable)
        
        #create the string that will be displayed
        truncated_dict = {}
        variations_strings = ['Nominal']
        if num_variations>1:
            for variation in dict_of_variations.keys():
                temp_dict = {}
                temp_str = str(variation) + '='
                for name in list_of_changed_variables:
                    temp_dict[name] = dict_of_variations[variation][name]
                    value = self.round_values(dict_of_variations[variation][name],decimals=2) 
                    temp_str=temp_str + name +':'+ value +' '
                variations_strings.append(temp_str)
                truncated_dict[variation] = temp_dict
        
        
        self.list_of_changed_variables = list_of_changed_variables
        self.dict_of_variations = dict_of_variations
        self.truncated_dict = truncated_dict
        self.variations_strings = variations_strings

    def round_values(self,unit_str, decimals=2):
        '''
        sometimes the output from aedt are number like 8.00000001mm. When they
        should be 8mm. This will round away those values and make them easier
        to display

        '''
        unit_str= unit_str.replace(" ","")

        try: #only a number entered, no units
            value = float(unit_str)
            units = ''
        except:
            if unit_str.isalpha(): #only a string, no value entered
                value = 1
                units = ''
            else: #alpha numeric value entered, remove units
                value = unit_str.rstrip('abcdefghijklmnopqrstuvwxyz')
                units = unit_str[len(value):]
                value = float(value)

        value = np.round(value,decimals)
        new_string = str(value) + units
        return new_string