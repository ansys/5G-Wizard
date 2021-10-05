# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:50:47 2021

@author: asligar
"""
import numpy as np
import time as walltime



class Load_NF_Fields():
    '''
    Load and compute near field data as defined in the codebook through superpostion
    of the individual near field values for each port. Scaled by mag/phase
    '''
    def __init__(self,nfd_files_dict,length,width,length_n,width_n):
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
        
        #the positions output from the nfd format give values in global CS
        #it is easier to work with values in local CS, so calculating here
        pos = np.zeros((length_n*width_n,3))
        yy = np.linspace(-length/2,length/2,num=length_n)
        xx = np.linspace(-width/2,width/2,num=width_n)
        count=0
        for x in xx:
            for y in yy:
                pos[count][0]=x
                pos[count][1]=y
                pos[count][2]=0
                count+=1
                
        if nfd_files_dict!=None:
            self.data_dict = {}
    
            for port in nfd_files_dict.keys():
                file = nfd_files_dict[port]
                temp_dict = {}
    
                print('loading port: ' + port)
                data = np.loadtxt(file,skiprows=3,delimiter=',')
                #pos = data[:,1:4]
                #e_fields = data[:,4:10]
                #h_fields = data[:,10:16]
                
                e_field_x = 1j*data[...,5]; e_field_x += data[...,4]
                e_field_y = 1j*data[...,7]; e_field_y += data[...,6]
                e_field_z = 1j*data[...,9]; e_field_z += data[...,8]
                e_field = np.vstack((e_field_x,e_field_y,e_field_z)).T
                h_field_x = 1j*data[...,11]; h_field_x += data[...,10]
                h_field_y = 1j*data[...,13]; h_field_y += data[...,12]
                h_field_z = 1j*data[...,15]; h_field_z += data[...,14]
                h_field = np.vstack((h_field_x,h_field_y,h_field_z)).T
                
    
                temp_dict['pos']=pos
                temp_dict['E'] = e_field
                temp_dict['H']=h_field
                self.data_dict[port] = temp_dict
    
        self.pos = pos
        self.num_samples = len(pos)
        self.solution_type = 'DrivenModal'
        self.unique_beams = None
        self.renormalize = False
        self.prad= []
        self.renorm_values= []

        
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
            
        if self.renormalize:
            #if list of value check to see lenght of it, needs to be at least as long as num unique beams
            if isinstance(self.renorm_values, list): 
                if len(self.renorm_values)==0: 
                    print('Renormalzing value not given, not renormalizing')
                    self.renormalize=False
                elif len(self.renorm_values)>=len(beams_to_eval): #an array of renormalzing value is given
                    print('###############################################')
                    print('# Renormalzing Power/Poynting of all Beams')
                    print('###############################################')
                elif len(self.renorm_values)==1: #just adding in case someone enters a [] when defining a list of a single value
                    val = self.renorm_values[0]
                else: #just adding in case someone enters a [] when defining a list of a single value
                    print('Renormalzing value list is too short. List should be at least')
                    print(' as long as the number of unique beams, or a single value. NOT renormalizing')
                    self.renormalize=False
            else: #if a single value is given, turn it into a list of the same values
                val = self.renorm_values
                self.renorm_values = list(np.ones(len(beams_to_eval))*val)
            
        for n, beam in enumerate(beams_to_eval):#each key in the vector is the beam_id
            beam_total_field_e = np.zeros((self.num_samples,3),dtype='complex')
            beam_total_field_h = np.zeros((self.num_samples,3),dtype='complex')
            beam_pair_id = vector[beam]['Beam_Pair']
            ports_in_beam = list(vector[beam]['ports'].keys())
            for port in ports_in_beam: #load all the data for the ports
                port_weight_mag = vector[beam]['ports'][port]['mag']
                port_weight_phase = vector[beam]['ports'][port]['phase']*np.pi/180 #convert to radians
                port_weight_cmplx = np.sqrt(port_weight_mag)*np.exp(1j*port_weight_phase)
                beam_total_field_e +=  port_weight_cmplx*self.data_dict[port]['E']
                beam_total_field_h +=  port_weight_cmplx*self.data_dict[port]['H']
            if beam_pair_id!=-1:
                ports_in_beam_pair = list(vector[beam_pair_id]['ports'].keys())
                for port in ports_in_beam_pair:
                    port_weight_mag = vector[beam_pair_id]['ports'][port]['mag']
                    port_weight_phase = vector[beam_pair_id]['ports'][port]['phase']*np.pi/180 #convert to radians
                    port_weight_phase  += relative_phase_beam_id*np.pi/180
                    port_weight_cmplx = np.sqrt(port_weight_mag)*np.exp(1j*port_weight_phase)
                    beam_total_field_e +=  port_weight_cmplx*self.data_dict[port]['E']
                    beam_total_field_h +=  port_weight_cmplx*self.data_dict[port]['H']
            poynting = 0.5*np.cross(beam_total_field_e,beam_total_field_h.conjugate())
            
            if self.renormalize:
                print('Renormalizing Power/Poynting Vector of Beam ' + str(beam) + 
                      ' by ' + str(np.round(self.renorm_values[n]/self.prad[n],3)))
                print('New Radiated Power for Beam ' + str(beam) + ' : ' + str(self.renorm_values[n])+ 'W')
                poynting_1W = poynting/self.prad[n]
                poynting = poynting_1W*self.renorm_values[n]


            if reshape:
                try:
                    reshape_with_xyz=tuple(list(reshape)+[3]) #add third demineions which is [x,y,z]
                    beam_total_field_e=np.reshape(beam_total_field_e,reshape_with_xyz)
                    beam_total_field_h=np.reshape(beam_total_field_h,reshape_with_xyz)
                    self.pos=np.reshape(self.pos,reshape_with_xyz)
                    poynting = np.reshape(poynting,reshape_with_xyz)
                except:
                    print('Unable to reshape fields, verify that field files are current and updated')
            self.data_dict_combined[beam] = {'E':beam_total_field_e,'H':beam_total_field_h,'P':poynting,'pos':self.pos}
            
        print("Unique Beams: " + str(self.unique_beams) + ", including Beam Pairs with each unique beam")
        return self.data_dict_combined
    
    
    def get_PD_n_plus_local(self,pd,surface_normal):
        '''
        Get PD n plus as defined in spec as equation (4)

        Parameters
        ----------
        pd : TYPE
            DESCRIPTION.
        surface_normal : TYPE
            DESCRIPTION.

        Returns
        -------
        pd_n_plus : TYPE
            DESCRIPTION.

        '''
        pd_n_plus = {}
        for beam_id in pd.keys():
            pd_current = np.dot(np.real(pd[beam_id]['P']),surface_normal)
            pd_n_plus[beam_id]=np.squeeze(pd_current*np.heaviside(pd_current,0))
        return pd_n_plus
    def get_PD_tot_plus_local(self,pd,surface_normal):
        '''
        Get PD n plus as defined in spec as equation (5)

        Parameters
        ----------
        pd : TYPE
            DESCRIPTION.
        surface_normal : TYPE
            DESCRIPTION.

        Returns
        -------
        pd_n_plus : TYPE
            DESCRIPTION.

        '''
        pd_tot_plus = {}
        na = surface_normal
        for beam_id in pd.keys():
            rpd = np.real(pd[beam_id]['P'])
            arpd = np.atleast_3d(np.linalg.norm(rpd,axis=-1))
            nr=np.divide(rpd,arpd)
            #calculate xi
            xi = np.arccos(np.dot(nr,na))*180/np.pi
            #replace values less than 85deg with 1, values greater than 90with 0 and 1-(xi-85)/5 for 85<xi<90
            xi_conditioned =np.ones(xi.shape)
            xi_conditioned = np.atleast_3d(np.where(xi < 85, 1, np.where(xi > 90, 0,1-(xi-85)/5)))
            pd_tot_plus[beam_id]=np.squeeze(arpd*xi_conditioned)
        return pd_tot_plus
    
    def get_PD_mod_plus_local(self,pd,surface_normal):
        '''
        Get PD n plus as defined in spec as equation (8)

        Parameters
        ----------
        pd : TYPE
            DESCRIPTION.
        surface_normal : TYPE
            DESCRIPTION.

        Returns
        -------
        pd_n_plus : TYPE
            DESCRIPTION.

        '''
        pdntot =self.get_PD_tot_plus_local(pd,surface_normal)

        pd_mod_plus = {}
        for beam_id in pd.keys():
            ipd = np.atleast_3d(np.imag(pd[beam_id]['P']))
            aipd_square = np.atleast_3d(np.power(ipd[:,:,0],2)+np.power(ipd[:,:,1],2)+np.power(ipd[:,:,2],2))
            pd_mod_plus[beam_id] = np.squeeze(np.sqrt(np.power(np.atleast_3d(pdntot[beam_id]),2)+ aipd_square))
        return pd_mod_plus

    def get_PD_all_types(self,pd,surface_normal):
        
        pdnplus = self.get_PD_n_plus_local(pd,surface_normal)
        pdntot = self.get_PD_tot_plus_local(pd,surface_normal)
        pdnmodplus = self.get_PD_mod_plus_local(pd,surface_normal)
        
        return {'PD_n_plus':pdnplus,'PD_tot_plus':pdntot,'PD_mod_plus':pdnmodplus}



    def initialize_averaging_area(self):
        '''
        Gets all index values that fall within the averaging sq at each rotation
        of theta. Theta is steped from 0 to 85 degrees, assumes theta is 
        always an integer and creates integeger number of steps
        
        Returns
        -------
        list_idx_for_avg_sq : list of numpy arrays
            Index values that align fall within teh averaging sq for the specific
            rotation of the sq. Values are normalized to 0,0 so they need to be
            offset for current position
        '''
        self.list_idx_for_avg_sq = {}
        for step in range(0,90,self.theta_step):
            self.list_idx_for_avg_sq[step] = self.get_idxs_in_avg_square(self.area ,self.grid_size,step)

        return self.list_idx_for_avg_sq



    def average_pd(self,pd,area=.0001,grid_size=1e-3,theta_step=5):
        '''
        
        Parameters
        ----------
        pd : dict of arrays
            pd array of values.this should include all beam ids, and the average
            will be caluclated for each beam id 
        area : float, optional
            area of averaging rectangle, this may only ever need to be
            1cm^2 or 4cm^2, but can be defined by the user. The default is .0001.
        grid_size : float, optional
            size of grid spacing, this should be either 1mm or lambda/10 whichever
            is smaller. The default is 1e-3.
        theta_step : int, optional
            Steps size, in degrees, to rotate the averaging square, this should
            probably be always default. The default is 5.

        Returns
        -------
        p_avg_all_beams : TYPE
            DESCRIPTION.

        '''
        
        self.area = area
        self.grid_size = grid_size
        self.theta_step = theta_step
        list_idx_for_avg_sq = self.initialize_averaging_area()

        num_theta = int(90/theta_step)
        
        if num_theta < 18:
            print("Warning: size of theta averaging steps are less than 5deg, increase theta_step")

        edge_length = np.sqrt(self.area)
        diagnol_length = np.sqrt(2)*edge_length/2 #from center to corner
        

        xpos_n = self.pos.shape[0]
        ypos_n = self.pos.shape[1]
        xmin = np.min(self.pos[:,:,0])
        xmax = np.max(self.pos[:,:,0])
        ymin = np.min(self.pos[:,:,1])
        ymax = np.max(self.pos[:,:,1])
        
        theta_steps = 18
        p_avg_all_beams = {}

        if self.unique_beams!=None:
            beams_to_eval = self.unique_beams
        else:
            beams_to_eval = list(pd.keys())
        for beam_id in beams_to_eval: #for each beam id in all beam ids
            time_before_averaging = walltime.time()
            total_num_points_to_eval = pd[beam_id].shape[0]*pd[beam_id].shape[1]
            points_evaluated = 0
            print('Averaging Beam ID: ' + str(beam_id))
            p_avg = np.zeros((xpos_n,ypos_n))
            for x_idx in range(xpos_n): #step through each xpos
                if x_idx%20==0: #print display frequency
                    print('Points Evaluated: ' + str(points_evaluated) + ' of ' +  str(total_num_points_to_eval))
                for y_idx in range(ypos_n): #step through each y pos

                    points_evaluated+=1
                    cur_pos = self.pos[x_idx,y_idx][0:2] #get rid of z pos
                    
                    for theta in np.linspace(0,85,num=theta_steps): #search all rotations of averaging square for max
                        current_idx = np.array([x_idx,y_idx]) #current index value to calculate
                        #list_idx_for_avg_sq contains all possible index values that vall within the
                        #averaging square at the specified rotation
                        offsets_idx_to_eval = list_idx_for_avg_sq[theta] + current_idx #offset list_idx_for_avg_sq by current position

                        
                        #cehck if averaging square is within solution space
                        if (xmin <= cur_pos[0]-diagnol_length and xmax >= cur_pos[0]+diagnol_length and (ymin <= cur_pos[1]-diagnol_length and ymax >= cur_pos[1]+diagnol_length)):
                            
                            pd_local_in_sq = pd[beam_id][tuple(offsets_idx_to_eval.T)]
                            pd_current_avg = np.sum(pd_local_in_sq)/len(pd_local_in_sq)

                            if pd_current_avg>p_avg[x_idx,y_idx]:#orientaiton where sq results in largest pd
                                p_avg[x_idx,y_idx] = pd_current_avg
                        else: 
                            #if any point is outside of the solution space, exit the loop
                            p_avg[x_idx,y_idx] = np.nan
                            break
            time_after_averaging = walltime.time()
            time_to_average = time_after_averaging-time_before_averaging
            print('Averaging Calculation Time: ' + str(np.round(time_to_average,2)))
            p_avg_all_beams[beam_id] = p_avg
                                

        return p_avg_all_beams


    def get_idxs_in_avg_square(self,area,grid_size,theta):
        '''
        Because the IEEE spec calls for the maximum PD to be deterined for 
        a rotation of a square (0-85deg@5deg), and the fields are sampled on 
        a cartesian grid, we need to determine which points will lie within
        the square once it is rotated with respect to the cartesian grid
        
        This algorithm determines which points lie within the rotated sq, by:
        1) determine the maximum number of grid points that should be checked.
        This is based on the max size of the square, diagnal distance. The
        distance is converted to a maximum number of indecies away from the 
        point that is evaluated
        2) brute force check each point within this max distance to see if it lies 
        within the rotated square.
            a) To keep this simple, I am rotating the point in the opposite direction
              as the square is rotated, because it is very easy to determine that
              a point lies within a square that is oriented along the cartesian
              coordinates. 
            b) if the point lies within, store it into a list of tuples (m,n)
        
        There is rooom for improvment here, oen thing that I tried below, is 
        determine which points will always be inside averaging square and which ones
        will depend on the orientation. The max distance away from the center of the
        point evaluated will be the diagnol length
        
        I am not sure if this has any performance benifit...need to revisit to 
        improve performance, maybe it just overcomplicates and we could just 
        brute force all points

        Parameters
        ----------

        area : float
            area of averaging rectangle 
        grid_size : float
            size of grid field spacing to be averaged
        theta : float
            angle that the averaging square is rotated (in degrees).

        Returns
        -------
        list_of_idx_inside : array of indecies
            list of points that lie inside the averaging square for the user specified theta.
            These points are referecned to origin/index at 0,0. Resulting index
            values can be offset by current location later to evaluate pd average

        '''
            

        edge_length = np.sqrt(area)
        #this point woudl be the max distance away from the center point
        #when a rotation is added
        new_point = self.rotate([edge_length/2,edge_length/2],theta)
        max_distance = np.max(new_point)
        
        #the max distance will determine the maximum number of indecies to
        #check if they are inside or outside of the rotated square
        max_num_idx_for_avg_sq= int(np.floor(max_distance/grid_size))
        
        
        #full range of index value from center point to outer most points that
        #could land inside the averaging square when it is rotated to any angle
        idx_x_start= -max_num_idx_for_avg_sq
        idx_x_stop=  max_num_idx_for_avg_sq
        idx_y_start= -max_num_idx_for_avg_sq
        idx_y_stop= max_num_idx_for_avg_sq
        

        #extents of averaging square when not rotated. becuase we are not rotating
        #the square, but rotating points to see if they would end up inside a
        #cartesian oriented square
        current_origin = [0,0]
        avg_area_x_min = -edge_length/2
        avg_area_x_max = edge_length/2
        avg_area_y_min = -edge_length/2
        avg_area_y_max = edge_length/2

        #full possible range of values
        idx_of_points_to_eval_x = range(idx_x_start,idx_x_stop+1)
        idx_of_points_to_eval_y = range(idx_y_start,idx_y_stop+1)
        list_of_idx_inside = []
        #check each potential point if it is inside the rotated averaging sq
        for x in idx_of_points_to_eval_x:
            for y in idx_of_points_to_eval_y:
                #check if rotated point is inside square
                test_pos = x*grid_size,y*grid_size
                #doing this in reverse beccause it is easy to check if point
                #is inside a square based on min/max values of a square that is 
                #aligned with a cartesian grid  So rotating points backwards to see if they 
                #woudl be in a non-rotated sq
                rotated_point = self.rotate(test_pos,-theta,current_origin)
                if (avg_area_x_min <= rotated_point[0] and avg_area_x_max >= rotated_point[0] and (avg_area_y_min <= rotated_point[1] and avg_area_y_max >= rotated_point[1])):
                    list_of_idx_inside.append([x,y])

        return np.array(list_of_idx_inside)

    def rotate(self,  point, theta,origin=[0,0],in_deg=True):
        """
        Rotate a point counterclockwise by a given angle around a given origin.
    
        The angle should be given in radians.
        """
        if in_deg:
            theta=np.deg2rad(theta)
        ox, oy = origin
        px, py = point
    
        qx = ox + np.cos(theta) * (px - ox) - np.sin(theta) * (py - oy)
        qy = oy + np.sin(theta) * (px - ox) + np.cos(theta) * (py - oy)
        return [qx, qy]


    def get_max_for_each_beam(self,all_beam_pd,label=''):
        '''
        from a dictionary of all PD across beam IDs, return the max value for
        each beam ID
        
        TODO also return the location of the max
        '''
        pd_max ={} 
        for beam_id in all_beam_pd.keys(): #for each beam id in all beam ids
            pd_max[beam_id] = np.nanmax(all_beam_pd[beam_id])
            print('Max PD for Beam ID ' + str(beam_id) + ': ' + str(pd_max[beam_id]) + ' ' + label)
        return pd_max
    
