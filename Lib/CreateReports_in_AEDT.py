# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 17:03:46 2021

@author: asligar
"""

class AEDT_CreateReports():

    def __init__(self,aedtapp):
            self.aedtapp= aedtapp
            self.selected_setup ="Setup1:LastAdaptive"
            self.selected_freq = 28e9
            self.beam_var = 'BeamID'
            self.ff_setup = ''
            
    def get_report_name(self,name):
        
        oDesign = self.aedtapp.odesign
        oModule = oDesign.GetModule("ReportSetup")
            
        all_report_names = oModule.GetAllReportNames()
        report_name = name 
        original_name = report_name
        x = 1
        while report_name in all_report_names:
            report_name= original_name +str(x)
            x = x+1    
        return report_name

    def create_report_cdf(self,type_of_data,beam_ids,report_name="CDF"):
        """
        This uses the build in function for CDF calcultion added in 2020R1.
        Allows for dynamic traces, linked to design variations to be created
        """
        oDesign = self.aedtapp.odesign
        report_name = self.get_report_name(report_name)

        beam_ids = [str(i) for i in beam_ids]
        oModule = oDesign.GetModule("ReportSetup")
        oModule.CreateReport(report_name, "Far Fields", "Rectangular Plot", self.selected_setup, 
            [
                "Context:="        , self.ff_setup
            ], 
            [
                self.beam_var + ":="        , ["All"],
                "OverridingValues:="    , beam_ids,
                "Freq:="        , [str(self.selected_freq  )],
                "Phi:="            , ["All"],
                "Theta:="        , ["All"]
            ], 
            [
                "X Component:="        , "Freq",
                "Y Component:="        , ["max(" + type_of_data + ")"]
            ], 
            [
                "DisplayFamiliesType:="    , "CumulativeDistribute"
            ])
    
        return report_name
    
    def generate_envelope_pattern_3D(self,type_of_data,beam_ids,report_name="EnvelopePattern3D"):
        """
        Generates a beam pattern that is the max far field quanity using
        all possible beam ids
        """
        oDesign = self.aedtapp.odesign
        report_name = self.get_report_name(report_name)
    
        beam_ids = [str(i) for i in beam_ids]    
        oModule = oDesign.GetModule("ReportSetup")
        oModule.CreateReport(report_name, "Far Fields", "Rectangular Contour Plot", self.selected_setup , 
            [
                "Context:="        , self.ff_setup
            ], 
            [
                self.beam_var+":="        , ["All"],
                "OverridingValues:="    , beam_ids ,
                "Theta:="        , ["All"],
                "Phi:="            , ["All"],
                "Freq:="        , [str(self.selected_freq )]
            ], 
            [
                "X Component:="        , "Theta",
                "Y Component:="        , "Phi",
                "Z Component:="        , ["max(" + type_of_data + ")"]
            ])


        return report_name