# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:50:47 2021

@author: asligar
"""
import numpy as np
import time as walltime



class Load_FF_Fields():
    '''
    Load and compute near field data as defined in the codebook through superpostion
    of the individual near field values for each port. Scaled by mag/phase
    '''
    def __init__(self,ffd_dict):
        '''
        
        Loads all the near fields into memory.
        
        Parameters
        ----------
        nfd_files_dict : dict
            dictionary of all near field files, with key=port name.
        length : float
            size of near field rectangle, this will coorponds to the x-axis. of
            the local CS used in HFSS to reference the near field surface
        width : float
            size of near field rectangle, this will coorponds to the y-axis. of
            the local CS used in HFSS to reference the near field surface
        length_n : int
            number of points in the near field rectangle.
        width_n : int
            number of points in the near field rectangle..

        Returns
        -------
        None.
        creates a dictionary of (data_dict) of near field values and positions
        for each port

        '''
        self.data_dict = {}


        all_ports = list(ffd_dict.keys())
        with open(ffd_dict[all_ports[0]], 'r') as reader:
            theta=[int(i) for i in reader.readline().split()] 
            phi=[int(i) for i in reader.readline().split()]
            num_freq=int(reader.readline().split()[1])
            frequency=float(reader.readline().split()[1])
        reader.close()
        results_dict = {}
        for port in ffd_dict.keys():
            if ':' in port:
                port = port.split(':')[0]
            temp_dict = {}
            theta_range=np.linspace(*theta)
            phi_range= np.linspace(*phi)
            
            ntheta=len(theta_range)
            nphi=len(phi_range)
            
            eep_txt=np.loadtxt(ffd_dict[port], skiprows=4)
            Etheta=np.vectorize(complex)(eep_txt[:,0], eep_txt[:,1])
            Ephi=np.vectorize(complex)(eep_txt[:,2], eep_txt[:,3])
            
            #eep=np.column_stack((etheta, ephi))  
            
            temp_dict['Theta']=theta_range
            temp_dict['Phi'] = phi_range
            temp_dict['rETheta']=Etheta
            temp_dict['rEPhi']=Ephi
            
            self.data_dict[port]=temp_dict
            
        #differential area of sphere, based on observation angle
        self.d_theta = np.abs(theta_range[1]-theta_range[0])
        self.d_phi = np.abs(phi_range[1]-phi_range[0])
        self.diff_area=np.radians(self.d_theta)*np.radians(self.d_phi)*np.sin(np.radians(theta_range)) 
        self.num_samples = len(temp_dict['rETheta'])
        self.all_port_names = list(results_dict.keys())
        self.solution_type = 'DrivenModal'
        self.unique_beams = None
        
        self.renormalize = False
        self.renormalize_dB = True
        self.renorm_value= 1
    
    def combine_fields(self,vector,reshape=None,relative_phase_beam_id=0):
        '''
        Performs superposition of all the near fields based on the codebook
        values for mag/phase.

        Parameters
        ----------
        vector : dict
            dictionary that contains the input steering vector of each beam id.
            the vector include mag/phase of each port for each beam id
        reshape : list [m.n], optional
            The data is original in 1D format, rehsaping it base don teh number
            of samples in x and y reiction will make averaging easier to perform
            . The default is None.
        relative_phase_beam_id : float, optional
            If we wanted to include a relative phase offset between the main
            beam and its beam pair, we can set this here. In some instances, a 
            very conservative estimage of max PD is made by looking at the max
            PD even across all possible relative beam pair phases. The default is 0.

        Returns
        -------
        data_dict_combined: dict
            dictionary of returned field values after superposition. This inlcudes
            E, H and P along with the positions for each beam ID

        '''

        
        self.data_dict_combined = {}
        if self.unique_beams!=None:
            beams_to_eval = self.unique_beams
        else:
            beams_to_eval = list(vector.keys())
        for beam in beams_to_eval:#each key in the vector is the beam_id
            temp_dict = {}
            beam_total_field_etheta = np.zeros((self.num_samples),dtype='complex')
            beam_total_field_ephi = np.zeros((self.num_samples),dtype='complex')
            beam_pair_id = vector[beam]['Beam_Pair']
            ports_in_beam = list(vector[beam]['ports'].keys())
            
            port_weight_sum = 0
            for port in ports_in_beam: #load all the data for the ports
                port_weight_mag = vector[beam]['ports'][port]['mag']
                port_weight_phase = vector[beam]['ports'][port]['phase']*np.pi/180 #convert to radians
                port_weight_cmplx = np.sqrt(port_weight_mag)*np.exp(1j*port_weight_phase)
                beam_total_field_etheta +=  port_weight_cmplx*self.data_dict[port]['rETheta']
                beam_total_field_ephi +=  port_weight_cmplx*self.data_dict[port]['rEPhi']
                port_weight_sum +=np.sum(port_weight_mag)
            if beam_pair_id!=-1:
                ports_in_beam_pair = list(vector[beam_pair_id]['ports'].keys())
                for port in ports_in_beam_pair:
                    port_weight_mag = vector[beam_pair_id]['ports'][port]['mag']
                    port_weight_phase = vector[beam_pair_id]['ports'][port]['phase']*np.pi/180 #convert to radians
                    port_weight_phase  += relative_phase_beam_id*np.pi/180
                    port_weight_cmplx = np.sqrt(port_weight_mag)*np.exp(1j*port_weight_phase)
                    beam_total_field_etheta +=  port_weight_cmplx*self.data_dict[port]['rETheta']
                    beam_total_field_ephi +=  port_weight_cmplx*self.data_dict[port]['rEPhi']
                    port_weight_sum +=np.sum(port_weight_mag)
                    
            temp_dict['rEPhi'] = beam_total_field_ephi
            temp_dict['rETheta'] = beam_total_field_etheta
            temp_dict['rETotal'] = np.sqrt(np.power(np.abs(beam_total_field_ephi ),2)+np.power(np.abs(beam_total_field_etheta ),2))
            temp_dict['Theta'] = self.data_dict[port]['Theta']
            temp_dict['Phi']= self.data_dict[port]['Phi']
            temp_dict['nPhi'] = len(self.data_dict[port]['Phi'])
            temp_dict['nTheta'] = len(self.data_dict[port]['Theta'])

            if self.solution_type=='DrivenTerminal':
                pin=np.sum(np.power(np.abs(port_weight_sum),2))
            else:
                pin=np.abs(port_weight_sum)

            temp_dict['Pincident'] = pin
            real_gain = 2*np.pi*np.abs(np.power(temp_dict['rETotal'],2))/pin/377
            temp_dict['RealizedGain'] = real_gain
            temp_dict['RealizedGain_dB'] = 10*np.log10(real_gain)
            


            # if reshape:
            #     try:
            #         reshape_with_xyz=tuple(list(reshape)+[3]) #add third demineions which is [x,y,z]
            #         beam_total_field_e=np.reshape(beam_total_field_e,reshape_with_xyz)
            #         beam_total_field_h=np.reshape(beam_total_field_h,reshape_with_xyz)
            #         self.pos=np.reshape(self.pos,reshape_with_xyz)
            #         poynting = np.reshape(poynting,reshape_with_xyz)
            #     except:
            #         print('Unable to reshape fields, verify that field files are current and updated')
            self.data_dict_combined[beam] = temp_dict
        return self.data_dict_combined
    

    def get_one_type(self,all_beam_ff,qty='RealizedGain'):
        '''
        return only one type of data in a dictionary in the form dict[beam_id]
    
        '''
        
        new_order = {}
        for beam in all_beam_ff.keys():
            new_order[beam] = all_beam_ff[beam][qty]
            
        return new_order

    def get_max_for_each_beam(self,all_beam_ff,qty='RealizedGain'):
        '''
        from a dictionary of all PD across beam IDs, return the max value for
        each beam ID
        
        TODO also return the location of the max
        '''
        ff_max ={} 
        for beam_id in all_beam_ff.keys(): #for each beam id in all beam ids
            ff_max[beam_id] = np.nanmax(all_beam_ff[beam_id][qty])
            print('Max ' +  qty + ' Far for Beam ID ' + str(beam_id) + ': ' + str(ff_max[beam_id]))
        return ff_max
    
    def envelope_pattern(self,all_beam_ff,qty='RealizedGain'):
        # if qty!='':
        #     qtys = ['Renormalized_Val_Lin','Renormalized_Val_dB','RealizedGain','RealizedGain_dB']
        # else:
        #     qtys=[qty]



            
        ff_max_all_angles ={} 

        beam_ids = list(all_beam_ff.keys())
        num_beams = len(all_beam_ff.keys())
        temp_data = np.zeros((num_beams,self.num_samples))
        for n, beam_id in enumerate(all_beam_ff.keys()): #for each beam id in all beam ids
            temp_data[n] = np.abs(all_beam_ff[beam_id][qty])
        
        #each observation angle will be weighted by the area it represents
        #the ffd is a nested loop of Theta then Phi. So we calcualted the
        #area based on theta as self.diff_arra. Now just repeat it to be
        # a 1D array as long as there are phi values
        array_area = np.repeat(self.diff_area,all_beam_ff[beam_id]['nPhi'])
        #array_area2 = np.tile(self.diff_area,all_beam_ff[beam_id]['nPhi'])
            
        ff_max_all_angles[qty] = np.max(temp_data,axis=0)
        ff_max_all_angles['Beam_For_Max'] = np.argmax(temp_data,axis=0)
        ff_max_all_angles['Theta'] = all_beam_ff[beam_id]['Theta']
        ff_max_all_angles['Phi']= all_beam_ff[beam_id]['Phi']
        ff_max_all_angles['nPhi'] = all_beam_ff[beam_id]['nPhi']
        ff_max_all_angles['nTheta'] = all_beam_ff[beam_id]['nTheta']
        ff_max_all_angles['Beam_Ids'] = beam_ids
        ff_max_all_angles['Area'] = array_area
        
        sorted_data = sorted( zip(ff_max_all_angles[qty], ff_max_all_angles['Area']) ) 
        cdf_vals = []
        cdf_area = []
        total_area = 0
        for val, area in sorted_data:
            total_area +=area
            cdf_area.append(total_area)
            cdf_vals.append(val)
            
        cdf_area = np.array(cdf_area/total_area) #normalize due to discrete integration of area
        cdf_vals = np.array(cdf_vals)
        
        max_cdf_vals = np.max(cdf_vals)
        max_real_gain_db = np.max(10*np.log10(cdf_vals))
        
        if self.renormalize:
            if self.renormalize_dB:
                renormalize_lin =np.power(10,(self.renorm_value/10))
                cdf_vals_renorm = cdf_vals/max_cdf_vals*renormalize_lin
            else:
                cdf_vals_renorm = cdf_vals/max_cdf_vals*self.renorm_value
            ff_max_all_angles['CDF_Value_Renorm'] = cdf_vals_renorm

        
        ff_max_all_angles['CDF_Area'] = cdf_area
        ff_max_all_angles['CDF_Value'] = cdf_vals
        
        
        
        idx_where_max = np.argmax(ff_max_all_angles[qty])
        beam_for_max = beam_ids[ff_max_all_angles['Beam_For_Max'][idx_where_max]]
        print("Max " + qty + ": " + str(np.max(np.abs(ff_max_all_angles[qty]))))
        print("Max Occurs for Beam " + str(beam_for_max))
        return ff_max_all_angles
    
    
def envelope_pattern_all_jobs(all_jobs,qty='RealizedGain'):
    ff_max_all_angles ={} 
    
    num_jobs = len(all_jobs.keys())
    
    temp_all_data = []
    for job in all_jobs.keys():
        
        all_beam_ff = all_jobs[job]

        
        beam_ids = list(all_beam_ff.keys())
        num_beams = len(all_beam_ff.keys())

        theta_range = all_beam_ff[beam_ids[0]]['Theta']
        phi_range = all_beam_ff[beam_ids[0]]['Phi']
        d_theta = np.abs(theta_range[1]-theta_range[0])
        d_phi = np.abs(phi_range[1]-phi_range[0])
        
        diff_area=np.radians(d_theta)*np.radians(d_phi)*np.sin(np.radians(theta_range)) 
        
        num_samples = len(all_beam_ff[beam_ids[0]]['rETheta'])
        temp_data = np.zeros((num_beams,num_samples))
        for n, beam_id in enumerate(all_beam_ff.keys()): #for each beam id in all beam ids
        
            temp_data[n] = np.abs(all_beam_ff[beam_id][qty])
        
        if len(temp_all_data)==0:
            temp_all_data = temp_data
        else:
            temp_all_data = np.vstack((temp_all_data,temp_data))
        #each observation angle will be weighted by the area it represents
        #the ffd is a nested loop of PHi then theta. So we calcualted the
        #area based on theta as self.diff_arra. Now just repeat it to be
        # a 1D array as long as there are phi values
        array_area = np.repeat(diff_area,all_beam_ff[beam_id]['nPhi'])#this would be if it were nested in phi theta order
        #array_area2 = np.tile(self.diff_area,all_beam_ff[beam_id]['nPhi']) #this would be if it were nested in theta phi order

    
    ff_max_all_angles[qty] = np.max(temp_all_data,axis=0)
    ff_max_all_angles['Theta'] = all_beam_ff[beam_id]['Theta']
    ff_max_all_angles['Phi']= all_beam_ff[beam_id]['Phi']
    ff_max_all_angles['nPhi'] = all_beam_ff[beam_id]['nPhi']
    ff_max_all_angles['nTheta'] = all_beam_ff[beam_id]['nTheta']
    ff_max_all_angles['Area'] = array_area
    
    sorted_data = sorted( zip(ff_max_all_angles[qty], ff_max_all_angles['Area']) ) 
    cdf_vals = []
    cdf_area = []
    total_area = 0
    for val, area in sorted_data:
        total_area +=area
        cdf_area.append(total_area)
        cdf_vals.append(val)
        
    cdf_area = np.array(cdf_area/total_area) #normalize due to discrete integration of area
    cdf_vals = np.array(cdf_vals)
    
    ff_max_all_angles['CDF_Area'] = cdf_area
    ff_max_all_angles['CDF_Value'] = cdf_vals
    

    print("Max " + qty + ": " + str(np.max(np.abs(ff_max_all_angles[qty]))))

    return ff_max_all_angles

