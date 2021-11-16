# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:02:31 2021

@author: asligar

inculdes some simple functions that are used for various tasks

"""
import h5py
import numpy as np
import os
import datetime
import json
import csv

def round_time(dt=None, roundTo=1):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
             
def write_csv(data,path='./out.csv',sort_by_pd=False):
    #headings = list(data.keys()) 
    #these heading should always exist
    headings = ['BeamId','Module_Name','PD_Type','EvalSurface','Freq','Averaging_Area','PD_Max','RadiatedPower','Renormalized PD']
    beam_ids = list(data['PD_Max'].keys())
    data['BeamId'] = beam_ids
    #headings.append('BeamId')
    #remove some headings we don't want to output in csv file
    #headings = list(filter(('Paths_To_Raw_Data').__ne__, headings))
    #headings = list(filter(('Paths_To_Avg_Data').__ne__, headings))

    all_rows = []
    if sort_by_pd:
        pd_max_as_list = list(data['PD_Max'].values())
        original_index_vals = list(range(len(beam_ids)))
        zipped = zip(pd_max_as_list,data['BeamId'],original_index_vals)
        sort_zip = list(sorted(zipped,reverse=True))
        for s in sort_zip:
            row_data = []
            for head in headings:
                cell_data= data[head]
                #cell data may be dict, list or single value
                if isinstance(cell_data, list):
                    cell_data=str(cell_data[s[2]])
                elif isinstance(cell_data, dict):
                    cell_data = str(cell_data[s[1]])
                else:
                    cell_data= str(cell_data)
                row_data.append(cell_data)
            all_rows.append(row_data)
    else:
        for n, beam in enumerate(beam_ids):
            row_data = []
            for head in headings:
                cell_data = data[head]
                #cell data may be dict, list or single value
                if isinstance(cell_data, list):
                    cell_data=str(cell_data[n])
                elif isinstance(cell_data, dict):
                    cell_data = str(cell_data[beam])
                else:
                    cell_data= str(cell_data)
                row_data.append(cell_data)
            all_rows.append(row_data)


    with open(path, 'w',newline='') as csvfile: 

        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(headings) 
        csvwriter.writerows(all_rows)

def dict_with_numpy_to_lists(input_dict):
    '''
    convert a dictionary with numpy arrays to list so they can be dumped to 
    json file. This is tempoarary, works with 2 levels of nested dictionaries.
    

    '''
    for level1 in input_dict.keys():
        if isinstance(input_dict[level1], np.ndarray):
            input_dict[level1] = input_dict[level1].tolist()
        elif isinstance(input_dict[level1], dict):
            for level2 in input_dict[level1].keys():
                if isinstance(input_dict[level1][level2], np.ndarray):
                    input_dict[level1][level2] = input_dict[level1][level2].tolist()
                    
    return input_dict
    

def write_dictionary_to_json(path='./out.json',dict_to_write=None):
    if dict_to_write:
        with open(path,'w',encoding='utf-8') as f:
            json.dump(dict_to_write,f,indent=4)                     

def write_line_to_text(path='./out.txt',line='',close_file=False):
    f = open(path, "a")
    f.write(line + '\n')
    if close_file:
        f.close()

def write_out_fields_2levels(name='out',output_path='/',data = None,qty=''):
    '''
    exports data to hdf5 format. The input data is assuemd to be a dictionary
    of dictionaries. That is why it is callued _2levels. The dictionary would
    have the format looking something like
    
    dict[beam_id][qty]=values. Where beam id is the integer beam id value and
    qty would be any field values stored in that dictionary. The typical format
    would include 'H' 'P' and 'E'

    Parameters
    ----------
    name : str
        name of file to be saved, no including the extension.
    output_path : str
        path whwere data should be saved. include trailing \\
    data : dict
        dictionary of values to be exported
    freq : str
        string of frequency value, will be appended to file name to make it clear
        what solution this is part of
        
    Returns
    -------
    list of files exported
    '''
    
    files_dict_all_beams = {}

    
    output_path = output_path + 'hdf5/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
   
    for beamid, fields in data.items():
        files_dict_one_beam = {}
        for key, values in fields.items():
            file_name = output_path+'Beamid_' + str(beamid) + '_QTY-' +str(key) + '.hdf5'
            h = h5py.File(file_name,'w')
            h.create_dataset( file_name, data=np.array(values, dtype='complex'))
            h.close()

            files_dict_one_beam[str(key)] = file_name
        files_dict_all_beams[beamid] = files_dict_one_beam
    return files_dict_all_beams
            
def write_out_fields_1level(name='out',output_path='/',data = None,qty=''):
    '''
    exports data to hdf5 format. The input data is assuemd to be a dictionary
    of values. That is why it is callued _1level. The dictionary would
    have the format looking something like
    
    dict[beam_id]=values. Where beam id is the integer beam id value. This format
    usually comes from the average value calculation for PD

    Parameters
    ----------
    name : str
        name of file to be saved, no including the extension.
    output_path : str
        path whwere data should be saved. include trailing \\
    data : dict
        dictionary of values to be exported
    freq : str
        string of frequency value, will be appended to file name to make it clear
        what solution this is part of
    qty : str
        name that is appended to exported data to make it clear which data
        is saved within the file
        
    Returns
    -------
    list of files exported
    '''
    files_dict_all_beams = {}

    output_path = output_path + 'hdf5/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
   
    for beamid, fields in data.items():
        files_dict_one_beam = {}
        file_name = output_path+'Beamid_' + str(beamid) + '_QTY-' + qty + '.hdf5'
        h = h5py.File(file_name,'w')
        h.create_dataset( file_name, data=np.array(fields, dtype='float'))
        h.close()
        files_dict_one_beam[qty] = file_name

        files_dict_all_beams[beamid] = files_dict_one_beam
    return files_dict_all_beams
        
def convert_units(value, oldUnits='', newUnits=''):
    '''
    convineince function to convert values from one unit to another unit
    if units contain units^2 or units2 it will assume square units and convert 
    
    Parameters
    ----------
    value : float or str
        value to be converted.If units are included, function will attempt
        to parse units from string
    oldUnits : str
        original units.
    newUnits : str
        destination units to convert into.

    Returns
    -------
    nuValue : float
        output value in new units.

    '''
    
    is_square_units = False
    if '^' in oldUnits:
        oldUnits =oldUnits.replace('^','')
    if '^' in newUnits:
        newUnits =newUnits.replace('^','')
    if ('2' in oldUnits or '2' in newUnits):
        oldUnits = oldUnits.replace('2','')
        newUnits = newUnits.replace('2','')
        is_square_units=True
    
    #if user passes in a string
    if isinstance(value, str):
        if oldUnits=='':
            try:#see if no units at all
                float(value)
            except:
                if value[-1] =='2':
                    value =value.replace('2','')
                    is_square_units=True
                if '^' in value:
                    value =value.replace('^','')

            value, oldUnits = split_num_units(value)
        else:
            print('inconsitent units, if passing a string that includes unites, do no include oldUnits string')

        
    unitConv = {"nm": .000000001, "um": .000001, "mm": .001, "meter": 1.0, "m": 1.0,
                "cm": .01, "ft": .3048, "in": .0254, "mil": .0000254, "uin": .0000000254,
                'thz':1e12,'ghz':1e9,'mhz':1e6,'khz':1e3,'hz':1}

    sf = 1.0

    BaseUnits = None
    NewUnits = None
    if oldUnits.lower() in unitConv:
        BaseUnits = unitConv[oldUnits.lower()]
    if newUnits.lower() in unitConv:
        NewUnits = unitConv[newUnits.lower()]

    if BaseUnits != None and NewUnits != None:
        if is_square_units:
            sf = BaseUnits*BaseUnits/NewUnits/NewUnits
        else:
            sf = BaseUnits/NewUnits


    if oldUnits != newUnits:

        nuValue = value*sf
    else:
        nuValue = value


    return nuValue


def split_num_units(s):
    if '^' in s:
        s =s.replace('^','')
    s = s.replace(" ","").lower()
    value = s.rstrip('abcdefghijklmnopqrstuvwxyz')
    units = s[len(value):]
    value = float(value)
    return value, units



