
# -*- coding: utf-8 -*-

"""
      Written by : Arien Sligar (arien.sligar@ansys.com)
      Last updated : 09.07.2021

    incldues all functions that are related to codebook import and setting
    up the edit sources
"""


import csv
import os
import sys
class Codebook_Utils():
    def __init__(self,aedtapp,file_name):
        '''
        Reads csv file of codebook with header
        Beam_ID,module_name,Ant_Feed,Amplitude,Phase,Paired_With
        
        additional columns of data can be included but are not required
        module_name is only used for output of reports
        
        data format should be 
        
        Beam_ID,module_name,Ant_Feed,Amplitude,Phase,Paired_With
        <int>,<string>,port_names1;port_name2;port_name3,1;1;1,0;30;60,<int>
        
        only ports which are excited should be included, if not excited leave out of list.
        Beam IDs should be as a integer value, does not need to be sorted, but cannot accept duplicates
        
        Paired with can be any other beam id that exists in the table, if no beam pair is used, -1 should be used
        Entires for Amplitude and Phase are seperated by ";" and need to be in the same 
        order as the port names appear. For driven model, amplitude is in Watts,
        For driven terminal, amplitude is in volts. Phase is always in degrees
        
        Parameters
        ----------
        aedtapp : TYPE
            HFSS object from AEDTLib.HFSSmodule.
        file_name : TYPE
            file name and path of codebook location.

        Returns
        -------
        None.

        '''
        all_ports = []
        vector_dict = {}
        with open(file_name) as csvfile:
            header = csvfile.readline()
            header = header.replace(" ","").replace("\n","")
            header = header.split(',')
            
            reader = csv.DictReader(csvfile,fieldnames=tuple(header))
            if 'Beam_ID' not in header:
                pass #need to add in format checking for codebook
            vector_dict = {}
            for row in reader: #each row will corropsond to a beam id
                
                port_names_temp = row['Ant_Feed']
                port_names = port_names_temp.split(';')
                
                port_mags_temp = row['Amplitude']
                port_mags = port_mags_temp.split(';')
                
                port_phases_temp = row['Phase']
                port_phases = port_phases_temp.split(';')
                
                mag_phase_dict = {}
                temp_dict = {}
                ports_dict = {}
                for n, port in enumerate(port_names):
                    all_ports.append(port)
                    mag_phase_dict={'mag':float(port_mags[n]),'phase':float(port_phases[n])}
                    ports_dict[port] = mag_phase_dict
                temp_dict['ports'] = ports_dict


                if 'Paired_With' in header:
                    beam_pair = int(row['Paired_With'])
                else:
                    beam_pair = -1
                temp_dict['Beam_Pair'] = beam_pair
                beamid = row['Beam_ID']
                
                #these are not required inputs, but they will be used if
                #provided
                if 'Module_Name' in header:
                    module = row['Module_Name']
                    temp_dict['Module_Name'] = module
                    
                #if Prad_Renorm is provided, it will always be used and will
                #override any other user settings in the GUI
                if 'Prad_Renorm' in header:
                    renorm = row['Prad_Renorm']
                    temp_dict['Prad_Renorm'] = float(renorm)
                    
                beamid = int(row['Beam_ID'])
                vector_dict[beamid] = temp_dict

        self.port_names_in_codebook = list(set(all_ports))
        self.input_vector = vector_dict
        self.beam_ids = sorted(self.input_vector.keys())

        #list of all beams that are unique, if a beam has a beam pair, no need to calculate
        #PD again for the second time it shows up in the list. For example if
        #beam 1 is paired with beam 8. Then we only need to add the fields for
        #beam1 and beam 8, and store it under beam 1. When beam 8 shows up again
        #in the codebook, we will just ignore it. This assumes that all beams
        #and pairs are reciprocal
        self.unique_beams = list(self.input_vector.keys()) #start with all beams
        for idx in self.unique_beams:
            pair_idx = self.input_vector[idx]['Beam_Pair']
            if pair_idx!=-1:
                if pair_idx in self.unique_beams:
                    self.unique_beams.remove(pair_idx)


        self.aedtapp = aedtapp
        path, filename = os.path.split(file_name)
        filename = filename.replace(".csv","")
        self.name = filename

    def build_edit_sources_array(self,name_array,mag_array,phase_array):
        '''
        Builds an array that is used as in input into HFSS edit sources. The 
        input if baseically an array of value for each port and corropsonding
        mag and phase for each beam id

        Parameters
        ----------
        name_array : list of string
            all port names in desgin.
        mag_array : TYPE
            all magnitudes for each port (can be an expression).
        phase_array : TYPE
            all magnitudes for each port (can be an expression)..

        Returns
        -------
        TYPE
            array in format required by HFSS.

        '''
        # ToDo, add port terminal name to port name mapping so you can use
        # the same port name for codebooks in driven terminal and modal
        solution_type = self.aedtapp.odesign.GetSolutionType()
        sources =[]
        if solution_type == 'DrivenTerminal':
            sources.append(["UseIncidentVoltage:=", True,
                "IncludePortPostProcessing:=", False,"SpecifySystemPower:=", False])
        else:
            sources.append(["IncludePortPostProcessing:=", False,"SpecifySystemPower:=", False])
        
        valid_codebook =True
        if not self.port_check(): #codebook is not valid, will try to import valid port and ignore the rest
            valid_codebook =False
            
        self.port_names_in_codebook
        if not valid_codebook:#modify ports from codebook to only include ones that exist in the design
            name_array = list(set(self.all_ports_in_design).intersection(self.port_names_in_codebook))
                
        for count, excite in enumerate(name_array):
            sources.append(["Name:=", excite,"Magnitude:=", 
                str(mag_array[count]),"Phase:=", str(phase_array[count]) ])
        self.edit_sources_array = sources
        return self.edit_sources_array 
        
        
    def edit_sources(self,edit_sources_array):
        '''
        Sets the edit sources values in HFSS based on the array
        Parameters
        ----------
        edit_sources_array : Array
            Array in the format expected by HFSS for edit sources. 

        Returns
        -------
        None. Sets edit source in HFSS

        '''
        # ToDo, add port terminal name to port name mapping so you can use
        # the same port name for codebooks in driven terminal and modal
        oModule = self.aedtapp.odesign.GetModule("Solutions")
        oModule.EditSources(edit_sources_array)

    def add_dataset(self,name,data):
        '''
        Adds a data set in HFSS. If a data set already exists, it will first
        delete it, then add it

        Parameters
        ----------
        name : str
            name of data set to be created or edited.
        data : 2d list
            values used in data set.

        Returns
        -------
        None.

        '''
        
        oDesign = self.aedtapp.odesign

        temp_data = ["NAME:Coordinates"]
        for each in data:
            temp_data.append(["NAME:Coordinate","X:=", float(each[0]),"Y:=",
                float(each[1])])        
        ds = ["NAME:"+ name,temp_data]
    
        if oDesign.HasDataset(name) == True:
            oDesign.EditDataset(name,ds)
        else:
            oDesign.AddDataset(ds)

    def add_or_edit_variable(self,name,value,description = "variable used for post processing",hidden = False):
        '''
        Add or edit an existing variable POST PROCESSING variable  to HFSS. 
        If a variable does not exist, it will be created. If it does it will
        only modify the value. 

        Parameters
        ----------
        name : str
            name of variable to be added or edited.
        value : str or float
            value to set variable to. this can be an expression or a value.
        description : str, optional
            If a text description should be added to the variable.
            The default is "variable used for post processing".
        hidden : boolean, optional
            This variable can be hidden from users and only displayed
            in the detailed view of variables. The default is False.

        Returns
        -------
        None.

        '''
        oDesign = self.aedtapp.odesign
        pp_vars = oDesign.GetPostProcessingVariables()
        if name in pp_vars:
            oDesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:LocalVariableTab",
                        [
                            "NAME:PropServers", 
                            "LocalVariables"
                        ],
                        [
                            "NAME:ChangedProps",
                            [
                                "NAME:"+name,
                                "Value:="        , str(value)
                            ]
                        ]
                    ]
                ])
        else:
            oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", 
                        "LocalVariables"
                    ],
                    [
                        "NAME:NewProps",
                        [
                            "NAME:"+name,
                            "PropType:="        , "PostProcessingVariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(value)
                        ]
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:"+name,
                            "Description:="        , description
                        ],
                        [
                            "NAME:"+name,
                            "Hidden:="        , hidden
                        ]
                    ]
                ]
            ])
    def port_check(self,correct_port_names=True):
        '''
        Call this function to check if port names in codebook exist in the design
        
        I will eventually modify this so that it can correct port names in cases
        where things like a port is named 1:<mode_num> or when terminal names
        are used instead of the port name
        
        Parameters
        ----------
        correct_port_names : bool
            apply port corrections if needed.

        Returns
        -------
        None.
        '''


        ports_in_design = self.aedtapp.get_all_sources()
        valid_port = True
        ports_modified = []
        for port in self.port_names_in_codebook:
            if port not in ports_in_design:
                #print('check port names in codebook:')
                print('WARNING: codebook contains port ' + port + ', and it is not included in the design')
                beams = self.input_vector.keys()
                for beam in beams: #remove any keys that don't exist in codebook
                    del(self.input_vector[beam]['ports'][port])
                valid_port=False
            else:
                ports_modified.append(port)
        if not valid_port:
            #actual port names between codebook and in design are not correct
            #modifying the port names so they don't get used
            self.port_names_in_codebook  = ports_modified
            print('*******************************************************************')
            print('*******************************************************************')
            print('*******************************************************************')
            print('* ')
            print(' WARNING: codebook is not valid, attempting to only excite ports that exists in the design')
            print(' VERIFY CODEBOOK!')
            print('* ')
            print('*******************************************************************')
            print('*******************************************************************')
            print('*******************************************************************')
            if len(self.port_names_in_codebook)==0:
                print('Ports in codebook do not exist in design')
                sys.exit()
            return False
        else:
            return True
            print('Codebook is Valid')
        

    
    def codebook_import(self,update_datasets=True,update_editsources=True,use_beam_pair=True):

        """
        Import codebook
        codebook defines mag/phase for each port when user selects corrosponding
        beam id number. Will also include mag/phase for beam pairs. If a beam
        pair does not exist (single beam) this should be indicated by using a beam
        pair =-1 in the codebook
        
        Parameters
        ----------
        update_datasets : bool, optional
            If datasets already exists, we can update them or leave them as they are 
            defined. The default is True.
        update_editsources : bool, optional
            Update edit sources to current values. This can be used to prevent
            mulitple updates to the edit sources when nothing else has changed.
            The default is True.
        use_beam_pair : bool, optional
            Use only the single beam or the superposition of its main beam
            and the beam pair. The default is False.

        Returns
        -------
        None.
    
        returns controls that give mag/phase for each port for given beam id
        """


            
        self.all_ports_in_design = self.aedtapp.get_all_sources()

    
        #create lists of mag/phase across beam id's. 
        mag_2d_array = []
        phase_2d_array = []
        mag_2d_array_bp = []
        phase_2d_array_bp = []
        for n, id_num in enumerate(self.beam_ids):
            ports_in_beam_id = self.input_vector[id_num]['ports'].keys()
            beam_pair = self.input_vector[id_num]['Beam_Pair'] 
            mag_array = []
            mag_array_bp = []
            phase_array= []
            phase_array_bp = []
            for m, port in enumerate(self.all_ports_in_design):
                if port in self.input_vector[id_num]['ports'].keys():
                    mag_array.append(self.input_vector[id_num]['ports'][port]['mag'])
                    phase_array.append(self.input_vector[id_num]['ports'][port]['phase'])
                else:
                    mag_array.append(0.0)
                    phase_array.append(0.0)
                if beam_pair ==-1: #single beam, without beam pair
                    mag_array_bp.append(0.0)
                    phase_array_bp.append(0.0)
                else:
                    if port not in self.input_vector[beam_pair]['ports'].keys():
                        mag_array_bp.append(0)
                        phase_array_bp.append(0)
                    else:
                        mag_array_bp.append(self.input_vector[beam_pair]['ports'][port]['mag'])
                        phase_array_bp.append(self.input_vector[beam_pair]['ports'][port]['phase'])
        
            mag_2d_array.append(mag_array)
            phase_2d_array.append(phase_array)    
            mag_2d_array_bp.append(mag_array_bp)
            phase_2d_array_bp.append(phase_array_bp)
    
        oDesign = self.aedtapp.odesign
        pp_vars = oDesign.GetPostProcessingVariables()
        beam_id_var_name = "beamID"
        if beam_id_var_name not in pp_vars:
            self.add_or_edit_variable(beam_id_var_name,self.beam_ids[0],
                description = "beam ID for controlling array",hidden = False)
    
        beam_pair_phase_offset_varname = "BeamPair_PhaseOffset"
        if beam_pair_phase_offset_varname not in pp_vars:
            self.add_or_edit_variable(beam_pair_phase_offset_varname ,"0deg",
                description = "phase offset to apply to beam pair",hidden = False)
    
        use_beam_pair_varname = "UseBeamPair"
        if use_beam_pair_varname not in pp_vars:
            if use_beam_pair==True:
                self.add_or_edit_variable(use_beam_pair_varname,"true",
                    description = "boolearn to select if beam pair is used",hidden = False)
            else:
                self.add_or_edit_variable(use_beam_pair_varname,"false",
                    description = "boolearn to select if beam pair is used",hidden = False)

        
    
        mag_func_list = []
        phase_func_list = []
    
        mag_func_list_bp = []
        phase_func_list_bp = []
    
        #create datasets
        for n, port in enumerate(self.all_ports_in_design ):
            temp_mag=[]
            temp_phase=[]
            temp_mag_bp=[]
            temp_phase_bp=[]        
            for m, id_num in enumerate(self.beam_ids):
                temp_mag.append(mag_2d_array [m][n])
                temp_phase.append(phase_2d_array[m][n])
                temp_mag_bp.append(mag_2d_array_bp[m][n])
                temp_phase_bp.append(phase_2d_array_bp[m][n])
            if ":" in port:
                port = port.replace(":","_")
    
            name_mag = "ds_" + port + "_mag"
            name_phase = "ds_" + port + "_phase"
    
            name_mag_bp = "ds_" + port + "_mag_bp"
            name_phase_bp = "ds_" + port + "_phase_bp"
    
    
            # if update_datasets==True:
            #     if self.aedtapp.dataset_exists(name_mag):
            #         ds=zip(self.beam_ids,temp_mag)
            #         self.aedtapp.odesign.EditDataset(name_mag,ds)
            #     else:
            #         self.aedtapp.create_dataset1d_design(name_mag,self.beam_ids,temp_mag)
                                                                   

                
            #     self.aedtapp.create_dataset1d_design(name_phase,self.beam_ids,temp_phase)
            #     self.aedtapp.create_dataset1d_design(name_mag_bp,self.beam_ids,temp_mag_bp)
            #     self.aedtapp.create_dataset1d_design(name_phase_bp,self.beam_ids,temp_phase_bp)

            mag_ds = zip(self.beam_ids,temp_mag)
            mag_ds = sorted(mag_ds)
            phase_ds = zip(self.beam_ids,temp_phase)
            phase_ds = sorted(phase_ds)
    
            mag_ds_bp = zip(self.beam_ids,temp_mag_bp)
            mag_ds_bp = sorted(mag_ds_bp)
            phase_ds_bp = zip(self.beam_ids,temp_phase_bp)
            phase_ds_bp = sorted(phase_ds_bp)
    
            if update_datasets==True:
                self.add_dataset(name_mag,mag_ds)    
                self.add_dataset(name_phase,phase_ds)
                self.add_dataset(name_mag_bp,mag_ds_bp)    
                self.add_dataset(name_phase_bp,phase_ds_bp)
    
            #this is the full expression needed for the edit sources
            #ang_deg(pwl(ds_2_mag, beamID)*exp(cmplx(0, pwl(ds_2_phase, beamID))) + pwl(ds_2_mag_bp, beamID)*exp(cmplx(0,BeamPair_PhaseOffset*pi/180deg + pwl(ds_2_phase_bp, beamID)*pi/180)))
    
    
            mag_beam_pair_ds_string_beam1 = ('pwl('+ name_mag + ',' + beam_id_var_name 
                +')*exp(cmplx(0,pwl('+ name_phase + ',' + beam_id_var_name +')*pi/180))')
            mag_beam_pair_ds_string_beam2 = ('pwl('+ name_mag_bp + ',' + beam_id_var_name 
                +')*exp(cmplx(0,'+ beam_pair_phase_offset_varname+ '*pi/180deg+pwl('
                +name_phase_bp+ ',' + beam_id_var_name +')*pi/180))')
    
            full_bp_string = mag_beam_pair_ds_string_beam1 +'+'+ mag_beam_pair_ds_string_beam2
            mag_bp_string = 'mag(' + full_bp_string + ')'
            ang_bp_string = 'ang_deg(' + full_bp_string + ')'
    
            mag_no_beam_pair_ds_string = 'pwl('+ name_mag + ',' + beam_id_var_name + ')'    
            phase_no_beam_pair_ds_string = 'pwl('+ name_phase + ',' + beam_id_var_name + ')'
            mag_func_list.append('if(' +use_beam_pair_varname + ','
                +mag_bp_string + ','
                +mag_no_beam_pair_ds_string + ')')
            #result is still in radians
            phase_func_list.append('180deg/pi*if(' +use_beam_pair_varname + ','
                +ang_bp_string + ','
                +phase_no_beam_pair_ds_string + '*1deg)')    
    
        #used to troubleshoot complex expressions used in edit sources
        # File_to_Write = open('C:\\Users\\asligar\\Desktop\\delete\\testoutput', "w+")
        # for line in mag_func_list:
        #     File_to_Write.writelines(line)
        #     File_to_Write.writelines('\n')
        # File_to_Write.close()        
    
            #mag_func_list.append('pwl('+name_mag + ',' + beam_id_var_name + ')')
            #phase_func_list.append('pwl('+name_phase + ',' + beam_id_var_name + ')')
    
        edit_sources_array = self.build_edit_sources_array(self.all_ports_in_design,mag_func_list,phase_func_list)
        if update_editsources==True:    
            self.edit_sources(edit_sources_array)
    
    



