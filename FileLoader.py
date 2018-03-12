# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 14:42:23 2018

@author: Victor Rogalev
"""
import pickle
from SPAN_UI import Ui_Dialog

class FileLoader_procedure (Ui_Dialog):
    
    def __init__(self, load_filename, save_filename):
        
        self.load_filename = load_filename
        self.save_filename = save_filename
        
    def load_file(self):
        """ read values from saved file to a dictionary and then load it to GUI """
        
        with open(self.load_filename[0], 'rb') as f:
            loaded_settings = pickle.load(f)
        
        f.close()
#       pprint.pprint(loaded_settings)
        self.Sputter_Button.setChecked(loaded_settings['Sputter_Button'])
        self.Sputter_Energy.setText(loaded_settings['Sputter_Energy'])
        self.Sputter_Pressure.setText(loaded_settings['Sputter_Pressure'])
        self.Sputter_Time.setText(loaded_settings['Sputter_Time'])
        self.Sputter_Pause.setText(loaded_settings['Sputter_Pause'])
        
        self.Anneal_Button.setChecked(loaded_settings['Anneal_Button'])
        self.Anneal_Current.setText(loaded_settings['Anneal_Current'])
        self.Anneal_Ramp.setText(loaded_settings['Anneal_Ramp'])
        self.Anneal_Time.setText(loaded_settings['Anneal_Time'])
        self.Anneal_Pause.setText(loaded_settings['Anneal_Pause'])
        
        self.Hot_Sputter_Current.setText(loaded_settings['Hot_Sputter_Current'])
        self.Hot_Sputter_Delay.setText(loaded_settings['Hot_Sputter_Delay'])
        self.Hot_Sputter_radioButton.setChecked(loaded_settings['Hot_Sputter_radioButton'])       
        
    def save_file(self):
        """ write values from table to a dictionary and then save it to a .pkl file """
        save_string={}
        
        save_string["Sputter_Button"]=self.Sputter_Button.isChecked()
        save_string["Sputter_Energy"]=self.Sputter_Energy.text()
        save_string["Sputter_Pressure"]=self.Sputter_Pressure.text()
        save_string["Sputter_Time"]=self.Sputter_Time.text()
        save_string["Sputter_Pause"]=self.Sputter_Pause.text()
        
        save_string["Anneal_Button"]=self.Anneal_Button.isChecked()
        save_string["Anneal_Current"]=self.Anneal_Current.text()
        save_string["Anneal_Ramp"]=self.Anneal_Ramp.text()
        save_string["Anneal_Time"]=self.Anneal_Time.text()
        save_string["Anneal_Pause"]=self.Anneal_Pause.text()
        
        save_string["Hot_Sputter_Current"]=self.Hot_Sputter_Current.text()
        save_string["Hot_Sputter_Delay"]=self.Hot_Sputter_Delay.text()
        save_string["Hot_Sputter_radioButton"]=self.Hot_Sputter_radioButton.isChecked()
        
        save_string["spinBox"]=self.spinBox.text()

        if self.save_filename[0].endswith('.pkl'):
            with open(self.save_filename[0], 'wb') as f:
                pickle.dump(save_string, f)
        else:
            with open(self.save_filename[0] + '.pkl', 'wb') as f:
                pickle.dump(save_string, f)
        f.close()