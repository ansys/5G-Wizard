
# -*- coding: utf-8 -*-

"""
      Written by : Arien Sligar (arien.sligar@ansys.com)
      Last updated : 12.09.2019

    incldues all functions that are related to         
"""


import numpy as np
import os
import Lib.Utillities as utils

class NearField_Utils():
    '''
    Various function used to extract near field from HFSS. Including creating
    a near field setup, extracting size of near field setup, and export fields
    '''
    def __init__(self,aedtapp):
        self.aedtapp= aedtapp
        
    def create_cs_sheet_center(self,sheet_name,cs_name="nearfield_cs",overwrite_existing=True):

        
        """
        This uses the built in function in HFSS to create an object CS
        I am creating this so it is centered on the rectangle and oriented so 
        X and Y direction are in teh plane of the rectangle based on edge lengths
        
        Parameters
        ----------
        sheet_name : str
            The name of the user defined sheed object that near fields should be based on.
        cs_name : str, optional
            The name to use, this doesn't really matter and any name can be used.
            The default is "nearfield_cs".
        overwrite_existing : bool, optional
            Mainly for testing, but if a user has already exported the fields,
            we can just use the existing fields if they want to change something
            only in the post processing. The default is True.

        Returns
        -------
        str
            return the name of the CS used. 
    
        add the properties for cs_name,length,width,norm_unitvec,units
        """
        oDesign = self.aedtapp.odesign
        oEditor = oDesign.SetActiveEditor("3D Modeler")
    
        object_id = oEditor.GetObjectIDByName(sheet_name)
        face_id = oEditor.GetFaceIDsOfSheet(sheet_name)
        face_id =face_id[0] #should only be 1 face
    

        self.aedtapp.modeler.set_working_coordinate_system('Global')
    
        units = oEditor.GetModelUnits()
        edge_IDs = oEditor.GetEdgeIDsFromObject(sheet_name) 
    
        face_center = oEditor.GetFaceCenter(face_id)
        #face_center = [ ConvertUnits(float(x),model_units,"meter") for x in face_center ]
    
        edge_lengths =[] 
        for edge in edge_IDs:
            edge_lengths.append(oEditor.GetEdgeLength(edge))
        edge_ids_and_length = zip(edge_lengths,edge_IDs)
    
        if len(set(edge_lengths)) <= 1: #this means it is a square
            short_edge_id = edge_IDs[0] #assigning first edge to just be the short edge
            short_edge_length= oEditor.GetEdgeLength(short_edge_id )
            width = short_edge_length 
            short_edge_vert_ids = oEditor.GetVertexIDsFromEdge(short_edge_id)
            id_index=1
            adjacent_edge=False
            while adjacent_edge==False:
                vert_ids = oEditor.GetVertexIDsFromEdge(edge_IDs[id_index])
                #check to see if an edge shares a vertex id with another edge
                #if it does, it is an adjacent edge
                adjacent_edge = any(item in short_edge_vert_ids for item in vert_ids)
                if adjacent_edge: 
                    long_edge_id = edge
                    long_edge_length= oEditor.GetEdgeLength(long_edge_id )
                    length = long_edge_length
                id_index+=1
        else:
            short_edge_length = np.min(edge_lengths)
            short_edge_id = edge_IDs[np.argmin(edge_lengths)]
            long_edge_length = np.max(edge_lengths)
            long_edge_id = edge_IDs[np.argmax(edge_lengths)]
            width = short_edge_length 
            length = long_edge_length 

    
        #get normal vector
        vert_ids_short = oEditor.GetVertexIDsFromEdge(short_edge_id)    
        vert_ids_long = oEditor.GetVertexIDsFromEdge(long_edge_id)    
        origin_index = list(set(vert_ids_short).intersection(vert_ids_long))
    
        short_endpoint_id = [x for x in vert_ids_short if x != origin_index[0] ]
        long_endpoint_id = [x for x in vert_ids_long if x != origin_index[0] ]
    
        origin_pos = oEditor.GetVertexPosition(origin_index[0])
        origin_pos = [float(i) for i in origin_pos]
        short_endpoint_pos = oEditor.GetVertexPosition(short_endpoint_id[0])
        short_endpoint_pos = [float(i) for i in short_endpoint_pos]
        long_endpoint_pos = oEditor.GetVertexPosition(long_endpoint_id[0])
        long_endpoint_pos= [float(i) for i in long_endpoint_pos]
    
    
        short_vec = np.array([
            short_endpoint_pos[0]-origin_pos[0],
            short_endpoint_pos[1]-origin_pos[1],
            short_endpoint_pos[2]-origin_pos[2]])
    
        short_vec_mag = np.linalg.norm(short_vec)
        short_unitvector = short_vec/short_vec_mag
        x_vector = short_unitvector #just using short axis of surface as x and long as y
    
        long_vec = np.array([
            long_endpoint_pos[0]-origin_pos[0],
            long_endpoint_pos[1]-origin_pos[1],
            long_endpoint_pos[2]-origin_pos[2]])
    
        long_vec_mag = np.linalg.norm(long_vec)    
        long_unitvector = long_vec/long_vec_mag
        y_vector = long_unitvector #just using short axis of surface as x and long as y
        
        #calculate surface normal unit vector
        norm_unitvec_1 = np.cross(short_unitvector,long_unitvector)
        norm_unitvec_2 = np.cross(long_unitvector,short_unitvector)
        face_center_vec = np.array(face_center,dtype='float')
        
        #this unit vector may point in or outward,
        #this should always  point away from global origin
        #checking which face center vector + normal vector is larger
        #larger distance means that is the direction pointing away from origin
        dist_norm1 = np.linalg.norm(face_center_vec+norm_unitvec_1)
        dist_norm2 = np.linalg.norm(face_center_vec+norm_unitvec_2)
        if dist_norm1>dist_norm2:
            norm_unitvec = norm_unitvec_1
        else:
            norm_unitvec = norm_unitvec_2


        
        exisiting_cs = oEditor.GetCoordinateSystems()
    
        if (overwrite_existing and cs_name in exisiting_cs):
            oEditor.ChangeProperty(
                [
                    "NAME:AllTabs",
                [
                    "NAME:Geometry3DCSTab",
                [
                    "NAME:PropServers", 
                    cs_name
                ],
                [
                    "NAME:ChangedProps",
                [
                    "NAME:Origin",
                    "X:="            , str(face_center[0]) + units,
                    "Y:="            , str(face_center[1]) + units,
                    "Z:="            , str(face_center[2]) + units
                ],
                [
                    "NAME:X Axis",
                    "X:="            ,str(x_vector[0])+ units,
                    "Y:="            , str(x_vector[1])+ units,
                    "Z:="            , str(x_vector[2])+ units
                ],
                [
                    "NAME:Y Point",
                    "X:="            , str(y_vector[0])+ units,
                    "Y:="            , str(y_vector[1])+ units,
                    "Z:="            , str(y_vector[2])+ units
                ]]]])
        else: #creates new CS with name increment
            original_cs_name = cs_name
            n=1
            while cs_name in exisiting_cs:
                cs_name = original_cs_name + "_" + str(n)
                n+=1
        
            oEditor.CreateRelativeCS(
                [
                    "NAME:RelativeCSParameters",
                    "Mode:="        , "Axis/Position",
                    "OriginX:="        , str(face_center[0]) + units,
                    "OriginY:="        , str(face_center[1]) + units,
                    "OriginZ:="        , str(face_center[2]) + units,
                    "XAxisXvec:="        , str(x_vector[0])+ units,
                    "XAxisYvec:="        , str(x_vector[1])+ units,
                    "XAxisZvec:="        , str(x_vector[2])+ units,
                    "YAxisXvec:="        , str(y_vector[0])+ units,
                    "YAxisYvec:="        , str(y_vector[1])+ units,
                    "YAxisZvec:="        , str(y_vector[2])+ units
                ], 
                [
                    "NAME:Attributes",
                    "Name:="        , cs_name
                ])


    

        self.aedtapp.modeler.set_working_coordinate_system(cs_name)
        self.cs_name = cs_name
        self.norm_unitvec = norm_unitvec
        self.y_vector = y_vector
        self.x_vector = x_vector
        self.length = length
        self.length_meter = utils.convert_units(length,units,'meter')
        self.width = width
        self.width_meter = utils.convert_units(width,units,'meter')
        self.units = units
        return self.cs_name
    
    def generate_nearfield_setup(self,nf_setup_name,cs_name,
                                 grid_size=1e-3,
                                 update_if_exists=True,
                                 use_true_size=True):
        
        '''
        Generate a near field setup on a rectangle defined by geo_name
        This will be the output of the near fields
     
        """

        Parameters
        ----------
        nf_setup_name : str
            DESCRIPTION.
        cs_name : str
            DESCRIPTION.
        grid_size : int, optional
            size of grid to be created. The default is 1e-3.
        update_if_exists : bool, optional
            If a near field setup already exist, just update it. If False, a
            new setup wil be created and the name will be incremented. 
            The default is True.
        use_true_size : bool, optional
            The original user defined rectangle may not align with an even number
            of grid points. Use this option to force the grid points to not extend
            beyone the user defined rectable if True. If False, the grid may extend 
            beyond the edge of the rectangle, forcing the number grid size to be
            as user specified, but the overall size of the sample area may be slighty
            larger than the user defined rectangle. The default is True.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        length_n = int(np.ceil(self.length_meter/grid_size)+1)
        width_n = int(np.ceil(self.width_meter/grid_size)+1)
        if use_true_size:
            actual_width = self.width_meter
            actual_length = self.length_meter
        else:
            actual_width = grid_size*(width_n-1)
            actual_length = grid_size*(length_n-1)


        if (("length" not in dir(self)) or ("width" not in dir(self))):
            print("create_cs_sheet_center() needs to be run before generate_nearfield_setup() can be run")
            return False
        oDesign = self.aedtapp.odesign
        oModule = oDesign.GetModule("RadField")
    
        self.length_n = length_n
        self.width_n = width_n
        self.actual_width = actual_width
        self.actual_length = actual_length
        
        existing_setups = oModule.GetSetupNames("Rectangle")
    
        if nf_setup_name in existing_setups:
            if update_if_exists==False:
                x=1
                orig_name = nf_setup_name
                while nf_setup_name in existing_setups:
                    nf_setup_name = orig_name +str(x)
                    x = x+1
    
                oModule.InsertNearFieldRectangleSetup(
                    [
                        "NAME:"+nf_setup_name,
                        "UseCustomRadiationSurface:=", False,
                        "Length:="        , str(self.actual_width) ,
                        "Width:="        , str(self.actual_length),
                        "LengthSamples:="    , int(width_n),
                        "WidthSamples:="    , int(length_n),
                        "CoordSystem:="        , cs_name
                    ])
            else:
                oModule.EditNearFieldRectangleSetup(nf_setup_name, 
                    [
                        "NAME:"+nf_setup_name,
                        "UseCustomRadiationSurface:=", False,
                        "Length:="        , str(self.actual_width),
                        "Width:="        , str(self.actual_length),
                        "LengthSamples:="    , int(width_n),
                        "WidthSamples:="    , int(length_n),
                        "CoordSystem:="        , cs_name
                    ])
        else:
            oModule.InsertNearFieldRectangleSetup(
                [
                    "NAME:"+nf_setup_name,
                    "UseCustomRadiationSurface:=", False,
                    "Length:="        , str(self.actual_width),
                    "Width:="        , str(self.actual_length),
                    "LengthSamples:="    , int(width_n),
                    "WidthSamples:="    , int(length_n),
                    "CoordSystem:="        , cs_name
                ])
        self.nf_setup_name = nf_setup_name
        return nf_setup_name
    
    def build_edit_sources_array(self,name_array,mag_array,phase_array):
        '''
        This is a repeated function from Codebook.py, 
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
            
        for count, excite in enumerate(name_array):
            sources.append(["Name:=", excite,"Magnitude:=", 
                str(mag_array[count]),"Phase:=", str(phase_array[count]) ])
        edit_sources_array =sources
        return edit_sources_array 
        
        
    def edit_sources(self,edit_sources_array):
        '''
        This is a repeated function from Codebook.py, 
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
        
    def export_all_nfd(self,nf_setup_name,ports,freq=None,setup_name="Setup1:LastAdaptive",export_path='./',overwrite=True):
        '''
        

        Parameters
        ----------
        nf_setup_name : str
            DESCRIPTION.
        ports : list
            DESCRIPTION.
        freq : str, optional
            DESCRIPTION. The default is None.
        setup_name : str, optional
            DESCRIPTION. The default is "Setup1:LastAdaptive".
        export_path : str, optional
            DESCRIPTION. The default is './'.
        overwrite : bool, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        dict or bool
            returns a dictionary with port names as keys for filename and path
            to the location of the nfd. If no fields exists it will return False

        '''
        oModule = self.aedtapp.odesign.GetModule("Solutions")
        has_fields = oModule.HasFields(setup_name,freq)
        nfd_files_dict = {}
        if has_fields:
            num_ports = len(ports)
            nfd_files = []
            for n, port in enumerate(ports):
                freq_str = str(freq/1e9) + "GHz"
                setup_name_str = setup_name.replace(':',"_")
                file_path = export_path+port +'_'+ freq_str + '_' + setup_name_str + '.nfd'
                does_file_exist= os.path.isfile(file_path)
                if (not does_file_exist or overwrite):
                    mag_array=[0]*num_ports
                    mag_array[n] = 1
                    phase_array=[0]*num_ports
                    name_array = ports
                    edit_sources_array = self.build_edit_sources_array(name_array,mag_array,phase_array)
                    self.edit_sources(edit_sources_array)
                    file_name = self.export_nfd(nf_setup_name,freq,setup_name,file_path)
                else:
                    file_name = file_path
                    print("Using existing nfd: "+ file_name)
                nfd_files_dict[port]=file_name
            return nfd_files_dict
        else:
            print("no fields exists")
            return False
    
    def export_nfd(self,nf_setup_name,freq,setup_name,file_name='./out.nfd'):
        '''
        exports NFD file on near field setup and returns the path name

        Parameters
        ----------
        nf_setup_name : str
            name of near field setup to extract data from.
        freq : str
            frequency to be exported. This frequency must be solved with fields
            saved within the setup to be exported. Typically a string like "28GHz"
        setup_name : str
            name in HFSS of the setup that is to be exported. For example this 
            shoudl be "Setup1:LastAdpative" or "Setup1:Sweep1" or whatever they
            are named in HFSS
        file_name : str, optional
            The name of the exported nfd file, this should ideally be set to
            easily identify which port and other setup information that the
            fields belong to. The default is './out.nfd'.

        Returns
        -------
        str
            path to file.

        '''
        
        if freq==None:
            print("setup requires a valid frequency point")
            return False

        path_directory = os.path.dirname(file_name)
        if not os.path.exists(path_directory):
            os.makedirs(path_directory)

        export_options =         [
            "ExportFileName:="    , file_name,
            "SetupName:="        , nf_setup_name
            ]
        variation_key1 = "IntrinsicVariationKey:="
        variation_key2 ="Freq=\'" + str(freq) + "\'"
        export_options.append(variation_key1)
        export_options.append(variation_key2)
        export_options.append("DesignVariationKey:=")
        export_options.append("")
        export_options.append("SolutionName:=")
        export_options.append(setup_name)

        oModule = self.aedtapp.odesign.GetModule("RadField")
        oModule.ExportRadiationFieldsToFile(export_options)
        
        print('NFD Exported: '+file_name)
        return file_name

