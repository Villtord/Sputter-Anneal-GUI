#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:23:47 2018

@author: villtord
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 20:02:12 2017

@author: villtord
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal,QTimer
from PyQt5.QtGui import QIcon
from SPAN_UI import Ui_Dialog
import sys
import pickle
import pprint



class ExampleApp(QWidget, Ui_Dialog):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('hot.png'))
        
        self.cycles_count=0
        
        self.Load_Button.clicked.connect(self.load_file) # Load function
        self.Save_Button.clicked.connect(self.save_file) # Load function
        self.Start_Button.clicked.connect(self.start_toggle) # Load function
        
        self.my_sputter = sputter_procedure()
        self.my_anneal = anneal_procedure()
        
        self.my_sputter.sp_end_trigger.connect(self.sputter_end)
        self.my_anneal.an_end_trigger.connect(self.anneal_end)

        self.my_sputter.sp_start_trigger.connect(self.group_status)
        self.my_anneal.an_start_trigger.connect(self.group_status)
    
    def load_file(self):
        """ read values from saved file to a dictionary and then load it to GUI """
        load_file_name = QFileDialog.getOpenFileName(self, 'Open file', '','*.pkl')
        
        with open(load_file_name[0], 'rb') as f:
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
        
        save_file_string = QFileDialog.getSaveFileName(self, 'Save file as', '')
        
        if save_file_string[0].endswith('.pkl'):
            with open(save_file_string[0], 'wb') as f:
                pickle.dump(save_string, f)
        else:
            with open(save_file_string[0] + '.pkl', 'wb') as f:
                pickle.dump(save_string, f)
        f.close()
        
    def group_status(self,Flag):
            print ("disabling/enabling buttons")
        
            self.Sputter_Button.setEnabled(bool(Flag))
            self.Sputter_Energy.setEnabled(bool(Flag))
            self.Sputter_Pressure.setEnabled(bool(Flag))
            self.Sputter_Time.setEnabled(bool(Flag))
            self.Sputter_Pause.setEnabled(bool(Flag))
            
            self.Anneal_Button.setEnabled(bool(Flag))
            self.Anneal_Current.setEnabled(bool(Flag))
            self.Anneal_Ramp.setEnabled(bool(Flag))
            self.Anneal_Time.setEnabled(bool(Flag))
            self.Anneal_Pause.setEnabled(bool(Flag))
            
            self.Hot_Sputter_Current.setEnabled(bool(Flag))
            self.Hot_Sputter_Delay.setEnabled(bool(Flag))
            self.Hot_Sputter_radioButton.setEnabled(bool(Flag))
            self.Start_Button.setChecked(bool(Flag))
        
    def start_toggle(self):
        """ Main action when start button pressed """
        self. cycles_count=0
        
        if self.Start_Button.text()=="Start!":
            
            self.progressBar.setValue(0)

            self.Start_Button.setText('Stop!')
            
            self.total_time=(float(self.Sputter_Time.text())+
                 float(self.Sputter_Pause.text())+
                 float(self.Anneal_Time.text())+
                 float(self.Anneal_Ramp.text())+
                 float(self.Anneal_Pause.text()))*int(self.spinBox.value())*60
                            
            if self.Sputter_Button.isChecked(): 
                
                self.my_sputter.start()
                
            
            elif self.Anneal_Button.isChecked():
                
                self.my_anneal.start()
            
            else:  
                pass
                       
        else:
            
            self.my_sputter.stop()
            self.my_anneal.stop()
            
            self.group_status('whatever')

            self.Start_Button.setText('Start!')
            
    def sputter_end(self):
        
        
        if self.Anneal_Button.isChecked():
            
            self.my_anneal.start()
        
        else:
            
            self.cycles_count+=1
            
            if self.cycles_count<int(self.spinBox.value()):
                self.my_sputter.start()
            
            else:
                self.group_status('whatever')
                self.Start_Button.setChecked(False)
                self.Start_Button.setText('Start!')
                self.progressBar.setValue(100)
                pass
            
    def anneal_end(self):
            
        self.cycles_count+=1
        if self.cycles_count<int(self.spinBox.value()):
            if self.Sputter_Button.isChecked():
                self.my_sputter.start()
            else:
                self.my_anneal.start()
        else:
            self.group_status('whatever')
            self.Start_Button.setChecked(False)
            self.Start_Button.setText('Start!')
            self.progressBar.setValue(100)
            pass

class sputter_procedure(QThread):
    """ This class defines the sputter process itself """
    sp_start_trigger = pyqtSignal('QString')
    sp_end_trigger = pyqtSignal()
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()
        print ("sputter initializeed")
      
    def start(self):
        
        print ("sputter started")
        
        """ Here should be communication with sputter gun """
        self.sp_start_trigger.emit('')
        
        timer = QTimer(self)
        timer.timeout.connect(self.emit_signal_sputter)
        timer.setSingleShot(True)
        timer.start(2000)

    def emit_signal_sputter(self):
        
        print ("sputter finished")
        
        self.sp_end_trigger.emit()
    
    def stop(self):
        
        print ("sputter interrupted")
        quit()
        
class anneal_procedure(QThread):
    an_start_trigger = pyqtSignal('QString')
    an_end_trigger = pyqtSignal()
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()
        print ("anneal initializeed")
      
    def start(self):
        print ("anneal started")
        """ Here should be communication with power supply """
        self.an_start_trigger.emit('')
        
        timer = QTimer(self)
        timer.timeout.connect(self.emit_signal_anneal)
        timer.setSingleShot(True)
        timer.start(2000)
        
    def emit_signal_anneal(self):
        
        print ("anneal finished")
        self.an_end_trigger.emit()
    
    def stop(self):
        print ("anneal interrupted")
        quit()
          

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function